#!/usr/bin/env python3
"""Compile one additional CODE mutation against verified retained positives.

This supplements evidence only: no positive compilation or acceptance mutation.
--check revalidates the parent and saved negative without running a compiler.
"""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path

import progress
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.replay_toolchain import digest, entry_digest, freeze_toolchain, required_input_paths
from lib.unit_context import UnitContext, compiler_arguments, load_unit_target
from lib.unit_sources import validate_producer_inputs
from replay_units import cold_round, mapped_control_comparison

ROOT = Path(__file__).resolve().parents[1]
KIND = "supplementary-compiled-code-negative"


def parent_inputs(root: Path, parent: Path, unit_id: str, artifact: str):
    receipt = progress.accept(parent, root=root, artifact_name=artifact, validate_only=True)
    if receipt.get("kind") != "bounded-cxx-unit-exact-replay" or receipt.get("pass") is not True:
        raise ValueError("supplement needs a verified successful ordinary parent replay")
    context = UnitContext(root, artifact)
    config = context.config()
    entries = [entry for entry in config["units"] if entry["id"] == unit_id]
    results = [result for result in receipt["results"] if result["id"] == unit_id]
    controls = [control for control in config.get("controls", []) if control["unit"] == unit_id]
    if len(entries) != 1 or len(results) != 1 or len(controls) != 1:
        raise ValueError("supplement needs one verified CODE owner and its configured control")
    entry, result, mutation = entries[0], results[0], controls[0]
    if entry.get("extent_kind", "code") != "code" or not result["exact"]:
        raise ValueError("supplement cannot stand in for failed or non-CODE positives")
    if len(result.get("producer_paths", [])) != 2:
        raise ValueError("supplement needs both actual retained positive producers")
    return context, entry, result, mutation


def check(path: Path, *, root: Path = ROOT) -> dict:
    report = json.loads(path.read_text())
    if (report.get("kind") != KIND or report.get("schema_version") != 1 or
            report.get("authored_credit") != 0 or report.get("positive_compilations") != 0 or
            report.get("negative_compilations") != 1 or report.get("retained_positive_producers") != 2 or
            report.get("acceptance_changed") is not False):
        raise ValueError("invalid supplemental negative claim")
    parent = (root / report["parent_receipt"]).resolve()
    parent.relative_to((root / ".analysis").resolve())
    if digest(parent) != report["parent_receipt_sha256"]:
        raise ValueError("supplement parent identity changed")
    context, entry, result, mutation = parent_inputs(root, parent, report["unit"], report["artifact"])
    if report["entry_sha256"] != entry_digest(entry) or report["mutation"] != mutation:
        raise ValueError("supplement owner or configured mutation changed")
    source = path.parent / "negative/source"
    snapshots = result["source_inputs"]
    validate_producer_inputs(parent.parent / "inputs", source, entry, snapshots, mutation=mutation)
    prefix = ("#pragma option " + entry["wrapper_options"] + "\n") if entry.get("wrapper_options") else ""
    if (source / entry["module"]).read_text() != prefix + f'#include "{entry["source"]}"\n':
        raise ValueError("supplement compiler wrapper changed")
    expected = compiler_arguments(entry, context.binary)
    recorded = json.loads((source / "compiler-arguments.json").read_text())
    if recorded.get(entry["module"]) != expected or report["compiler_arguments"] != expected:
        raise ValueError("supplement actual compiler arguments changed")
    obj = source / (Path(entry["module"]).stem + ".obj")
    omf = describe_omf(obj.read_bytes())
    if (not omf["valid"] or omf["translator_comments"] != ["TC86 Borland C++ 4.02"] or
            omf != report["omf"]):
        raise ValueError("supplement compiler OMF changed")
    paths = required_input_paths(parent.parent / "inputs", entry, {"omfs": [omf]})
    if paths != {item["path"] for item in snapshots}:
        raise ValueError("supplement dependency scope differs from its retained positives")
    for name, expected_hash in report["outputs"].items():
        if name not in ("units.exe", "units.map") or digest(source / name) != expected_hash:
            raise ValueError("supplement saved output identity changed")
    if set(report["outputs"]) != {"units.exe", "units.map"}:
        raise ValueError("supplement requires both saved linked outputs")
    _, target, _ = load_unit_target(context, context.config())
    candidate = parse_mz((source / "units.exe").read_bytes())
    if not candidate.valid:
        raise ValueError("invalid supplemental linked MZ")
    comparison = mapped_control_comparison(target, candidate, entry, source / "units.map")
    progress.validate_control(comparison)
    if comparison != report["comparison"]:
        raise ValueError("supplement raw/ordered comparison changed")
    if digest(path.parent / "toolchain-attestation.json") != report["toolchain_receipt_sha256"]:
        raise ValueError("supplement tool receipt changed")
    if report["toolchain_receipt_sha256"] != json.loads(parent.read_text())["toolchain_receipt_sha256"]:
        raise ValueError("supplement changed the retained producer's pinned tool receipt")
    return report


def build(parent: Path, unit_id: str, output: Path, *, artifact: str = "main", root: Path = ROOT):
    parent = parent.resolve()
    parent.relative_to((root / ".analysis").resolve())
    context, entry, result, mutation = parent_inputs(root, parent, unit_id, artifact)
    parent_sha = digest(parent)
    output = output.resolve()
    output.relative_to((root / ".analysis").resolve())
    if output.exists():
        raise ValueError("supplement requires a fresh output directory")
    output.mkdir(parents=True)
    with (root / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(root, output / "toolchain-attestation.json")
        if tool["receipt_sha256"] != json.loads(parent.read_text())["toolchain_receipt_sha256"]:
            raise ValueError("supplement requires the same verified tool receipt as its positives")
        negative = cold_round(output / "negative", parent.parent / "inputs", [entry],
                              paths={item["path"] for item in result["source_inputs"]},
                              mutation=mutation, binary=context.binary)
    if digest(parent) != parent_sha:
        raise ValueError("parent receipt changed during supplemental compilation")
    _, target, _ = load_unit_target(context, context.config())
    comparison = mapped_control_comparison(target, negative["candidate"], entry,
                                           negative["source"] / "units.map")
    progress.validate_control(comparison)
    obj = negative["source"] / (Path(entry["module"]).stem + ".obj")
    report = dict(schema_version=1, kind=KIND, artifact=artifact, unit=unit_id,
                  parent_receipt=parent.relative_to(root).as_posix(), parent_receipt_sha256=parent_sha,
                  entry_sha256=entry_digest(entry), mutation=mutation, comparison=comparison,
                  compiler_arguments=negative["compiler_arguments"][unit_id],
                  toolchain_receipt_sha256=tool["receipt_sha256"], omf=describe_omf(obj.read_bytes()),
                  outputs={name: digest(negative["source"] / name) for name in ("units.exe", "units.map")},
                  positive_compilations=0, retained_positive_producers=2, negative_compilations=1,
                  authored_credit=0, acceptance_changed=False)
    path = output / "receipt.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    check(path, root=root)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--parent", type=Path)
    parser.add_argument("--unit")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--artifact", choices=("main", "op", "maine"), default="main")
    args = parser.parse_args()
    if args.check:
        path = args.check.resolve()
        check(path)
    else:
        if not all((args.parent, args.unit, args.output)):
            parser.error("--parent, --unit and --output are required to compile a supplement")
        path = build(args.parent, args.unit, args.output, artifact=args.artifact)
    print(json.dumps(dict(receipt=str(path), negative_rejected=True,
                          positive_compilations=0, acceptance_changed=False)))


if __name__ == "__main__":
    main()

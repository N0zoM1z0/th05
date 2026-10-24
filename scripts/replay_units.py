#!/usr/bin/env python3
"""Replay selected or changed C++ units with two isolated cold producers.

Only maintained dependencies and each selected binding scaffold are staged.
Unchanged units retain their earlier evidence; an empty default plan runs no
compiler, toolchain probes or target reads.
"""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import shutil
import sys
import tomllib
import uuid

from lib.omf import describe_omf
from lib.pc98 import digest_file, parse_mz
from lib.reference_build import Builder
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.unit_oracle import compare_unit, map_contribution
from lib.replay_toolchain import (bindings_source, digest, entry_digest, freeze_toolchain,
    required_input_paths, scoped_snapshot, snapshot_paths, staged_paths,
    static_toolchain, validate_snapshot)

ROOT = Path(__file__).resolve().parents[1]
OMF_FIELDS = ("sha256", "dependency_timestamp_normalized_sha256", "module_name",
              "translator_comments", "dependency_paths")


def select_units(root: Path, manifest: dict, requested: list[str] | None,
                 acceptance: dict | None = None) -> tuple[list[dict], dict[str, str]]:
    entries = {unit["id"]: unit for unit in manifest["units"]}
    if len(entries) != len(manifest["units"]):
        raise ValueError("duplicate configured unit IDs")
    if requested:
        if len(set(requested)) != len(requested) or set(requested) - entries.keys():
            raise ValueError("duplicate or unknown --units ID")
        return [entries[name] for name in requested], {name: "explicit" for name in requested}
    path = root / "config/accepted_units.json"
    if acceptance is None:
        acceptance = json.loads(path.read_text()) if path.exists() else {"units": []}
    saved = {item["id"]: item for item in acceptance["units"]}
    selected, reasons = [], {}
    for entry in entries.values():
        old = saved.get(entry["id"])
        reason = None
        if old is None:
            reason = "missing"
        elif old.get("entry_sha256") != entry_digest(entry):
            reason = "config-changed"
        elif old.get("toolchain_manifest_sha256", acceptance.get("toolchain_manifest_sha256")) != digest(root / "config/toolchain.toml"):
            reason = "toolchain-config-changed"
        else:
            try:
                validate_snapshot(root, scoped_snapshot(root, entry, old["result"], old["source_inputs"]))
            except (OSError, ValueError, KeyError):
                reason = "source-changed"
        if reason:
            selected.append(entry)
            reasons[entry["id"]] = reason
    return selected, reasons


def cold_round(work: Path, inputs: Path, units: list[dict], *,
               paths: set[str], mutation: dict | None = None) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    for name in sorted(paths):
        destination = source / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(inputs / name, destination)
    scaffolds = {bindings_source(unit) for unit in units}
    if len(scaffolds) != 1:
        raise ValueError("one cold group requires one binding scaffold")
    for unit in units:
        wrapper = source / unit["module"]
        wrapper.parent.mkdir(parents=True, exist_ok=True)
        prefix = ("#pragma option " + unit["wrapper_options"] + "\n") if unit.get("wrapper_options") else ""
        wrapper.write_text(prefix + f'#include "{unit["source"]}"\n')
    if mutation:
        path = source / mutation["source"]
        data = path.read_text()
        if not mutation["find"] or data.count(mutation["find"]) != 1 or mutation["find"] == mutation["replace"]:
            raise ValueError("compiled negative-control mutation anchor drifted")
        path.write_text(data.replace(mutation["find"], mutation["replace"]))
    shutil.copyfile(source / next(iter(scaffolds)), source / "bindings.asm")
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    dos = ["wine", str(builder.msdos), "-e", "-x"]
    builder.execute("bindings", ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t", "bindings.asm", "bindings.obj"])
    objects, omfs = [], {}
    for unit in units:
        obj = Path(unit["module"]).stem + ".obj"
        if obj in objects or obj.lower() == "bindings.obj":
            raise ValueError("duplicate generated object filename")
        builder.execute(obj, [*dos, "tcc", "-c", "-I.", "-O", "-b-", "-3", "-Z", "-d",
                              "-DGAME=5", "-ml", "-DBINARY='M'", unit["module"]])
        objects.append(obj)
        omf = describe_omf((source / obj).read_bytes())
        if not omf["valid"] or omf["translator_comments"] != ["TC86 Borland C++ 4.02"]:
            raise ValueError(f"invalid compiler object {obj}")
        omfs[unit["id"]] = {key: omf[key] for key in OMF_FIELDS}
    (source / "link.rsp").write_bytes(("-c -s -E bindings.obj " + " ".join(objects) +
                                      ", units.exe, units.map,\r\n").encode("ascii"))
    builder.execute("link", [*dos, "tlink", "@link.rsp"])
    candidate = parse_mz((source / "units.exe").read_bytes())
    if not candidate.valid:
        raise ValueError(str(candidate.errors))
    return {"source": source, "candidate": candidate, "omfs": omfs, "steps": builder.records}


def control_comparison(target, candidate, entry: dict, start: int, size: int) -> dict:
    if size == entry["size"]:
        return compare_unit(target, candidate, entry["target_start"], start, size)
    from lib.pc98 import digest_bytes
    from lib.unit_oracle import relative_fixups
    left = target.program_image[entry["target_start"]:entry["target_start"] + entry["size"]]
    right = candidate.program_image[start:start + size]
    if len(right) != size or not size:
        raise ValueError("truncated compiled negative contribution")
    left_fixups = relative_fixups(target, entry["target_start"], entry["size"])
    right_fixups = relative_fixups(candidate, start, size)
    return {"target_start": entry["target_start"], "candidate_start": start,
            "size": entry["size"], "candidate_size": size,
            "target_sha256": digest_bytes(left), "candidate_sha256": digest_bytes(right),
            "raw_exact": left == right, "target_fixups": left_fixups,
            "candidate_fixups": right_fixups, "fixups_exact": left_fixups == right_fixups,
            "exact": left == right and left_fixups == right_fixups}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--units", nargs="+", metavar="ID")
    parser.add_argument("--plan", action="store_true", help="report selected units without running tools")
    args = parser.parse_args()
    manifest_path = ROOT / "config/exact_units.toml"
    manifest_bytes = manifest_path.read_bytes()
    manifest = tomllib.loads(manifest_bytes.decode())
    units, reasons = select_units(ROOT, manifest, args.units)
    if not units or args.plan:
        print(json.dumps({"selected": reasons, "work_required": bool(units), "tools_executed": False}, indent=2))
        return 0
    controls = {row["unit"]: row for row in manifest.get("controls", [])}
    control_unit = next((unit for unit in units if unit["id"] in controls), None)
    if control_unit is None:
        raise ValueError("selected units need a configured natural source-mutation control")
    mutation = controls[control_unit["id"]]
    scopes = {unit["id"]: staged_paths(ROOT, unit) for unit in units}
    if mutation["source"] not in scopes[control_unit["id"]]:
        raise ValueError("negative-control source is outside its selected unit closure")
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), manifest["artifact"])
    target = parse_mz(read_verified_artifact(ROOT, artifact))
    work = (args.output or ROOT / ".analysis/unit-replays" / uuid.uuid4().hex).resolve()
    if work.exists():
        parser.error("cold replay requires a new output directory")
    work.relative_to((ROOT / ".analysis").resolve())
    work.mkdir(parents=True)
    (work / "exact-units.toml").write_bytes(manifest_bytes)
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        shutil.copyfile(ROOT / "config/toolchain.toml", work / "toolchain.toml")
        inputs = work / "inputs"
        frozen = snapshot_paths(ROOT, set().union(*scopes.values()))
        for item in frozen:
            destination = inputs / item["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / item["path"], destination)
        groups = {}
        for unit in units:
            groups.setdefault(bindings_source(unit), []).append(unit)
        results = []
        for index, members in enumerate(groups.values()):
            paths = set().union(*(scopes[unit["id"]] for unit in members))
            group = work / f"group-{index}"
            rounds = [cold_round(group / label, inputs, members, paths=paths) for label in ("a", "b")]
            for unit in members:
                comparisons = []
                for producer in rounds:
                    start, size = map_contribution(producer["source"] / "units.map", unit["module"], unit["segment"])
                    if size != unit["size"]:
                        raise ValueError(f"{unit['id']}: complete contribution size mismatch: {size}")
                    comparisons.append(compare_unit(target, producer["candidate"], unit["target_start"], start, size))
                omfs = [producer["omfs"][unit["id"]] for producer in rounds]
                result = {"id": unit["id"], "entry_sha256": entry_digest(unit), "rounds": comparisons,
                          "object_normalized_equal": len({obj["dependency_timestamp_normalized_sha256"] for obj in omfs}) == 1,
                          "omfs": omfs,
                          "producer_paths": [str(producer["source"].relative_to(work)) for producer in rounds]}
                actual = required_input_paths(inputs, unit, result)
                result["source_inputs"] = snapshot_paths(inputs, actual)
                result["exact"] = result["object_normalized_equal"] and all(row["exact"] for row in comparisons)
                results.append(result)
        negative = cold_round(work / "negative", inputs, [control_unit],
                              paths=scopes[control_unit["id"]], mutation=mutation)
        negative_dependencies = required_input_paths(inputs, control_unit,
            {"omfs": [negative["omfs"][control_unit["id"]]]})
        positive_control = next(row for row in results if row["id"] == control_unit["id"])
        if negative_dependencies != {row["path"] for row in positive_control["source_inputs"]}:
            raise ValueError("negative-control dependency scope differs from its positive producer")
        start, size = map_contribution(negative["source"] / "units.map", control_unit["module"], control_unit["segment"])
        control = control_comparison(target, negative["candidate"], control_unit, start, size)
        accepted = all(row["exact"] for row in results) and not control["exact"] and not control["raw_exact"]
        negative_record = {"unit_id": control_unit["id"], "entry_sha256": entry_digest(control_unit),
                           "mutation": mutation, "control_sha256": entry_digest(mutation),
                           "producer_path": "negative/source", "comparison": control,
                           "omf": negative["omfs"][control_unit["id"]]}
        # Source scanning stages a safe superset for conditional includes. Only
        # dependencies actually consumed by the cold producers remain frozen.
        used = {item["path"] for result in results for item in result["source_inputs"]}
        frozen = [item for item in frozen if item["path"] in used]
        for path in inputs.rglob("*"):
            if path.is_file() and path.relative_to(inputs).as_posix() not in used:
                path.unlink()
        receipt = {"schema_version": 2, "kind": "bounded-cxx-unit-exact-replay",
                   "target_sha256": artifact["sha256"], "manifest_sha256": digest(work / "exact-units.toml"),
                   "toolchain_receipt_sha256": tool["receipt_sha256"],
                   "toolchain_manifest_sha256": tool["manifest_sha256"], "toolchain_reused": tool["reused"],
                   "toolchain_reuse_proof_sha256": tool["proof_sha256"],
                   "source_inputs": frozen, "results": results,
                   "compiled_negative_control": control, "negative_control": negative_record,
                   "selected_units": [unit["id"] for unit in units],
                   "complete_executable_exact": False, "pass": accepted}
        live = tomllib.loads(manifest_path.read_text())
        current = {unit["id"]: unit for unit in live["units"]}
        for unit in units:
            if entry_digest(current[unit["id"]]) != entry_digest(unit):
                raise ValueError("selected unit configuration changed during replay")
        if mutation not in live.get("controls", []):
            raise ValueError("selected negative-control configuration changed during replay")
        validate_snapshot(ROOT, frozen)
        if static_toolchain(ROOT)[0] != tool["manifest_sha256"]:
            raise ValueError("toolchain configuration changed during replay")
        (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"pass": accepted, "selected": reasons,
                      "toolchain_reused": tool["reused"],
                      "results": [{"id": row["id"], "exact": row["exact"]} for row in results],
                      "compiled_negative_rejected": not control["exact"],
                      "receipt": str(work / "receipt.json")}, indent=2))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())

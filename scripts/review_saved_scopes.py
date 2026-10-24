#!/usr/bin/env python3
"""Review complete function scopes of retained whole-CODE producers, with no build.

The original two cold producers and negative producer are archived unchanged.
This is a review of those producers, never a claim of new cold compilation.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import shutil
import tomllib

from lib.pc98 import parse_mz
from lib.replay_toolchain import bindings_source, digest, entry_digest
from lib.unit_context import UnitContext, load_unit_target, unit_binary
from lib.unit_oracle import compare_mapped_unit, function_scoped, map_unit_scope
from lib.unit_sources import source_encoding
from replay_units import mapped_control_comparison

ROOT = Path(__file__).resolve().parents[1]
KIND = "reviewed-complete-scopes-of-retained-producers"
PARENT_KIND = "bounded-cxx-unit-exact-replay"


def archive_hashes(directory: Path) -> dict:
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError("retained producer archive must not contain symlinks")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = digest(path)
    return result


def producer_identity(entry: dict, context: UnitContext) -> tuple:
    return (entry["source"], entry["module"], entry.get("wrapper_options", ""),
            bindings_source(entry), unit_binary(entry, context.binary), source_encoding(entry), entry["segment"])


def check_scope_entries(parent_entry: dict, entries: list[dict], context: UnitContext,
                        *, retained_control: str | None = None) -> None:
    if (function_scoped(parent_entry) or parent_entry.get("extent_kind", "code") != "code" or not entries):
        raise ValueError("review requires a whole-CODE parent and nonempty complete function scopes")
    covered = []
    for entry in entries:
        retained = (entry["id"] == retained_control and entry_digest(entry) == entry_digest(parent_entry))
        if ((not function_scoped(entry) and not retained) or
                entry.get("extent_kind", "code") != "code" or
                producer_identity(entry, context) != producer_identity(parent_entry, context)):
            raise ValueError("reviewed scope changes actual source/module/flags/bindings/binary/encoding/segment")
        start, size = entry["target_start"], entry["size"]
        if (type(start) is not int or type(size) is not int or size <= 0 or start < parent_entry["target_start"] or
                start + size > parent_entry["target_start"] + parent_entry["size"]):
            raise ValueError("reviewed complete function escapes its parent extent")
        if any(start < right and start + size > left for left, right in covered):
            raise ValueError("reviewed complete function extents overlap")
        covered.append((start, start + size))
        relative = start - parent_entry["target_start"]
        for key in ("alignment_offsets", "padding_bytes", "code_data_ranges"):
            expected = []
            for item in parent_entry.get(key, []):
                offset = item if key == "alignment_offsets" else item["offset"]
                length = item["size"] if key == "code_data_ranges" else 1
                if offset < relative + size and offset + length > relative:
                    if offset < relative or offset + length > relative + size:
                        raise ValueError("function scope splits parent table/padding classification")
                    expected.append(offset - relative if key == "alignment_offsets" else {**item, "offset": offset - relative})
            if entry.get(key, []) != expected:
                raise ValueError("reviewed function must preserve parent table/padding classification")


def derive_review(root: Path, work: Path, config: dict, selected: list[str]) -> dict:
    """Mechanical projection after the caller fully validates the archived parent."""
    context = UnitContext(root, config["artifact"].removeprefix("th05-"))
    parent_work = work / "parent"
    parent_path = parent_work / "receipt.json"
    parent = json.loads(parent_path.read_text())
    if parent.get("kind") != PARENT_KIND or not parent.get("results"):
        raise ValueError("review requires original bounded whole-CODE producers")
    parent_config = tomllib.loads((parent_work / "exact-units.toml").read_text())
    parent_entries = {entry["id"]: entry for entry in parent_config["units"]}
    parents = []
    for result in parent["results"]:
        entry = parent_entries[result["id"]]
        # The original parent is still validated in full, including unselected
        # results. Only whole CODE contributions can supply new function scopes.
        if function_scoped(entry) or entry.get("extent_kind", "code") != "code":
            continue
        if (not result["object_normalized_equal"] or len(result["rounds"]) != 2 or
                not all(row["raw_exact"] for row in result["rounds"])):
            raise ValueError("retained parents must be deterministic raw-exact whole-CODE producers")
        parents.append((entry, result))
    configured = {entry["id"]: entry for entry in config["units"]}
    if not selected or len(selected) != len(set(selected)) or set(selected) - configured.keys():
        raise ValueError("review contains empty, duplicate or unknown new scope IDs")
    entries = [configured[name] for name in selected]
    if not any(function_scoped(entry) for entry in entries):
        raise ValueError("review must derive at least one complete function scope")
    owners = {}
    control_id = parent["negative_control"]["unit_id"]
    for entry in entries:
        matches = [(whole, result) for whole, result in parents
                   if producer_identity(entry, context) == producer_identity(whole, context) and
                   whole["target_start"] <= entry["target_start"] and
                   entry["target_start"] + entry["size"] <= whole["target_start"] + whole["size"]]
        if len(matches) != 1:
            raise ValueError("reviewed scope must belong to exactly one actual parent contribution")
        owners[entry["id"]] = matches[0]
    for whole, _ in parents:
        children = [entry for entry in entries if owners[entry["id"]][0]["id"] == whole["id"]]
        if children:
            check_scope_entries(whole, children, context, retained_control=control_id)
    artifact, target, target_view = load_unit_target(context, config)
    results = []
    for entry in entries:
        parent_entry, parent_result = owners[entry["id"]]
        producers = [parent_work / path for path in parent_result["producer_paths"]]
        candidates = [parse_mz((source / "units.exe").read_bytes()) for source in producers]
        comparisons = []
        for index, (source, candidate) in enumerate(zip(producers, candidates)):
            scope = map_unit_scope(source / "units.map", entry)
            parent_comparison = parent_result["rounds"][index]
            if (scope.get("contribution_start", scope["start"]) != parent_comparison["candidate_start"] or
                    scope.get("contribution_size", scope["size"]) != parent_entry["size"] or
                    scope["start"] - parent_comparison["candidate_start"] != entry["target_start"] - parent_entry["target_start"]):
                raise ValueError("function MAP placement is not the same relative scope inside its actual parent contribution")
            comparison = compare_mapped_unit(target, candidate, source / "units.map", entry)
            if not comparison["exact"]:
                raise ValueError(f"reviewed complete function is not raw/ordered-fixup exact: {entry['id']}")
            comparisons.append(comparison)
        result = {"id": entry["id"], "entry_sha256": entry_digest(entry), "rounds": comparisons,
                  "object_normalized_equal": parent_result["object_normalized_equal"],
                  "omfs": copy.deepcopy(parent_result["omfs"]),
                  "producer_paths": ["parent/" + path for path in parent_result["producer_paths"]],
                  "source_inputs": copy.deepcopy(parent_result.get("source_inputs", parent["source_inputs"])), "exact": True}
        for key in ("compiler_arguments", "producer_source_inputs"):
            if key in parent_result:
                result[key] = copy.deepcopy(parent_result[key])
        results.append(result)
    original_negative = parent["negative_control"]
    negative_source = parent_work / original_negative["producer_path"]
    negative_image = parse_mz((negative_source / "units.exe").read_bytes())
    changed = [(entry, mapped_control_comparison(target, negative_image, entry, negative_source / "units.map")) for entry in entries]
    owners = [(entry, comparison) for entry, comparison in changed if not comparison["raw_exact"]]
    if len(owners) != 1:
        raise ValueError("review must include exactly one raw-rejected natural mutation owner")
    owner, control = owners[0]
    mutation = {**original_negative["mutation"], "unit": owner["id"]}
    if mutation not in config.get("controls", []):
        raise ValueError("new negative owner must retain the identical parent mutation except its unit ID")
    negative = {**copy.deepcopy(original_negative), "unit_id": owner["id"], "entry_sha256": entry_digest(owner),
                "mutation": mutation, "control_sha256": entry_digest(mutation),
                "producer_path": "parent/" + original_negative["producer_path"], "comparison": control}
    receipt = {key: copy.deepcopy(parent[key]) for key in (
        "schema_version", "target_sha256", "toolchain_receipt_sha256", "toolchain_manifest_sha256",
        "toolchain_reused", "toolchain_reuse_proof_sha256", "source_inputs")}
    receipt.update(kind=KIND, compiler_invocations=0, retained_cold_producer_count=2,
                   parent_receipt_path="parent/receipt.json", parent_receipt_sha256=digest(parent_path),
                   parent_manifest_sha256=digest(parent_work / "exact-units.toml"), parent_aggregate_pass=parent["pass"],
                   parent_artifacts=archive_hashes(parent_work), manifest_sha256=digest(work / "exact-units.toml"),
                   results=results, negative_control=negative, compiled_negative_control=control,
                   selected_units=selected, complete_executable_exact=False, **{"pass": not control["raw_exact"] and not control["exact"]})
    if target_view is not None:
        receipt.update(artifact=context.artifact, target_view=target_view)
    return receipt


def validate_review(path: Path, *, root: Path, artifact_name: str, validate_parent) -> None:
    work = path.parent
    receipt = json.loads(path.read_text())
    if receipt.get("parent_receipt_path") != "parent/receipt.json" or receipt.get("compiler_invocations") != 0:
        raise ValueError("scope review cannot relabel new compiles or an arbitrary parent path")
    parent_path = work / "parent/receipt.json"
    parent = json.loads(parent_path.read_text())
    if (parent.get("kind") != PARENT_KIND or digest(parent_path) != receipt.get("parent_receipt_sha256") or
            archive_hashes(work / "parent") != receipt.get("parent_artifacts")):
        raise ValueError("retained parent receipt or producer archive was changed")
    validate_parent(parent_path)
    config = tomllib.loads((work / "exact-units.toml").read_text())
    if config["artifact"] != "th05-" + artifact_name:
        raise ValueError("scope review artifact context differs")
    expected = derive_review(root, work, config, receipt["selected_units"])
    if receipt != expected:
        raise ValueError("scope review is not the exact mechanical projection of retained producers")


def review(root: Path, artifact_name: str, parent_path: Path, selected: list[str], output: Path) -> Path:
    from progress import accept
    context = UnitContext(root, artifact_name)
    parent_path = parent_path.resolve()
    parent_work = parent_path.parent
    output = output.resolve()
    output.relative_to((root / ".analysis").resolve())
    if output.is_relative_to(parent_work) or parent_work.is_relative_to(output):
        raise ValueError("new review output must be separate from the retained parent tree")
    parent = json.loads(parent_path.read_text())
    if parent_path.name != "receipt.json" or parent.get("kind") != PARENT_KIND:
        raise ValueError("scope review requires an original bounded replay receipt")
    accept(parent_path, root=root, artifact_name=artifact_name, validate_only=True)
    before = archive_hashes(parent_work)
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(parent_work, output / "parent")
    if before != archive_hashes(output / "parent") or before != archive_hashes(parent_work):
        raise ValueError("retained producer changed during archive copy")
    for name in ("exact-units.toml",):
        shutil.copyfile(context.manifest, output / name)
    for name in ("inputs", "target-view"):
        if (parent_work / name).is_dir():
            shutil.copytree(parent_work / name, output / name)
    for name in ("toolchain-attestation.json", "toolchain-reuse-proof.json", "toolchain.toml"):
        shutil.copyfile(parent_work / name, output / name)
    config = tomllib.loads((output / "exact-units.toml").read_text())
    receipt = derive_review(root, output, config, selected)
    destination = output / "receipt.json"
    destination.write_text(json.dumps(receipt, indent=2) + "\n")
    accept(destination, root=root, artifact_name=artifact_name, validate_only=True)
    if before != archive_hashes(parent_work):
        raise ValueError("original parent changed while reviewing scopes")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", choices=("main", "op", "maine"), required=True)
    parser.add_argument("--from-receipt", type=Path, required=True)
    parser.add_argument("--units", nargs="+", metavar="NEW_FN_ID", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = review(ROOT, args.artifact, args.from_receipt, args.units, args.output)
    print(json.dumps({"receipt": str(receipt), "compiler_invocations": 0, "ledger_written": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

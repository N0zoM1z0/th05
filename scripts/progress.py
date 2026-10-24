#!/usr/bin/env python3
"""Render source-sensitive progress and merge independently replayed unit evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tomllib

from lib.replay_toolchain import (bindings_source, digest, entry_digest, relative_path,
    compiler_dependencies, scoped_snapshot, validate_snapshot)

ROOT = Path(__file__).resolve().parents[1]


def validate_result(entry: dict, result: dict) -> None:
    if result["id"] != entry["id"] or not result["exact"] or not result["object_normalized_equal"]:
        raise ValueError("unit receipt does not accept the configured source")
    if len(result["rounds"]) != 2 or len(result["omfs"]) != 2:
        raise ValueError("two independent cold rounds are required")
    hashes = set()
    for comparison in result["rounds"]:
        if (comparison["size"] != entry["size"] or comparison["target_start"] != entry["target_start"]
                or not all(comparison[k] for k in ("exact", "raw_exact", "fixups_exact"))
                or comparison["target_sha256"] != comparison["candidate_sha256"]
                or comparison["target_fixups"] != comparison["candidate_fixups"]):
            raise ValueError("raw bytes, boundaries or relocation evidence disagree")
        hashes.add(comparison["target_sha256"])
    if len(hashes) != 1:
        raise ValueError("cold extent bytes are nondeterministic")
    if len({obj["dependency_timestamp_normalized_sha256"] for obj in result["omfs"]}) != 1:
        raise ValueError("cold OMF objects are nondeterministic")
    if any(obj["translator_comments"] != ["TC86 Borland C++ 4.02"] for obj in result["omfs"]):
        raise ValueError("compiler producer identity disagrees")


def validate_control(control: dict) -> None:
    if control["raw_exact"] or control["exact"] or control["target_sha256"] == control["candidate_sha256"]:
        raise ValueError("compiled negative control was not rejected")


def summarize(root: Path = ROOT, acceptance: dict | None = None) -> dict:
    config = tomllib.loads((root / "config/exact_units.toml").read_text())
    entries = {unit["id"]: unit for unit in config["units"]}
    path = root / "config/accepted_units.json"
    acceptance = acceptance if acceptance is not None else json.loads(path.read_text()) if path.exists() else {"units": []}
    if acceptance["units"]:
        targets = tomllib.loads((root / "config/targets.toml").read_text())
        target = next(row for row in targets["artifacts"] if row["id"] == config["artifact"])
        if (acceptance["target_sha256"] != target["sha256"]
                or acceptance["toolchain_manifest_sha256"] != digest(root / "config/toolchain.toml")
                or acceptance["compiled_negative_rejected"] is not True):
            raise ValueError("target, toolchain or negative-control identity changed")
        validate_control(acceptance["compiled_negative_control"])
    accepted, covered = [], []
    for item in acceptance["units"]:
        entry = entries[item["id"]]
        if item["entry_sha256"] != entry_digest(entry):
            raise ValueError(f"unit configuration changed: {entry['id']}")
        validate_result(entry, item["result"])
        # Legacy whole-tree captures are narrowed using their original OMF
        # dependencies. Unrelated maintained files are never freshness inputs.
        snapshots = scoped_snapshot(root, entry, item["result"], item["source_inputs"])
        validate_snapshot(root, snapshots)
        if "compiled_negative_control" in item:
            validate_control(item["compiled_negative_control"])
        start, end = entry["target_start"], entry["target_start"] + entry["size"]
        if any(start < right and end > left for left, right in covered):
            raise ValueError("accepted unit extents overlap")
        covered.append((start, end))
        alignment = entry["alignment_offsets"]
        if len(alignment) != len(set(alignment)) or any(not 0 <= value < entry["size"] for value in alignment):
            raise ValueError("invalid alignment exclusions")
        accepted.append({"id": entry["id"], "size": entry["size"],
                         "instruction_bytes": entry["size"] - len(alignment),
                         "functions": entry["functions"]})
    return {"units": accepted, "unit_count": len(accepted),
            "functions": sum(unit["functions"] for unit in accepted),
            "complete_extent_bytes": sum(unit["size"] for unit in accepted),
            "instruction_bytes": sum(unit["instruction_bytes"] for unit in accepted),
            "percentage": None, "authored_denominator": None}


def render(summary: dict) -> tuple[str, str]:
    count, functions, instructions, extent = (summary[k] for k in
        ("unit_count", "functions", "instruction_bytes", "complete_extent_bytes"))
    alignment = extent - instructions
    markdown = f'''# TH05 progress

Goal: **98% authored bytes exact**. Global percentage: **unmeasured**; the
complete authored ownership denominator remains under review.

| Accepted scope | Functions | Instruction bytes | Complete extent bytes |
| --- | ---: | ---: | ---: |
| MAIN bounded C++ units | {functions} | {instructions} | {extent} |
| OP | 0 | 0 | 0 |
| MAINE | 0 | 0 | 0 |
| ZUN | 0 | 0 | 0 |

{count} complete C++ contributions pass two cold builds, raw bytes and ordered
relative relocation sites with explicit original external-symbol bindings.
Explicit codestring directives reproduce {alignment} observed NOP alignment bytes;
these bytes are checked but excluded from authored instruction credit.
These are bounded unit results; whole executable placement, standalone linkage
and packed-file exactness are separate and remain unaccepted.

The targets contain 256,877 stored bytes, or 319,268 decoded/container bytes.
Neither figure is an accepted authored denominator. Runtime/library/data/stub
ownership and unknown extents must be reviewed before publishing a percentage.

Generated by `python3 scripts/progress.py --write`. Public CI checks ledger
consistency and source freshness; actual exact replay requires private inputs.
See [oracle contract](ORACLES.md) and [first C++ units](reconstruction/FIRST_CXX_UNITS.md).
'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="164" viewBox="0 0 720 164" role="img" aria-labelledby="title desc">
<title id="title">TH05 source reconstruction progress</title>
<desc id="desc">Goal 98 percent authored bytes exact. {functions} functions, {instructions} instruction bytes exact. Global denominator under review.</desc>
<rect width="720" height="164" rx="12" fill="#181b29"/>
<g font-family="system-ui,sans-serif" fill="#f3f0fa">
<text x="24" y="35" font-size="21" font-weight="600">TH05 · Mystic Square</text>
<text x="24" y="62" font-size="14" fill="#c9bddc">Authored bytes exact · goal 98% · denominator under review</text>
<rect x="24" y="80" width="672" height="14" rx="7" fill="#363148"/>
<text x="24" y="120" font-size="16">{functions} functions · {instructions} instruction bytes · {count} cold-replayed C++ units</text>
<text x="24" y="146" font-size="12" fill="#c9bddc">Bounded unit evidence · whole executables and global percentage unaccepted</text>
</g></svg>
'''
    return markdown, svg


def _saved_source(work: Path, relative: str) -> Path:
    relative = relative_path(relative)
    path = (work / relative).resolve()
    path.relative_to(work.resolve())
    return path


def merge_acceptance(root: Path, previous: dict, imported: list[dict], *,
                     target_sha: str, tool_sha: str, replay_sha: str, control: dict) -> dict:
    """Replace only imported IDs, preserving each earlier unit's original evidence."""
    replacements = {item["id"]: item for item in imported}
    if len(replacements) != len(imported):
        raise ValueError("duplicate imported unit IDs")
    if previous.get("units") and previous.get("target_sha256") != target_sha:
        raise ValueError("cannot merge prior unit evidence from a different target")
    units = []
    entries = {entry["id"]: entry for entry in tomllib.loads((root / "config/exact_units.toml").read_text())["units"]}
    for original in previous.get("units", []):
        if original["id"] in replacements:
            continue
        item = dict(original)
        item["source_inputs"] = scoped_snapshot(root, entries[item["id"]], item["result"], item["source_inputs"])
        item.setdefault("toolchain_manifest_sha256", previous.get("toolchain_manifest_sha256"))
        item.setdefault("replay_receipt_sha256", previous.get("replay_receipt_sha256"))
        item.setdefault("compiled_negative_control", previous.get("compiled_negative_control"))
        units.append(item)
    units.extend(imported)
    order = {name: index for index, name in enumerate(entries)}
    units.sort(key=lambda item: order[item["id"]])
    return {"schema_version": 2, "scope": "bounded C++ unit bytes and fixup sites",
            "target_sha256": target_sha, "replay_receipt_sha256": replay_sha,
            "toolchain_manifest_sha256": tool_sha, "compiled_negative_rejected": True,
            "compiled_negative_control": control, "units": units}


def accept(receipt_path: Path, *, root: Path | None = None) -> None:
    """Recheck saved selected producers; no compilation or whole-cohort replay."""
    from lib.omf import describe_omf
    from lib.pc98 import parse_mz
    from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
    from lib.unit_oracle import compare_unit, map_contribution
    from replay_units import control_comparison
    root = ROOT if root is None else root
    receipt_path = receipt_path.resolve()
    work = receipt_path.parent
    receipt = json.loads(receipt_path.read_text())
    config = tomllib.loads((root / "config/exact_units.toml").read_text())
    entries = {entry["id"]: entry for entry in config["units"]}
    # A whole-manifest hash remains provenance, not a reason to invalidate
    # unrelated entries added after a completed replay.
    frozen_path = work / "exact-units.toml"
    if not frozen_path.is_file() or digest(frozen_path) != receipt["manifest_sha256"]:
        raise ValueError("frozen replay unit manifest disagrees with its receipt")
    frozen_entries = {entry["id"]: entry for entry in tomllib.loads(frozen_path.read_text())["units"]}
    tool_path = work / "toolchain-attestation.json"
    if digest(tool_path) != receipt["toolchain_receipt_sha256"]:
        raise ValueError("frozen toolchain attestation digest disagrees")
    tool = json.loads(tool_path.read_text())
    if not all(tool.get(key) is True for key in ("ready", "identity_pass", "execution_pass")):
        raise ValueError("frozen executable toolchain probes did not pass")
    tool_sha = tool["manifest_sha256"]
    if tool_sha != digest(root / "config/toolchain.toml"):
        raise ValueError("historical toolchain evidence cannot be relabelled as the active pin")
    if (work / "toolchain.toml").is_file() and digest(work / "toolchain.toml") != tool_sha:
        raise ValueError("frozen toolchain manifest disagrees with its original probe report")
    if receipt.get("schema_version", 1) >= 2:
        proof_path = work / "toolchain-reuse-proof.json"
        if digest(proof_path) != receipt.get("toolchain_reuse_proof_sha256"):
            raise ValueError("frozen static toolchain reuse proof digest disagrees")
        proof = json.loads(proof_path.read_text())
        if (proof["manifest_sha256"] != tool_sha or
                proof["original_full_receipt_sha256"] != receipt["toolchain_receipt_sha256"] or
                proof["reused"] != receipt["toolchain_reused"]):
            raise ValueError("static context proof relabels a different executable probe report")
    artifact = find_artifact(load_target_manifest(root / "config/targets.toml"), config["artifact"])
    if not receipt["pass"] or receipt["target_sha256"] != artifact["sha256"]:
        raise ValueError("replay target or selected aggregate verdict disagrees")
    target = parse_mz(read_verified_artifact(root, artifact))
    results = {result["id"]: result for result in receipt["results"]}
    if not results or len(results) != len(receipt["results"]):
        raise ValueError("empty or duplicate replay result set")
    control = receipt["compiled_negative_control"]
    validate_control(control)
    if "negative_control" in receipt:
        negative = receipt["negative_control"]
        if negative["unit_id"] not in results:
            raise ValueError("negative control belongs to an unselected unit")
        control_entry = entries[negative["unit_id"]]
        if negative["entry_sha256"] != entry_digest(control_entry):
            raise ValueError("negative-control unit configuration changed")
        if negative["control_sha256"] != entry_digest(negative["mutation"]):
            raise ValueError("negative-control mutation identity disagrees")
        if negative["comparison"] != control:
            raise ValueError("negative-control comparison records disagree")
    else:
        matches = [entries[name] for name in results if entries[name]["target_start"] == control["target_start"]
                   and entries[name]["size"] == control["size"]]
        if len(matches) != 1:
            raise ValueError("legacy negative-control owner is ambiguous")
        control_entry = matches[0]
        mutations = [row for row in config.get("controls", []) if row["unit"] == control_entry["id"]]
        if len(mutations) != 1:
            raise ValueError("legacy compiled mutation needs one explicit review control")
        negative = {"unit_id": control_entry["id"], "producer_path": "negative/source",
                    "mutation": mutations[0], "comparison": control,
                    "legacy_source_revalidated": True}
    imported = []
    frozen_inputs = {item["path"]: item["sha256"] for item in receipt["source_inputs"]}
    for name, result in results.items():
        entry = entries[name]
        if name not in frozen_entries or entry_digest(frozen_entries[name]) != entry_digest(entry):
            raise ValueError(f"replay entry changed: {name}")
        if result.get("entry_sha256", entry_digest(entry)) != entry_digest(entry):
            raise ValueError(f"replay result entry identity disagrees: {name}")
        validate_result(entry, result)
        snapshots = scoped_snapshot(root, entry, result, result.get("source_inputs", receipt["source_inputs"]))
        validate_snapshot(root, snapshots)
        for item in snapshots:
            frozen_name = item["path"]
            if frozen_name not in frozen_inputs and frozen_name == bindings_source(entry):
                frozen_name = "main_bindings.asm"
            if frozen_inputs.get(frozen_name) != item["sha256"] or digest(_saved_source(work / "inputs", frozen_name)) != item["sha256"]:
                raise ValueError("frozen compiler input snapshot disagrees")
        producers = result.get("producer_paths", ["a/source", "b/source"])
        if len(producers) != 2 or producers[0] == producers[1]:
            raise ValueError("independent cold producer paths are required")
        for index, producer in enumerate(producers):
            source = _saved_source(work, producer)
            candidate = parse_mz((source / "units.exe").read_bytes())
            start, size = map_contribution(source / "units.map", entry["module"], entry["segment"])
            if size != entry["size"] or compare_unit(target, candidate, entry["target_start"], start, size) != result["rounds"][index]:
                raise ValueError("saved raw target/candidate artifacts disagree with replay receipt")
            obj = describe_omf((source / (Path(entry["module"]).stem + ".obj")).read_bytes())
            if not obj["valid"] or any(obj[key] != value for key, value in result["omfs"][index].items()):
                raise ValueError("saved compiler object disagrees with replay receipt")
            prefix = ("#pragma option " + entry["wrapper_options"] + "\n") if entry.get("wrapper_options") else ""
            if (source / entry["module"]).read_text() != prefix + f'#include "{entry["source"]}"\n':
                raise ValueError("saved compiler wrapper disagrees with unit configuration")
            for item in snapshots:
                saved = source / item["path"]
                if not saved.is_file() and item["path"] == bindings_source(entry):
                    saved = source / "bindings.asm"
                if digest(saved) != item["sha256"]:
                    raise ValueError("saved cold source disagrees with its input snapshot")
        if any(target.program_image[entry["target_start"] + offset] != 0x90 for offset in entry["alignment_offsets"]):
            raise ValueError("reviewed alignment is not NOP in original target")
        imported.append({"id": name, "entry_sha256": entry_digest(entry), "result": result,
                         "source_inputs": snapshots, "toolchain_manifest_sha256": tool_sha,
                         "toolchain_receipt_sha256": receipt["toolchain_receipt_sha256"],
                         "replay_receipt_sha256": digest(receipt_path),
                         "compiled_negative_control": control, "negative_control": negative})
    negative_source = _saved_source(work, negative["producer_path"])
    start, size = map_contribution(negative_source / "units.map", control_entry["module"], control_entry["segment"])
    observed_control = control_comparison(target, parse_mz((negative_source / "units.exe").read_bytes()), control_entry, start, size)
    if observed_control != control:
        raise ValueError("saved compiled negative artifact disagrees with receipt")
    negative_obj = describe_omf((negative_source / (Path(control_entry["module"]).stem + ".obj")).read_bytes())
    if not negative_obj["valid"] or negative_obj["translator_comments"] != ["TC86 Borland C++ 4.02"]:
        raise ValueError("saved negative compiler object is invalid")
    if "omf" in negative and any(negative_obj[key] != value for key, value in negative["omf"].items()):
        raise ValueError("saved negative compiler object disagrees with its frozen identity")
    if compiler_dependencies(control_entry, [negative_obj]) != compiler_dependencies(control_entry, results[control_entry["id"]]["omfs"]):
        raise ValueError("negative compiler dependency scope differs from its selected unit")
    mutation = negative["mutation"]
    control_snapshots = next(item["source_inputs"] for item in imported if item["id"] == control_entry["id"])
    if mutation["source"] not in {item["path"] for item in control_snapshots}:
        raise ValueError("negative mutation is outside its selected compiler dependency scope")
    original = (root / mutation["source"]).read_text()
    if original.count(mutation["find"]) != 1 or (negative_source / mutation["source"]).read_text() != original.replace(mutation["find"], mutation["replace"]):
        raise ValueError("saved negative source does not reproduce its recorded natural mutation")
    acceptance_path = root / "config/accepted_units.json"
    previous = json.loads(acceptance_path.read_text()) if acceptance_path.exists() else {"units": []}
    acceptance = merge_acceptance(root, previous, imported, target_sha=artifact["sha256"],
                                  tool_sha=tool_sha, replay_sha=digest(receipt_path), control=control)
    summarize(root, acceptance)
    temporary = acceptance_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(acceptance, indent=2) + "\n")
    temporary.replace(acceptance_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept", type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.accept:
        accept(args.accept)
    summary = summarize()
    md, svg = render(summary)
    for name, content in (("docs/PROGRESS.md", md), ("resources/progress.svg", svg)):
        path = ROOT / name
        if args.write:
            path.write_text(content)
        elif args.check and path.read_text() != content:
            raise ValueError(f"stale generated progress: {name}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render source-sensitive progress from bounded cold-replay receipts.

Public checks validate receipt consistency and source freshness. Reproducing
the actual byte comparisons requires the private targets and pinned compiler.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry_digest(entry: dict) -> str:
    return hashlib.sha256(json.dumps(entry, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


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
    if len({o["dependency_timestamp_normalized_sha256"] for o in result["omfs"]}) != 1:
        raise ValueError("cold OMF objects are nondeterministic")
    if any(o["translator_comments"] != ["TC86 Borland C++ 4.02"] for o in result["omfs"]):
        raise ValueError("compiler producer identity disagrees")


def summarize(root: Path = ROOT, acceptance: dict | None = None) -> dict:
    config = tomllib.loads((root / "config/exact_units.toml").read_text())
    entries = {u["id"]: u for u in config["units"]}
    path = root / "config/accepted_units.json"
    acceptance = acceptance if acceptance is not None else json.loads(path.read_text()) if path.exists() else {"units": []}
    if acceptance["units"]:
        targets = tomllib.loads((root / "config/targets.toml").read_text())
        target = next(a for a in targets["artifacts"] if a["id"] == config["artifact"])
        if (acceptance["target_sha256"] != target["sha256"]
                or acceptance["toolchain_manifest_sha256"] != digest(root / "config/toolchain.toml")
                or acceptance["compiled_negative_rejected"] is not True):
            raise ValueError("target, toolchain or negative-control identity changed")
        control = acceptance["compiled_negative_control"]
        if control["raw_exact"] or control["exact"] or control["target_sha256"] == control["candidate_sha256"]:
            raise ValueError("compiled negative control was not rejected")
    accepted = []
    covered = []
    for item in acceptance["units"]:
        entry = entries[item["id"]]
        if item["entry_sha256"] != entry_digest(entry):
            raise ValueError(f"unit configuration changed: {entry['id']}")
        validate_result(entry, item["result"])
        snapshots = {s["path"] for s in item["source_inputs"]}
        dependencies = {d.replace("\\", "/") for o in item["result"]["omfs"] for d in o["dependency_paths"]
                        if d.startswith("src/")}
        if not {entry["source"], "main_bindings.asm", *dependencies}.issubset(snapshots):
            raise ValueError("source snapshot omits maintained compiler dependencies")
        for source in item["source_inputs"]:
            if Path(source["path"]).is_absolute() or ".." in Path(source["path"]).parts:
                raise ValueError("source snapshot path escapes the repository")
            live = root / ("probes/units/main_bindings.asm" if source["path"] == "main_bindings.asm" else source["path"])
            if digest(live) != source["sha256"]:
                raise ValueError(f"accepted source changed: {source['path']}")
        start, end = entry["target_start"], entry["target_start"] + entry["size"]
        if any(start < b and end > a for a, b in covered):
            raise ValueError("accepted unit extents overlap")
        covered.append((start, end))
        alignment = entry["alignment_offsets"]
        if len(alignment) != len(set(alignment)) or any(not 0 <= a < entry["size"] for a in alignment):
            raise ValueError("invalid alignment exclusions")
        accepted.append({"id": entry["id"], "size": entry["size"],
                         "instruction_bytes": entry["size"] - len(alignment),
                         "functions": entry["functions"]})
    return {"units": accepted, "unit_count": len(accepted),
            "functions": sum(u["functions"] for u in accepted),
            "complete_extent_bytes": sum(u["size"] for u in accepted),
            "instruction_bytes": sum(u["instruction_bytes"] for u in accepted),
            "percentage": None, "authored_denominator": None}


def render(summary: dict) -> tuple[str, str]:
    count, functions, instructions, extent = (summary[k] for k in
        ("unit_count", "functions", "instruction_bytes", "complete_extent_bytes"))
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
Explicit codestring directives reproduce five observed NOP alignment bytes;
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


def accept(receipt_path: Path) -> None:
    # Import a completed private replay; no compiler or target bytes are copied.
    from lib.omf import describe_omf
    from lib.pc98 import parse_mz
    from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
    from lib.unit_oracle import compare_unit, map_contribution
    receipt = json.loads(receipt_path.read_text())
    config = tomllib.loads((ROOT / "config/exact_units.toml").read_text())
    if receipt["manifest_sha256"] != digest(ROOT / "config/exact_units.toml"):
        raise ValueError("replay was built with a different unit configuration")
    tool_path = receipt_path.parent / "toolchain-attestation.json"
    if digest(tool_path) != receipt["toolchain_receipt_sha256"]:
        raise ValueError("frozen toolchain attestation digest disagrees")
    tool = json.loads(tool_path.read_text())
    if (tool["manifest_sha256"] != digest(ROOT / "config/toolchain.toml")
            or not all(tool[k] for k in ("ready", "identity_pass", "execution_pass"))):
        raise ValueError("toolchain manifest or executable probe identity disagrees")
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    if not receipt["pass"] or receipt["target_sha256"] != artifact["sha256"]:
        raise ValueError("replay target or aggregate verdict disagrees")
    control = receipt["compiled_negative_control"]
    if control["exact"] or control["raw_exact"] or control["target_sha256"] == control["candidate_sha256"]:
        raise ValueError("compiled negative control was not rejected")
    target = parse_mz(read_verified_artifact(ROOT, artifact))
    results = {r["id"]: r for r in receipt["results"]}
    units = []
    for entry in config["units"]:
        validate_result(entry, results[entry["id"]])
        for index, label in enumerate(("a", "b")):
            source = receipt_path.parent / label / "source"
            candidate = parse_mz((source / "units.exe").read_bytes())
            start, size = map_contribution(source / "units.map", entry["module"], entry["segment"])
            observed = compare_unit(target, candidate, entry["target_start"], start, size)
            if observed != results[entry["id"]]["rounds"][index]:
                raise ValueError("saved raw target/candidate artifacts disagree with the replay receipt")
            obj = describe_omf((source / (Path(entry["module"]).stem + ".obj")).read_bytes())
            expected = results[entry["id"]]["omfs"][index]
            if not obj["valid"] or any(obj[k] != v for k, v in expected.items()):
                raise ValueError("saved compiler object disagrees with the replay receipt")
        if any(target.program_image[entry["target_start"] + i] != 0x90 for i in entry["alignment_offsets"]):
            raise ValueError("reviewed alignment is not NOP in the original target")
        units.append({"id": entry["id"], "entry_sha256": entry_digest(entry),
                      "result": results[entry["id"]], "source_inputs": receipt["source_inputs"]})
    for item in receipt["source_inputs"]:
        if digest(receipt_path.parent / "inputs" / item["path"]) != item["sha256"]:
            raise ValueError("frozen compiler input snapshot disagrees")
    negative_source = receipt_path.parent / "negative/source"
    tune = next(e for e in config["units"] if e["id"] == "main-bullet-tune")
    start, size = map_contribution(negative_source / "units.map", tune["module"], tune["segment"])
    actual_control = compare_unit(target, parse_mz((negative_source / "units.exe").read_bytes()),
                                  tune["target_start"], start, size)
    if actual_control != control:
        raise ValueError("saved compiled negative artifact disagrees with the receipt")
    acceptance = {"schema_version": 1, "scope": "bounded C++ unit bytes and fixup sites",
                  "target_sha256": artifact["sha256"], "replay_receipt_sha256": digest(receipt_path),
                  "toolchain_manifest_sha256": digest(ROOT / "config/toolchain.toml"),
                  "compiled_negative_rejected": True, "compiled_negative_control": control, "units": units}
    summarize(ROOT, acceptance)
    (ROOT / "config/accepted_units.json").write_text(json.dumps(acceptance, indent=2) + "\n")


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

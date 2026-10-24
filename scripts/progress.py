#!/usr/bin/env python3
"""Render source-sensitive progress and merge independently replayed unit evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import tomllib
from lib.unit_oracle import function_scoped
from lib.unit_context import UnitContext, compiler_arguments, load_unit_target, validate_public_target_view

from lib.replay_toolchain import (bindings_source, digest, entry_digest, relative_path,
    compiler_dependencies, scoped_snapshot, validate_snapshot)

ROOT = Path(__file__).resolve().parents[1]


def classify_extent(entry: dict, *, target_bytes: bytes | None = None) -> dict:
    """Classify a completely compared extent without exempting any raw bytes.

    Only explicit compiler switch tables are CODE data. Asset arrays, unknown
    ranges and padding never receive an implicit instruction-byte exemption.
    This metadata does not independently prove a range's compiler ownership.
    """
    size = entry["size"]
    if type(size) is not int or size <= 0:
        raise ValueError("invalid complete unit extent size")
    alignment = entry.get("alignment_offsets", [])
    explicit_padding = entry.get("padding_bytes", [])
    code_ranges = entry.get("code_data_ranges", [])
    if any(not isinstance(value, list) for value in (alignment, explicit_padding, code_ranges)):
        raise ValueError("extent classifications must be explicit lists")
    padding = {}
    for offset in alignment:
        if type(offset) is not int or not 0 <= offset < size or offset in padding:
            raise ValueError("invalid or duplicate NOP alignment padding")
        padding[offset] = 0x90
    for item in explicit_padding:
        if not isinstance(item, dict) or set(item) != {"offset", "value"}:
            raise ValueError("padding requires only explicit offset and byte value")
        offset, value = item["offset"], item["value"]
        if (type(offset) is not int or not 0 <= offset < size or
                type(value) is not int or not 0 <= value <= 255 or offset in padding):
            raise ValueError("invalid, duplicate or overlapping padding byte")
        padding[offset] = value
    ranges = []
    code_data = 0
    for item in code_ranges:
        if not isinstance(item, dict) or set(item) != {"offset", "size", "kind"}:
            raise ValueError("CODE data requires only explicit offset, size and compiler kind")
        if item["kind"] != "compiler-switch-table":
            raise ValueError("only compiler-switch-table CODE data is supported; assets are not CODE tables")
        start, length = item["offset"], item["size"]
        if (type(start) is not int or type(length) is not int or
                start < 0 or length <= 0 or start + length > size):
            raise ValueError("CODE data range is empty or outside the complete unit")
        end = start + length
        if any(start < other_end and end > other_start for other_start, other_end in ranges):
            raise ValueError("CODE data ranges overlap")
        if any(start <= offset < end for offset in padding):
            raise ValueError("CODE data and padding overlap")
        ranges.append((start, end))
        code_data += length
    authored = size - len(padding)
    if authored - code_data <= 0:
        raise ValueError("a C++ code contribution must retain instruction bytes")
    if target_bytes is not None:
        if len(target_bytes) != size:
            raise ValueError("padding verification requires the complete original extent")
        if any(target_bytes[offset] != value for offset, value in padding.items()):
            raise ValueError("declared padding value disagrees with the original target")
    return {"authored_code_bytes": authored, "code_data_bytes": code_data,
            "instruction_bytes": authored - code_data, "padding_bytes": len(padding)}


def validate_result(entry: dict, result: dict, *, require_exact: bool = True) -> None:
    classify_extent(entry)
    scoped = function_scoped(entry)
    if (result["id"] != entry["id"] or type(result["exact"]) is not bool or
            (require_exact and not result["exact"]) or result["object_normalized_equal"] is not True):
        raise ValueError("unit receipt does not accept the configured source")
    if len(result["rounds"]) != 2 or len(result["omfs"]) != 2:
        raise ValueError("two independent cold rounds are required")
    hashes, candidates = set(), set()
    for comparison in result["rounds"]:
        if (comparison["size"] != entry["size"] or comparison["target_start"] != entry["target_start"]
                or any(type(comparison[k]) is not bool for k in ("exact", "raw_exact", "fixups_exact"))
                or comparison["raw_exact"] != (comparison["target_sha256"] == comparison["candidate_sha256"])
                or comparison["fixups_exact"] != (comparison["target_fixups"] == comparison["candidate_fixups"])
                or comparison["exact"] != (comparison["raw_exact"] and comparison["fixups_exact"])
                or (require_exact and not comparison["exact"])):
            raise ValueError("raw bytes, boundaries or relocation evidence disagree")
        if scoped:
            scope = comparison.get("map_scope", {})
            integers = ("start", "size", "contribution_start", "contribution_size")
            if (any(type(scope.get(key)) is not int for key in integers) or
                    scope.get("kind") != "complete-function" or
                    scope.get("function_symbol") != entry["function_symbol"] or
                    scope["start"] != comparison["candidate_start"] or scope["size"] != entry["size"] or
                    scope["contribution_start"] < 0 or scope["contribution_size"] <= 0 or
                    scope["start"] < scope["contribution_start"] or
                    scope["start"] + scope["size"] > scope["contribution_start"] + scope["contribution_size"]):
                raise ValueError("complete function MAP containment evidence disagrees")
            at_end = scope["start"] + scope["size"] == scope["contribution_start"] + scope["contribution_size"]
            if (scope.get("boundary_kind") != ("contribution-end" if at_end else "next-function") or
                    (at_end and scope.get("next_function_symbol") is not None) or
                    (not at_end and not isinstance(scope.get("next_function_symbol"), str)) or
                    ("function_end_symbol" in entry and scope.get("next_function_symbol") != entry["function_end_symbol"])):
                raise ValueError("complete function next-boundary evidence disagrees")
        hashes.add(comparison["target_sha256"])
        candidates.add((comparison["candidate_sha256"], tuple(comparison["candidate_fixups"])))
    if len(hashes) != 1:
        raise ValueError("cold extent bytes are nondeterministic")
    if len(candidates) != 1:
        raise ValueError("cold candidate bytes or ordered fixups are nondeterministic")
    if result["exact"] != all(row["exact"] for row in result["rounds"]):
        raise ValueError("unit aggregate exact verdict disagrees with its cold evidence")
    if len({obj["dependency_timestamp_normalized_sha256"] for obj in result["omfs"]}) != 1:
        raise ValueError("cold OMF objects are nondeterministic")
    if any(obj["translator_comments"] != ["TC86 Borland C++ 4.02"] for obj in result["omfs"]):
        raise ValueError("compiler producer identity disagrees")


def validate_control(control: dict) -> None:
    if control["raw_exact"] or control["exact"] or control["target_sha256"] == control["candidate_sha256"]:
        raise ValueError("compiled negative control was not rejected")


def select_accept_units(results: dict, requested: list[str] | None, control_id: str) -> set[str]:
    if requested is None:
        selected = set(results)
    else:
        if not requested or len(requested) != len(set(requested)) or set(requested) - results.keys():
            raise ValueError("accept subset contains empty, duplicate or unknown unit IDs")
        selected = set(requested)
    if control_id not in selected:
        raise ValueError("accept subset must include the compiled negative-control owner")
    if any(results[name].get("exact") is not True for name in selected):
        raise ValueError("every accepted unit must have an exact real replay result")
    return selected


def validate_receipt_aggregate(receipt: dict, results: dict, control: dict) -> bool:
    """Call after saved producers have reproduced every result, selected or not."""
    observed = all(result["exact"] for result in results.values()) and not control["exact"] and not control["raw_exact"]
    if type(receipt.get("pass")) is not bool or receipt["pass"] != observed:
        raise ValueError("receipt aggregate pass verdict disagrees with all saved results/control")
    return observed


def replay_entries_for_accept(live: dict, frozen: dict, results: dict,
                              requested: list[str] | None) -> dict:
    """Excluded failed entries may leave the live manifest after subset import."""
    if requested is not None and set(requested) - live.keys():
        raise ValueError("accepted subset units must still exist in the live manifest")
    resolved = {}
    for name in results:
        if name not in frozen or (name in live and entry_digest(live[name]) != entry_digest(frozen[name])):
            raise ValueError(f"replay entry changed or missing from frozen manifest: {name}")
        if name not in live and (requested is None or name in requested):
            raise ValueError("only explicitly excluded replay entries may use frozen configuration")
        resolved[name] = live.get(name, frozen[name])
    return resolved


def summarize(root: Path = ROOT, acceptance: dict | None = None, *, artifact_name: str = "main") -> dict:
    context = UnitContext(root, artifact_name)
    config = context.config()
    entries = {unit["id"]: unit for unit in config["units"]}
    path = context.ledger
    acceptance = acceptance if acceptance is not None else json.loads(path.read_text()) if path.exists() else {"units": []}
    if acceptance["units"]:
        targets = tomllib.loads((root / "config/targets.toml").read_text())
        target = next(row for row in targets["artifacts"] if row["id"] == config["artifact"])
        if (acceptance["target_sha256"] != target["sha256"]
                or acceptance["toolchain_manifest_sha256"] != digest(root / "config/toolchain.toml")
                or acceptance["compiled_negative_rejected"] is not True):
            raise ValueError("target, toolchain or negative-control identity changed")
        validate_control(acceptance["compiled_negative_control"])
    target_view = acceptance.get("target_view") if acceptance["units"] and artifact_name != "main" else None
    if acceptance["units"] and artifact_name != "main":
        validate_public_target_view(context, config, target_view, target["sha256"])
        if acceptance.get("artifact") != context.artifact:
            raise ValueError("decoded ledger comparison context changed")
    accepted, covered = [], []
    for item in acceptance["units"]:
        entry = entries[item["id"]]
        if item["entry_sha256"] != entry_digest(entry):
            raise ValueError(f"unit configuration changed: {entry['id']}")
        validate_result(entry, item["result"])
        if target_view is not None and item.get("target_view") != target_view:
            raise ValueError("accepted decoded unit belongs to a different comparison context")
        if artifact_name != "main" or "binary" in entry:
            if item["result"].get("compiler_arguments") != [compiler_arguments(entry, context.binary)] * 2:
                raise ValueError("accepted producer binary arguments changed")
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
        accepted.append({"id": entry["id"], "size": entry["size"],
                         **classify_extent(entry),
                         "functions": entry["functions"]})
    return {"units": accepted, "unit_count": len(accepted),
            "functions": sum(unit["functions"] for unit in accepted),
            "complete_extent_bytes": sum(unit["size"] for unit in accepted),
            "authored_code_bytes": sum(unit["authored_code_bytes"] for unit in accepted),
            "code_data_bytes": sum(unit["code_data_bytes"] for unit in accepted),
            "padding_bytes": sum(unit["padding_bytes"] for unit in accepted),
            "instruction_bytes": sum(unit["instruction_bytes"] for unit in accepted),
            "percentage": None, "authored_denominator": None}


def summarize_all(root: Path = ROOT) -> dict:
    summaries = {"main": summarize(root)}
    for name in ("op", "maine"):
        if UnitContext(root, name).manifest.exists():
            summaries[name] = summarize(root, artifact_name=name)
    combined = dict(summaries["main"])
    for key in ("unit_count", "functions", "complete_extent_bytes", "authored_code_bytes", "code_data_bytes", "padding_bytes", "instruction_bytes"):
        combined[key] = sum(summary[key] for summary in summaries.values())
    combined["units"] = [{**unit, "artifact": name, "id": name + ":" + unit["id"]}
                         for name, summary in summaries.items() for unit in summary["units"]]
    combined["artifacts"] = summaries
    return combined


def render(summary: dict) -> tuple[str, str]:
    count, functions, instructions, extent = (summary[key] for key in
        ("unit_count", "functions", "instruction_bytes", "complete_extent_bytes"))
    authored = summary.get("authored_code_bytes", instructions)
    tables = summary.get("code_data_bytes", 0)
    padding = summary.get("padding_bytes", extent - authored)
    scopes = summary.get("artifacts", {"main": summary})
    rows = []
    for name, label in (("main", "MAIN bounded C++ units"), ("op", "OP decoded C++ units"), ("maine", "MAINE decoded C++ units")):
        scope = scopes.get(name, {})
        rows.append("| " + label + " | " + " | ".join(str(scope.get(key, 0)) for key in
                    ("functions", "authored_code_bytes", "instruction_bytes", "code_data_bytes", "complete_extent_bytes")) + " |")
    scope_rows = "\n".join(rows)
    markdown = f'''# TH05 progress

Goal: **98% authored bytes exact**. Global percentage: **unmeasured**; the
complete authored ownership denominator remains under review.

| Accepted scope | Functions | Authored code bytes | Instruction bytes | CODE table bytes | Complete extent bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
{scope_rows}
| ZUN | 0 | 0 | 0 | 0 | 0 |

{count} bounded C++ units pass two cold builds, raw bytes and ordered
relative relocation sites with explicit original external-symbol bindings.
A unit covers a complete compiler contribution or one reviewed complete
function. Unaccepted functions in the same translation unit receive no credit.
Authored code includes {tables} bytes of explicitly classified compiler switch
tables; these remain separate from instruction bytes. All {padding} observed
padding bytes are checked against their declared target values and excluded
from authored code. Every table and padding byte remains inside the complete
raw-byte comparisons; classification supplies no byte-comparison exemption.
Asset arrays are not compiler-switch-table metadata.
These are bounded unit results; whole executable placement, standalone linkage
and packed-file exactness are separate and remain unaccepted.
OP/MAINE comparisons use their retained decoded load modules and original
observed relocation order; they grant no packed-file exactness.

The targets contain 256,877 stored bytes, or 319,268 decoded/container bytes.
Neither figure is an accepted authored denominator. Runtime/library/data/stub
ownership and unknown extents must be reviewed before publishing a percentage.

Generated by `python3 scripts/progress.py --write`. Public CI checks ledger
consistency and source freshness; actual exact replay requires private inputs.
See [oracle contract](ORACLES.md) and [first C++ units](reconstruction/FIRST_CXX_UNITS.md).
'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="164" viewBox="0 0 720 164" role="img" aria-labelledby="title desc">
<title id="title">TH05 source reconstruction progress</title>
<desc id="desc">Goal 98 percent authored bytes exact. {functions} functions, {authored} authored code bytes exact: {instructions} instruction and {tables} compiler switch-table bytes. Global denominator under review.</desc>
<rect width="720" height="164" rx="12" fill="#181b29"/>
<g font-family="system-ui,sans-serif" fill="#f3f0fa">
<text x="24" y="35" font-size="21" font-weight="600">TH05 · Mystic Square</text>
<text x="24" y="62" font-size="14" fill="#c9bddc">Authored code bytes exact · goal 98% · denominator under review</text>
<rect x="24" y="80" width="672" height="14" rx="7" fill="#363148"/>
<text x="24" y="120" font-size="16">{functions} functions · {authored} authored code bytes · {count} cold-replayed C++ units</text>
<text x="24" y="146" font-size="12" fill="#c9bddc">{instructions} instruction · {tables} compiler switch-table · {padding} padding bytes · bounded extents</text>
</g></svg>
'''
    return markdown, svg


def _saved_source(work: Path, relative: str) -> Path:
    relative = relative_path(relative)
    path = (work / relative).resolve()
    path.relative_to(work.resolve())
    return path


def merge_acceptance(root: Path, previous: dict, imported: list[dict], *,
                     target_sha: str, tool_sha: str, replay_sha: str, control: dict,
                     artifact_name: str = "main") -> dict:
    """Replace only imported IDs, preserving each earlier unit's original evidence."""
    replacements = {item["id"]: item for item in imported}
    if len(replacements) != len(imported):
        raise ValueError("duplicate imported unit IDs")
    if previous.get("units") and previous.get("target_sha256") != target_sha:
        raise ValueError("cannot merge prior unit evidence from a different target")
    units = []
    entries = {entry["id"]: entry for entry in tomllib.loads(UnitContext(root, artifact_name).manifest.read_text())["units"]}
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


def accept(receipt_path: Path, *, root: Path | None = None, units: list[str] | None = None,
           artifact_name: str = "main") -> None:
    """Recheck saved selected producers; no compilation or whole-cohort replay."""
    from lib.omf import describe_omf
    from lib.pc98 import parse_mz
    from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
    from lib.unit_oracle import compare_mapped_unit
    from replay_units import mapped_control_comparison
    root = ROOT if root is None else root
    context = UnitContext(root, artifact_name)
    receipt_path = receipt_path.resolve()
    work = receipt_path.parent
    receipt = json.loads(receipt_path.read_text())
    config = context.config()
    entries = {entry["id"]: entry for entry in config["units"]}
    # A whole-manifest hash remains provenance, not a reason to invalidate
    # unrelated entries added after a completed replay.
    frozen_path = work / "exact-units.toml"
    if not frozen_path.is_file() or digest(frozen_path) != receipt["manifest_sha256"]:
        raise ValueError("frozen replay unit manifest disagrees with its receipt")
    frozen_config = tomllib.loads(frozen_path.read_text())
    if frozen_config["artifact"] != context.artifact or frozen_config.get("target_view") != config.get("target_view"):
        raise ValueError("frozen replay artifact or decoded-view pin changed")
    frozen_entries = {entry["id"]: entry for entry in frozen_config["units"]}
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
    artifact, target, target_view = load_unit_target(context, config)
    if receipt["target_sha256"] != artifact["sha256"]:
        raise ValueError("replay target identity disagrees")
    if target_view is not None:
        if (receipt.get("artifact") != context.artifact or receipt.get("target_view") != target_view or
                load_unit_target(context, config, cache=work / "target-view")[2] != target_view):
            raise ValueError("saved decoded target comparison proof disagrees")
    results = {result["id"]: result for result in receipt["results"]}
    if not results or len(results) != len(receipt["results"]):
        raise ValueError("empty or duplicate replay result set")
    replay_entries = replay_entries_for_accept(entries, frozen_entries, results, units)
    if "selected_units" in receipt and (len(receipt["selected_units"]) != len(set(receipt["selected_units"])) or
                                       set(receipt["selected_units"]) != set(results)):
        raise ValueError("replay selected-unit set disagrees with its actual results")
    control = receipt["compiled_negative_control"]
    validate_control(control)
    if "negative_control" in receipt:
        negative = receipt["negative_control"]
        if negative["unit_id"] not in results:
            raise ValueError("negative control belongs to an unselected unit")
        control_entry = replay_entries[negative["unit_id"]]
        if negative["entry_sha256"] != entry_digest(control_entry):
            raise ValueError("negative-control unit configuration changed")
        if negative["control_sha256"] != entry_digest(negative["mutation"]):
            raise ValueError("negative-control mutation identity disagrees")
        if negative["comparison"] != control:
            raise ValueError("negative-control comparison records disagree")
    else:
        matches = [replay_entries[name] for name in results if replay_entries[name]["target_start"] == control["target_start"]
                   and replay_entries[name]["size"] == control["size"]]
        if len(matches) != 1:
            raise ValueError("legacy negative-control owner is ambiguous")
        control_entry = matches[0]
        mutations = [row for row in config.get("controls", []) if row["unit"] == control_entry["id"]]
        if len(mutations) != 1:
            raise ValueError("legacy compiled mutation needs one explicit review control")
        negative = {"unit_id": control_entry["id"], "producer_path": "negative/source",
                    "mutation": mutations[0], "comparison": control,
                    "legacy_source_revalidated": True}
    selected = select_accept_units(results, units, control_entry["id"])
    imported = []
    frozen_inputs = {item["path"]: item["sha256"] for item in receipt["source_inputs"]}
    for name, result in results.items():
        entry = replay_entries[name]
        if name not in frozen_entries or entry_digest(frozen_entries[name]) != entry_digest(entry):
            raise ValueError(f"replay entry changed: {name}")
        if result.get("entry_sha256", entry_digest(entry)) != entry_digest(entry):
            raise ValueError(f"replay result entry identity disagrees: {name}")
        validate_result(entry, result, require_exact=name in selected)
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
            if artifact_name != "main" or "binary" in entry:
                expected = compiler_arguments(entry, context.binary)
                recorded = json.loads((source / "compiler-arguments.json").read_text())
                if result.get("compiler_arguments") != [expected] * 2 or recorded.get(entry["module"]) != expected:
                    raise ValueError("saved actual compiler binary arguments disagree with the artifact context")
            candidate = parse_mz((source / "units.exe").read_bytes())
            if compare_mapped_unit(target, candidate, source / "units.map", entry) != result["rounds"][index]:
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
        classify_extent(entry, target_bytes=target.program_image[
            entry["target_start"]:entry["target_start"] + entry["size"]])
        if name in selected:
            imported.append({"id": name, "entry_sha256": entry_digest(entry), "result": result,
                             "source_inputs": snapshots, "toolchain_manifest_sha256": tool_sha,
                             "toolchain_receipt_sha256": receipt["toolchain_receipt_sha256"],
                             "replay_receipt_sha256": digest(receipt_path),
                             "compiled_negative_control": control, "negative_control": negative})
            if target_view is not None:
                imported[-1]["target_view"] = target_view
    negative_source = _saved_source(work, negative["producer_path"])
    if artifact_name != "main" or "binary" in control_entry:
        expected = compiler_arguments(control_entry, context.binary)
        recorded = json.loads((negative_source / "compiler-arguments.json").read_text())
        if negative.get("compiler_arguments") != expected or recorded.get(control_entry["module"]) != expected:
            raise ValueError("negative producer compiler binary arguments disagree")
    observed_control = mapped_control_comparison(target, parse_mz((negative_source / "units.exe").read_bytes()),
                                                 control_entry, negative_source / "units.map")
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
    aggregate_pass = validate_receipt_aggregate(receipt, results, observed_control)
    if units is None and not aggregate_pass:
        raise ValueError("default acceptance requires the complete replay aggregate to pass")
    for item in imported:
        item["receipt_aggregate_pass"] = aggregate_pass
        if units is not None:
            item["receipt_selected_subset"] = sorted(selected)
    acceptance_path = context.ledger
    previous = json.loads(acceptance_path.read_text()) if acceptance_path.exists() else {"units": []}
    acceptance = merge_acceptance(root, previous, imported, target_sha=artifact["sha256"],
                                  tool_sha=tool_sha, replay_sha=digest(receipt_path), control=control,
                                  artifact_name=artifact_name)
    if target_view is not None:
        acceptance.update(artifact=context.artifact, target_view=target_view,
                          scope="decoded load-module unit bytes and ordered fixups; packed file unaccepted")
    summarize(root, acceptance, artifact_name=artifact_name)
    temporary = acceptance_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(acceptance, indent=2) + "\n")
    temporary.replace(acceptance_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept", type=Path)
    parser.add_argument("--artifact", choices=("main", "op", "maine"), default="main")
    parser.add_argument("--units", nargs="+", metavar="ID", help="explicit exact subset of --accept receipt")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.units is not None and args.accept is None:
        parser.error("--units requires --accept")
    if args.accept:
        accept(args.accept, units=args.units, artifact_name=args.artifact)
    summary = summarize_all()
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

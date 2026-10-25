#!/usr/bin/env python3
"""Gapless target-coordinate ownership inventory; unknown is never excluded."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import tomllib

from lib.pc98 import digest_bytes
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_extents import unit_extent_kind
from progress import classify_extent, summarize_all

ROOT = Path(__file__).resolve().parents[1]


def partition(size: int, units: list[dict]) -> list[dict]:
    """Split only accepted whole extents and their explicit byte classifications."""
    if type(size) is not int or size <= 0:
        raise ValueError("ownership view must have a positive size")
    pieces = []
    cursor = 0
    for entry in sorted(units, key=lambda row: row["target_start"]):
        classify_extent(entry)
        start, end = entry["target_start"], entry["target_start"] + entry["size"]
        if type(start) is not int or start < cursor or end > size:
            raise ValueError("accepted ownership intervals overlap or exceed target bounds")
        if cursor < start:
            pieces.append({"start": cursor, "end": start, "kind": "unknown"})
        padding = set(entry.get("alignment_offsets", []))
        padding.update(row["offset"] for row in entry.get("padding_bytes", []))
        tables = [(row["offset"], row["offset"] + row["size"])
                  for row in entry.get("code_data_ranges", [])]
        boundaries = {0, entry["size"]}
        boundaries.update(value for offset in padding for value in (offset, offset + 1))
        boundaries.update(value for pair in tables for value in pair)
        points = sorted(boundaries)
        for left, right in zip(points, points[1:]):
            if left in padding:
                kind = "checked-uncredited-padding"
            elif any(low <= left < high for low, high in tables):
                kind = "accepted-cxx-switch-table"
            elif unit_extent_kind(entry) == 'initialized-data':
                kind = ('accepted-c-initialized-data'
                        if entry.get('origin') == 'compiler-generated-c-semantic-data'
                        else 'accepted-cxx-initialized-data')
            else:
                kind = "accepted-cxx-instructions"
            row = {"start": start + left, "end": start + right, "kind": kind, "unit": entry["id"]}
            if (pieces and pieces[-1]["end"] == row["start"] and
                    all(pieces[-1].get(key) == row.get(key) for key in ("kind", "unit"))):
                pieces[-1]["end"] = row["end"]
            else:
                pieces.append(row)
        cursor = end
    if cursor < size:
        pieces.append({"start": cursor, "end": size, "kind": "unknown"})
    validate_partition(size, pieces)
    return pieces


def validate_partition(size: int, pieces: list[dict]) -> None:
    cursor = 0
    for row in pieces:
        if (type(row["start"]) is not int or type(row["end"]) is not int or
                row["start"] != cursor or not cursor < row["end"] <= size):
            raise ValueError("ownership partition contains a gap, overlap or invalid bound")
        cursor = row["end"]
    if cursor != size:
        raise ValueError("ownership partition does not cover the entire observed view")


def overlay_vendor(size: int, pieces: list[dict], claims: list[dict]) -> list[dict]:
    """Replace only unknown ranges with complete, independently reviewed vendor claims."""
    validate_partition(size, pieces)
    known = [row for row in pieces if row["kind"] != "unknown"]
    for row in claims:
        if (row.get("kind") != "verified-vendor-code" or
                type(row.get("start")) is not int or type(row.get("end")) is not int or
                not 0 <= row["start"] < row["end"] <= size or not row.get("member")):
            raise ValueError("invalid complete vendor ownership claim")
    output = []
    cursor = 0
    for row in sorted(known + claims, key=lambda item: (item["start"], item["end"])):
        if row["start"] < cursor:
            raise ValueError("vendor claim overlaps accepted source or another ownership claim")
        if cursor < row["start"]:
            output.append({"start": cursor, "end": row["start"], "kind": "unknown"})
        output.append(dict(row))
        cursor = row["end"]
    if cursor < size:
        output.append({"start": cursor, "end": size, "kind": "unknown"})
    validate_partition(size, output)
    return output


def reviewed_vendor(root: Path, *, view: dict, verify_targets: bool) -> tuple[list[dict], str | None]:
    decision_path = root / "config/reviewed_vendor_units.json"
    if not decision_path.exists():
        return [], None
    from review_vendor import validate_metadata, review_inputs

    decision = json.loads(decision_path.read_text())
    proof_bytes = (root / "config/vendor_ownership.json").read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root)  # Public verifier/parser/toolchain identities, bounds and actions.
    if (decision.get("schema_version") != 1 or decision.get("artifact") != "th05-main" or
            decision.get("evidence_sha256") != digest_bytes(proof_bytes) or
            proof["target_payload_sha256"] != view["sha256"] or
            decision.get("classification") != "third-party-library-code"):
        raise ValueError("reviewed vendor decision is stale or belongs to a different target")
    selected = decision.get("members")
    if (not isinstance(selected, list) or not selected or
            any(not isinstance(name, str) or not name for name in selected) or
            len(selected) != len(set(selected))):
        raise ValueError("reviewed vendor decision requires unique explicit members")
    proposed = {row["member"]: row for row in proof["contributions"]}
    if any(name not in proposed for name in selected):
        raise ValueError("deferred or unverified vendor member cannot be excluded")
    if verify_targets and review_inputs(root) != proof:
        raise ValueError("native private vendor replay disagrees with reviewed evidence")
    claims = [{"start": proposed[name]["start"], "end": proposed[name]["end"],
               "kind": "verified-vendor-code", "library": proof["library"], "member": name}
              for name in selected]
    return claims, digest_bytes(decision_path.read_bytes())


def reviewed_master(root: Path, *, view: dict, verify_targets: bool) -> tuple[list[dict], str | None]:
    """Adopt only the twenty explicitly reviewed complete Master procedures."""
    decision_path = root / "config/reviewed_master_procedures.json"
    if not decision_path.exists():
        return [], None
    from review_master import validate_metadata, review_inputs

    decision_bytes = decision_path.read_bytes()
    decision = json.loads(decision_bytes)
    proof_bytes = (root / "config/master_vendor_ownership.json").read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root)
    if (type(decision.get("schema_version")) is not int or decision.get("schema_version") != 1 or
            decision.get("artifact") != "th05-main" or
            decision.get("decision") != "ADOPT_ONLY_LISTED_PROCEDURES" or
            decision.get("classification") != "third-party-library-code" or
            decision.get("evidence_sha256") != digest_bytes(proof_bytes) or
            decision.get("target_sha256") != proof["inputs"]["target"]["sha256"] or
            decision.get("target_payload_sha256") != proof["target_payload_sha256"] or
            proof["target_payload_sha256"] != view["sha256"]):
        raise ValueError("reviewed Master decision is stale or belongs to a different target/classification")
    if (type(decision.get("authored_credit")) is not int or decision["authored_credit"] != 0 or
            decision.get("other_procedures_policy") != "unknown" or
            decision.get("uncovered_gaps_policy") != "unknown" or
            "authored_denominator" not in decision or decision["authored_denominator"] is not None):
        raise ValueError("Master adoption cannot grant credit or classify other procedures/gaps")
    selected = decision.get("procedures")
    if (not isinstance(selected, list) or len(selected) != 20 or
            any(not isinstance(name, str) or not name for name in selected) or
            len(selected) != len(set(selected))):
        raise ValueError("reviewed Master decision requires twenty unique explicit procedures")
    proposed = {row["name"]: row for row in proof["procedures"]}
    if set(selected) != set(proposed):
        raise ValueError("unknown, deferred or unverified Master procedure cannot be classified")
    totals = {"full_bytes": sum(proposed[name]["size"] for name in selected),
              "instruction_bytes": sum(proposed[name]["instruction_bytes"] for name in selected),
              "padding_bytes": sum(len(proposed[name]["padding"]) for name in selected)}
    if any(decision.get(key) != value for key, value in totals.items()):
        raise ValueError("Master decision full/instruction/library-padding extents disagree")
    if verify_targets:
        result = review_inputs(proof, root=root)  # Actual private bytes/context replay, never a saved PASS.
        if not isinstance(result, dict) or not all(result.get(key) == value for key, value in {
                "kind": "native-master-procedure-review", "decision": "PROPOSAL",
                "byte_proof_replayed": True, "procedures": 20, "full_bytes": 376,
                "instruction_bytes": 367, "padding_bytes": 9, "authored_credit": 0,
                "denominator_changed": False}.items()):
            raise ValueError("native private Master replay disagrees with reviewed evidence")
    claims = [{"start": proposed[name]["start"], "end": proposed[name]["end"],
               "kind": "verified-vendor-code", "library": "master.lib 0.23", "member": name}
              for name in selected]
    return claims, digest_bytes(decision_bytes)


def reviewed_context_vendor(root: Path, *, context: str, view: dict,
                            verify_targets: bool) -> tuple[list[dict], str | None]:
    """Optional explicit OP/MAINE decisions; proposals alone classify nothing."""
    if context not in ("op", "maine"):
        raise ValueError("unsupported decoded vendor ownership context")
    decision_path = root / f"config/reviewed_vendor_units.{context}.json"
    if not decision_path.exists():
        return [], None
    from review_vendor_context import metadata_path, validate_metadata, review_inputs

    decision_bytes = decision_path.read_bytes()
    decision = json.loads(decision_bytes)
    proof_bytes = metadata_path(root, context).read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root, context=context)
    if (type(decision.get("schema_version")) is not int or decision["schema_version"] != 1 or
            decision.get("artifact") != "th05-" + context or
            decision.get("decision") != "ADOPT_ONLY_LISTED_MEMBERS" or
            decision.get("classification") != "third-party-library-code" or
            decision.get("evidence_sha256") != digest_bytes(proof_bytes) or
            decision.get("target_sha256") != proof["target_sha256"] or
            decision.get("target_payload_sha256") != proof["target_payload_sha256"] or
            (view.get("size"), view.get("sha256")) !=
            (proof["target_payload_size"], proof["target_payload_sha256"])):
        raise ValueError("decoded vendor decision belongs to another context or stale evidence")
    if (type(decision.get("authored_credit")) is not int or decision["authored_credit"] != 0 or
            decision.get("other_members_policy") != "unknown" or
            decision.get("uncovered_gaps_policy") != "unknown" or
            "authored_denominator" not in decision or decision["authored_denominator"] is not None):
        raise ValueError("decoded vendor decision cannot grant credit or classify other bytes")
    names = decision.get("members")
    if (not isinstance(names, list) or not names or
            any(not isinstance(name, str) or not name for name in names) or
            len(names) != len(set(names))):
        raise ValueError("decoded vendor decision requires unique explicit members")
    proposed = {row["member"]: row for row in proof["contributions"]}
    if any(name not in proposed for name in names):
        raise ValueError("unknown/deferred vendor member cannot be classified")
    if verify_targets and review_inputs(root, context=context) != proof:
        raise ValueError("decoded vendor private replay disagrees with reviewed evidence")
    claims = [{"start": proposed[name]["start"], "end": proposed[name]["end"],
               "kind": "verified-vendor-code", "library": proof["library"], "member": name}
              for name in names]
    return claims, digest_bytes(decision_bytes)


def inventory(root: Path = ROOT, *, verify_targets: bool = False) -> dict:
    summary = summarize_all(root)  # Includes current sources, ledgers and public decoded proofs.
    config = tomllib.loads((root / "config/ownership.toml").read_text())
    if config["schema_version"] != 1 or set(config["views"]) != {"main", "op", "maine", "zun"}:
        raise ValueError("ownership inventory requires all four independent coordinate views")
    targets = tomllib.loads((root / "config/targets.toml").read_text())
    target_by_id = {row["id"]: row for row in targets["artifacts"]}
    views = {}
    for name, view in config["views"].items():
        target = target_by_id["th05-" + name]
        entries = []
        if name != "zun":
            context = UnitContext(root, name)
            ledger = json.loads(context.ledger.read_text())
            live = {row["id"]: row for row in context.config()["units"]}
            entries = [live[row["id"]] for row in ledger["units"]]
            if name != "main":
                proof = ledger["target_view"]
                if (proof["payload_size"], proof["payload_sha256"]) != (view["size"], view["sha256"]):
                    raise ValueError("ownership view differs from verified decoded evidence")
            if verify_targets:
                _, image, _ = load_unit_target(context, context.config())
                if (len(image.program_image), digest_bytes(image.program_image)) != (view["size"], view["sha256"]):
                    raise ValueError("ownership view differs from actual target bytes")
        elif (view["size"], view["sha256"]) != (target["size"], target["sha256"]):
            raise ValueError("ZUN coordinates must cover the original COM, without double counting children")
        pieces = partition(view["size"], entries)
        review_sha = master_review_sha = None
        if name == "main":
            claims, review_sha = reviewed_vendor(root, view=view, verify_targets=verify_targets)
            master_claims, master_review_sha = reviewed_master(root, view=view, verify_targets=verify_targets)
            pieces = overlay_vendor(view["size"], pieces, claims + master_claims)
        elif name in ("op", "maine"):
            claims, review_sha = reviewed_context_vendor(root, context=name, view=view,
                                                         verify_targets=verify_targets)
            pieces = overlay_vendor(view["size"], pieces, claims)
        counts = Counter()
        for row in pieces:
            counts[row["kind"]] += row["end"] - row["start"]
        views[name] = {**view, "original_sha256": target["sha256"],
                       "byte_counts": dict(sorted(counts.items())), "intervals": pieces}
        if review_sha:
            views[name]["vendor_review_sha256"] = review_sha
        if master_review_sha:
            views[name]["master_vendor_review_sha256"] = master_review_sha
    counts = Counter()
    for view in views.values():
        counts.update(view["byte_counts"])
    if (counts["accepted-cxx-instructions"] != summary["instruction_bytes"] or
            counts["accepted-cxx-switch-table"] != summary["code_data_bytes"] or
            counts['accepted-cxx-initialized-data'] + counts['accepted-c-initialized-data'] !=
            summary.get('authored_data_bytes', 0) or
            counts["checked-uncredited-padding"] != summary["padding_bytes"]):
        raise ValueError("ownership partition disagrees with accepted source progress")
    return {"schema_version": 1, "kind": "gapless-observed-coordinate-inventory",
            "authored_denominator": None, "percentage": None,
            "unknown_policy": "retain every unknown interval; only explicitly reviewed complete vendor contributions are classified; no inferred asset, runtime or ASM exclusion",
            "observed_bytes": sum(row["size"] for row in views.values()),
            "byte_counts": dict(sorted(counts.items())), "views": views}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--verify-targets", action="store_true", help="rehash private cached targets; never decode/recompile")
    args = parser.parse_args()
    result = inventory(verify_targets=args.verify_targets)
    rendered = json.dumps(result, indent=2) + "\n"
    destination = ROOT / "resources/ownership.json"
    if args.write:
        destination.write_text(rendered)
    elif not destination.exists() or destination.read_text() != rendered:
        raise SystemExit("ownership inventory is stale; run scripts/ownership.py --write")
    print(json.dumps({key: result[key] for key in ("observed_bytes", "byte_counts", "authored_denominator")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

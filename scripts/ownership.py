#!/usr/bin/env python3
"""Gapless target-coordinate ownership inventory; unknown is never excluded."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import tomllib

from lib.pc98 import digest_bytes
from lib.tiny_com import UnitContext, load_unit_target
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
        if (row.get("kind") not in ("verified-vendor-code", "verified-vendor-initialized-data") or
                type(row.get("start")) is not int or type(row.get("end")) is not int or
                not 0 <= row["start"] < row["end"] <= size or not row.get("member")):
            raise ValueError("invalid complete vendor ownership claim")
        if row["kind"] == "verified-vendor-initialized-data":
            if (row.get("content_kind") != "library-initialized-data" or
                    type(row.get("instruction_bytes", 0)) is not int or row.get("instruction_bytes", 0) != 0):
                raise ValueError("initialized vendor DATA requires its exact content kind and zero instructions")
        elif row.get("content_kind") == "library-initialized-data":
            raise ValueError("initialized vendor DATA cannot use the vendor CODE kind")
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


def overlay_asm(size: int, pieces: list[dict], claims: list[dict]) -> list[dict]:
    """Adopt reviewed ASM only where ownership was previously unknown."""
    validate_partition(size, pieces)
    allowed = {"accepted-reviewed-asm-instructions", "accepted-reviewed-asm-initialized-data",
               "accepted-reviewed-asm-dispatch-table", "accepted-reviewed-asm-semantic-code-table",
               "checked-uncredited-asm-inert-branch",
               "checked-uncredited-asm-alignment", "checked-uncredited-asm-runtime-placeholder"}
    for row in claims:
        if (row.get("kind") not in allowed or not row.get("unit")
                or row.get("origin") != "reviewed-native-handwritten-assembly-reconstruction"
                or type(row.get("start")) is not int or type(row.get("end")) is not int
                or not 0 <= row["start"] < row["end"] <= size):
            raise ValueError("invalid reviewed ASM ownership claim")
    known = [row for row in pieces if row["kind"] != "unknown"]
    output, cursor = [], 0
    for row in sorted(known + claims, key=lambda item: (item["start"], item["end"])):
        if row["start"] < cursor:
            raise ValueError("reviewed ASM claim overlaps previously known ownership")
        if cursor < row["start"]:
            output.append({"start": cursor, "end": row["start"], "kind": "unknown"})
        output.append(dict(row))
        cursor = row["end"]
    if cursor < size:
        output.append({"start": cursor, "end": size, "kind": "unknown"})
    validate_partition(size, output)
    return output


def overlay_resources(size: int, pieces: list[dict], claims: list[dict]) -> list[dict]:
    """Classify reviewed bitmap resources only within still-unknown bytes."""
    validate_partition(size, pieces)
    sprite_sizes = {"main-sprite-pointnum": 1536, "main-sprite-pellet": 128,
                    "main-sprite-pellet-bottom": 64, "main-sprite-sparks": 1024}
    for row in claims:
        font = (row.get("kind") == "reviewed-embedded-font-bitmap" and
                row.get("model") == "th05-zun-cg-256-glyphs-16x16-1bpp" and
                row.get("end", 0) - row.get("start", 0) == 8192)
        sprite = (row.get("kind") == "reviewed-embedded-sprite-bitmap" and
                  row.get("model") == "th05-main-bmp2arr-8px-1bpp-preshifted" and
                  row.get("resource") in sprite_sizes and
                  row.get("end", 0) - row.get("start", 0) ==
                  sprite_sizes.get(row.get("resource")))
        if (not (font or sprite) or not row.get("resource")
                or type(row.get("authored_credit")) is not int or row["authored_credit"] != 0
                or type(row.get("instruction_bytes")) is not int or row["instruction_bytes"] != 0
                or type(row.get("start")) is not int or type(row.get("end")) is not int
                or not 0 <= row["start"] < row["end"] <= size):
            raise ValueError("invalid zero-credit resource claim")
    rows = [row for row in pieces if row["kind"] != "unknown"] + claims
    output, cursor = [], 0
    for row in sorted(rows, key=lambda item: (item["start"], item["end"])):
        if row["start"] < cursor:
            raise ValueError("resource claim overlaps existing ownership")
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


def reviewed_master_additions(root: Path, *, views: dict, targets: dict,
                              verify_targets: bool) -> tuple[dict[str, list[dict]], str | None]:
    """One explicit cross-artifact decision; replay its private evidence once."""
    decision_path = root / "config/reviewed_master_additions.json"
    if not decision_path.exists():
        return {}, None
    from review_master_additions import BASE_PROOF, PROOF, validate_metadata, review_inputs

    decision_bytes = decision_path.read_bytes()
    decision = json.loads(decision_bytes)
    proof_bytes = (root / PROOF).read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root)
    baseline = json.loads((root / BASE_PROOF).read_bytes())
    if (type(decision.get("schema_version")) is not int or decision["schema_version"] != 1 or
            decision.get("decision") != "ADOPT_ONLY_LISTED_SCOPES" or
            decision.get("classification") != "third-party-library-code" or
            decision.get("evidence_sha256") != digest_bytes(proof_bytes)):
        raise ValueError("Master additions decision is stale or has another classification")
    if (type(decision.get("authored_credit")) is not int or decision["authored_credit"] != 0 or
            "authored_denominator" not in decision or decision["authored_denominator"] is not None or
            decision.get("other_scopes_policy") != "unknown" or
            decision.get("uncovered_gaps_policy") != "unknown"):
        raise ValueError("Master additions cannot grant authored credit or classify other scopes/gaps")
    proposed = {row["id"]: row for row in proof["scopes"]}
    selected = decision.get("scopes")
    if (not isinstance(selected, list) or len(selected) != 7 or
            any(not isinstance(scope, str) or not scope for scope in selected) or
            len(selected) != len(set(selected)) or set(selected) != set(proposed)):
        raise ValueError("Master additions require the exact seven unique reviewed scope IDs")
    for key in ("full_bytes", "instruction_bytes", "library_padding_bytes", "library_code_data_bytes"):
        if type(decision.get(key)) is not int or decision[key] != proof[key]:
            raise ValueError("Master additions instruction/data/library-padding accounting differs")
    artifacts = decision.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != {"main", "op", "maine"}:
        raise ValueError("Master additions require all three actual artifact contexts")
    for name in ("main", "op", "maine"):
        packed = (baseline["inputs"]["target"]["sha256"] if name == "main"
                  else proof["table_contexts"][name]["target_sha256"])
        payload = (baseline["target_payload_sha256"] if name == "main"
                   else proof["table_contexts"][name]["target_payload_sha256"])
        row = artifacts[name]
        if (not isinstance(row, dict) or row.get("artifact") != "th05-" + name or
                row.get("target_sha256") != packed or
                targets.get("th05-" + name, {}).get("sha256") != packed or
                row.get("target_payload_sha256") != payload or
                views.get(name, {}).get("sha256") != payload or
                type(row.get("target_payload_size")) is not int or
                row["target_payload_size"] != views.get(name, {}).get("size") or
                row["target_payload_size"] <= 0):
            raise ValueError("Master additions packed/payload identity belongs to another artifact/context")
        if (name != "main" and row["target_payload_size"] !=
                proof["table_contexts"][name]["target_view"]["payload_size"]):
            raise ValueError("Master additions decoded context size differs")
    if verify_targets:
        expected = dict(kind="native-source-backed-master-additions-review", scopes=7,
                        full_bytes=2152, instruction_bytes=103, library_padding_bytes=1,
                        library_code_data_bytes=2048, byte_proof_replayed=True, decision="PROPOSAL",
                        authored_credit=0, compiler_invocations=0, authored_denominator=None)
        if review_inputs(proof, root=root) != expected:
            raise ValueError("Master additions actual private replay disagrees with reviewed proof")
    claims = {name: [] for name in artifacts}
    for scope in selected:
        row = proposed[scope]
        name = row["artifact"].removeprefix("th05-")
        claims[name].append({"start": row["start"], "end": row["end"],
                            "kind": "verified-vendor-code", "content_kind": row["content_kind"],
                            "library": "master.lib 0.23", "member": row["name"], "scope_id": scope})
    return claims, digest_bytes(decision_bytes)


def reviewed_master_sin8(root: Path, *, views: dict, targets: dict,
                         verify_targets: bool) -> tuple[dict[str, list[dict]], str | None]:
    """Adopt exactly the three source-backed DATA scopes, with one native replay."""
    path = root / "config/reviewed_master_sin8.json"
    if not path.exists():
        return {}, None
    from review_master_sin8 import PROOF, validate_metadata, review_inputs

    decision_bytes = path.read_bytes()
    decision = json.loads(decision_bytes)
    proof_bytes = (root / PROOF).read_bytes()
    proof = json.loads(proof_bytes)
    validate_metadata(proof, root=root)
    if (type(decision.get("schema_version")) is not int or decision["schema_version"] != 1 or
            decision.get("decision") != "ADOPT_ONLY_LISTED_INITIALIZED_DATA" or
            decision.get("classification") != "third-party-library-initialized-data" or
            decision.get("claim_kind") != "verified-vendor-initialized-data" or
            decision.get("evidence_sha256") != digest_bytes(proof_bytes)):
        raise ValueError("SIN8 initialized DATA decision is stale or has another kind/classification")
    if (type(decision.get("authored_credit")) is not int or decision["authored_credit"] != 0 or
            "authored_denominator" not in decision or decision["authored_denominator"] is not None or
            decision.get("other_scopes_policy") != "unknown" or decision.get("uncovered_gaps_policy") != "unknown" or
            type(decision.get("instruction_bytes")) is not int or decision["instruction_bytes"] != 0 or
            type(decision.get("full_bytes")) is not int or decision["full_bytes"] != 1920):
        raise ValueError("SIN8 DATA adoption cannot grant instruction/authored credit or classify other gaps")
    proposed = {row["id"]: row for row in proof["scopes"]}
    selected = decision.get("scopes")
    if (not isinstance(selected, list) or len(selected) != 3 or
            any(not isinstance(scope, str) or not scope for scope in selected) or
            len(selected) != len(set(selected)) or set(selected) != set(proposed)):
        raise ValueError("SIN8 requires exactly three unique reviewed initialized DATA scope IDs")
    artifacts = decision.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != {"main", "op", "maine"}:
        raise ValueError("SIN8 decision requires all three real artifact contexts")
    for scope in proof["scopes"]:
        name = scope["artifact"].removeprefix("th05-")
        row = artifacts[name]
        if (not isinstance(row, dict) or row.get("artifact") != scope["artifact"] or
                row.get("target_sha256") != scope["original_packed_sha256"] or
                targets.get(scope["artifact"], {}).get("sha256") != scope["original_packed_sha256"] or
                row.get("target_payload_sha256") != scope["target_payload_sha256"] or
                views.get(name, {}).get("sha256") != scope["target_payload_sha256"] or
                type(row.get("target_payload_size")) is not int or row["target_payload_size"] <= 0 or
                row["target_payload_size"] != views.get(name, {}).get("size") or
                (scope["target_view"] is not None and row["target_payload_size"] != scope["target_view"]["payload_size"])):
            raise ValueError("SIN8 decision has stale packed/payload identity or wrong artifact/context")
    if verify_targets:
        expected = dict(kind="native-SIN8-initialized-data-review", scopes=3, full_bytes=1920,
                        instruction_bytes=0, byte_proof_replayed=True, decision="PROPOSAL",
                        authored_credit=0, compiler_invocations=0, authored_denominator=None)
        if review_inputs(proof, root=root) != expected:
            raise ValueError("SIN8 actual initialized DATA input replay disagrees with reviewed proof")
    claims = {name: [] for name in artifacts}
    for scope_id in selected:
        scope = proposed[scope_id]
        claims[scope["artifact"].removeprefix("th05-")].append({
            "start": scope["original_start"], "end": scope["original_end"],
            "kind": "verified-vendor-initialized-data", "content_kind": "library-initialized-data",
            "instruction_bytes": 0, "library": "master.lib 0.23", "member": "SIN8", "scope_id": scope_id})
    return claims, digest_bytes(decision_bytes)


def inventory(root: Path = ROOT, *, verify_targets: bool = False) -> dict:
    summary = summarize_all(root)  # Includes current sources, ledgers and public decoded proofs.
    config = tomllib.loads((root / "config/ownership.toml").read_text())
    if config["schema_version"] != 1 or set(config["views"]) != {"main", "op", "maine", "zun"}:
        raise ValueError("ownership inventory requires all four independent coordinate views")
    targets = tomllib.loads((root / "config/targets.toml").read_text())
    target_by_id = {row["id"]: row for row in targets["artifacts"]}
    additions, additions_sha = reviewed_master_additions(
        root, views=config["views"], targets=target_by_id, verify_targets=verify_targets)
    sin8, sin8_sha = reviewed_master_sin8(
        root, views=config["views"], targets=target_by_id, verify_targets=verify_targets)
    from review_vendor_data import reviewed_claims
    cl_data, cl_data_sha = reviewed_claims(root, config["views"], verify_targets=verify_targets)
    from review_text_fx_asm import reviewed_claims as reviewed_asm_claims
    asm, asm_sha = reviewed_asm_claims(root, config["views"], verify_targets=verify_targets)
    from replay_enemy_vm import reviewed_claims as reviewed_enemy_vm_claims
    enemy_vm, enemy_vm_sha = reviewed_enemy_vm_claims(root, config["views"], verify_targets=verify_targets)
    from replay_asm_family import reviewed_claims as reviewed_generic_asm
    generic_asm, generic_asm_sha = reviewed_generic_asm(root, config["views"], verify_targets=verify_targets)
    from review_font_resource import reviewed_claims as reviewed_font_resources
    fonts, fonts_sha = reviewed_font_resources(root, config["views"], verify_targets=verify_targets)
    from review_main_runtime import reviewed_claims as reviewed_runtime
    runtime, runtime_sha = reviewed_runtime(root, config["views"], verify_targets=verify_targets)
    from review_string_runtime import reviewed_claims as reviewed_strings
    strings, strings_sha = reviewed_strings(root, config["views"], verify_targets=verify_targets)
    from review_master_egc_shifts import reviewed_claims as reviewed_egc_shifts
    egc_shifts, egc_shifts_sha = reviewed_egc_shifts(root, config["views"], verify_targets=verify_targets)
    from review_master_ems_transfers import reviewed_claims as reviewed_ems_transfers
    ems_transfers, ems_transfers_sha = reviewed_ems_transfers(root, config["views"], verify_targets=verify_targets)
    from review_master_primary_circlefill import reviewed_claims as reviewed_primary_circlefill
    primary_circlefill, primary_circlefill_sha = reviewed_primary_circlefill(root, config["views"], verify_targets=verify_targets)
    from review_master_primary_circlex import reviewed_claims as reviewed_primary_circlex
    primary_circlex, primary_circlex_sha = reviewed_primary_circlex(root, config["views"], verify_targets=verify_targets)
    views = {}
    for name, view in config["views"].items():
        target = target_by_id["th05-" + name]
        entries = []
        if name == "zun" and (view["size"], view["sha256"]) != (target["size"], target["sha256"]):
            raise ValueError("ZUN coordinates must cover the original COM, without double counting children")
        if name != "zun" or UnitContext(root, name).ledger.exists():
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
        pieces = partition(view["size"], entries)
        review_sha = master_review_sha = None
        if name == "main":
            claims, review_sha = reviewed_vendor(root, view=view, verify_targets=verify_targets)
            master_claims, master_review_sha = reviewed_master(root, view=view, verify_targets=verify_targets)
            # These two large CL.LIB CODE members have real original OMF
            # source writes, but contain eight unwritten runtime CS: slots.
            # Only the 2040 bytes emitted by LEDATA/LIDATA are owned; the
            # reserved variables remain unknown, never implicit zero credit.
            from review_vendor_reserved import reviewed_claims as reviewed_reserved_vendor
            reserved_claims, reserved_review_sha = reviewed_reserved_vendor(
                root, view=view, verify_targets=verify_targets)
            # setenvp's original four DATA-group offsets differ from the
            # calibration's by 12h, but all ten genuine OMF CODE fixups resolve.
            from review_main_setenvp import reviewed_claims as reviewed_setenvp
            env_claims, env_review_sha = reviewed_setenvp(
                root, view=view, verify_targets=verify_targets)
            # The original C0L CRT also supplies exactly 144 initialized DATA
            # bytes, including its genuine _BSSEND linker word. These are
            # vendor DATA, not executable bytes or guessed zero-filled BSS.
            from review_main_c0_data import reviewed_claims as reviewed_c0_data
            c0_data_claims, c0_data_review_sha = reviewed_c0_data(
                root, view=view, verify_targets=verify_targets)
            # Five further actual MAIN CL.LIB CODE objects bind against
            # the independently observed original DGROUP/BSS/string frames.
            from review_main_shifted_vendor import reviewed_claims as shifted_main_claims
            shifted_main, shifted_main_sha = shifted_main_claims(
                root, view=view, verify_targets=verify_targets)
            # Eight full native Master SUPER graphics procedures are linked
            # from original symbolic ASM and the actual TASM OMF. Their DATA
            # fixup shift comes from the original C0L/CRT layout, not bytes.
            from review_master_super import reviewed_claims as master_super_claims
            super_claims, super_review_sha = master_super_claims(
                root, view=view, verify_targets=verify_targets)
            # The original PROC/ENDP source also proves separate rectangle
            # renderers, SUPERPUT dispatchers and complete auxiliary routines.
            from review_master_super_helpers import reviewed_claims as super_helper_claims
            super_helper_ranges, super_helper_sha = super_helper_claims(
                root, view=view, verify_targets=verify_targets)
            # Nine complete original Master music-driver procedures, including
            # BGM_INIT and BGM_PLAY, also link through genuine near/segment
            # OMF fixups and the native CRT layout, not copied target code.
            from review_master_bgm import reviewed_claims as master_bgm_claims
            bgm_claims, bgm_review_sha = master_bgm_claims(
                root, view=view, verify_targets=verify_targets)
            # Large Master GRCG clipping and primitive line/polygon drawing
            # are proven from original ASM plus complete OMF FIXUPP contexts.
            from review_master_grcg import reviewed_claims as master_grcg_claims
            grcg_claims, grcg_review_sha = master_grcg_claims(
                root, view=view, verify_targets=verify_targets)
            # Complete original Master file/DOS/heap procedures are source-
            # exact under the genuine _TEXT/DGROUP and ordered OMF fixups.
            from review_master_io import reviewed_claims as master_io_claims
            io_claims, io_review_sha = master_io_claims(
                root, view=view, verify_targets=verify_targets)
            pieces = overlay_vendor(view["size"], pieces,
                                    claims + master_claims + reserved_claims + env_claims +
                                    c0_data_claims + shifted_main + super_claims +
                                    super_helper_ranges + bgm_claims + grcg_claims + io_claims)
            pieces = overlay_vendor(view["size"], pieces, runtime)
            pieces = overlay_vendor(view["size"], pieces, strings)
            pieces = overlay_vendor(view["size"], pieces, egc_shifts)
            pieces = overlay_vendor(view["size"], pieces, ems_transfers)
            pieces = overlay_vendor(view["size"], pieces, primary_circlefill)
            pieces = overlay_vendor(view["size"], pieces, primary_circlex)
        elif name in ("op", "maine"):
            claims, review_sha = reviewed_context_vendor(root, context=name, view=view,
                                                         verify_targets=verify_targets)
            # Two original CL.LIB CODE members per decoded artifact contain
            # actual source LIDATA and small runtime-write CS: state slots.
            # Adopt only the 2040 source-written bytes; the 8-byte holes
            # remain original unknown bytes, with no invented code.
            from review_context_reserved import reviewed_claims as context_reserved_claims
            context_reserved, context_reserved_sha = context_reserved_claims(
                root, name, view=view, verify_targets=verify_targets)
            # Original CL.LIB xxas/signal/setenvp CODE also resolves completely
            # once OMF group targets and TLINK far-JMPs use the real link frames.
            from review_context_remaining import reviewed_claims as remaining_context_claims
            remaining_context, remaining_context_sha = remaining_context_claims(
                root, name, view=view, verify_targets=verify_targets)
            if name == "maine":
                # Real MAINE string-entry and DGROUP link shifts explain
                # five more original CL.LIB CODE member contributions.
                from review_maine_shifted_vendor import reviewed_claims as maine_shifted_claims
                shifted_context, shifted_context_sha = maine_shifted_claims(
                    root, view=view, verify_targets=verify_targets)
            else:
                shifted_context, shifted_context_sha = [], None
            # The original six Borland string class CODE contributions
            # are source-complete; OP's previously reviewed _TEXT set is
            # not re-adopted. MAINE's _TEXTC starts six bytes later.
            from review_context_string_runtime import reviewed_claims as string_context_claims
            string_context, string_context_sha = string_context_claims(
                root, name, view=view, verify_targets=verify_targets)
            # Original 1512-byte GRAPH_PI_LOAD_PACK in each executable is
            # linked from the actual TASM OMF and independent Master source.
            from review_context_pi_pack import reviewed_claims as pi_pack_claims
            pi_pack, pi_pack_review_sha = pi_pack_claims(
                root, name, view=view, verify_targets=verify_targets)
            # Real OMF _TEXT and DGROUP contributions recover eleven further
            # full, large Master procedures from the independent author ASM.
            from review_context_master_large import reviewed_claims as large_master_claims
            large_master, large_master_sha = large_master_claims(
                root, name, view=view, verify_targets=verify_targets)
            pieces = overlay_vendor(view["size"], pieces,
                                    claims + context_reserved + remaining_context +
                                    shifted_context + string_context + pi_pack + large_master)
        elif name == "zun":
            # Borland C0T.OBJ contributes two actual CODE LEDATAs and one
            # initialized DATA LEDATA. Leave its original two-byte writable
            # CS: slot outside the vendor CODE claims; BSS/_INIT_ are foreign.
            from replay_zun_crt import reviewed_claims as reviewed_zun_crt
            crt_claims, crt_review_sha = reviewed_zun_crt(
                root, view=view, verify_targets=verify_targets)
            pieces = overlay_vendor(view["size"], pieces, crt_claims)
        if name in additions:
            pieces = overlay_vendor(view["size"], pieces, additions[name])
        if name in sin8:
            pieces = overlay_vendor(view["size"], pieces, sin8[name])
        if name in cl_data:
            pieces = overlay_vendor(view["size"], pieces, cl_data[name])
        if name in asm:
            pieces = overlay_asm(view["size"], pieces, asm[name])
        if name in enemy_vm:
            pieces = overlay_asm(view["size"], pieces, enemy_vm[name])
        if name in generic_asm:
            pieces = overlay_asm(view["size"], pieces, generic_asm[name])
        if name == 'op':
            # OP's twelve musical key-top masks are semantic CODE data,
            # not twelve decoded CPU instructions or an external sprite.
            from replay_piano_top import reviewed_claims as piano_top_claims
            pieces = overlay_asm(view['size'], pieces, piano_top_claims(root, view))
        if name in fonts:
            pieces = overlay_resources(view["size"], pieces, fonts[name])
        if name == "main":
            # Independently reproduced TH02/TH04 BMP-derived sprite tables;
            # original MAIN's order differs from the native calibration.
            from review_main_sprites import reviewed_claims as main_sprite_claims
            sprites, sprite_review_sha = main_sprite_claims(
                root, view, verify_targets=verify_targets)
            pieces = overlay_resources(view["size"], pieces, sprites)
        counts = Counter()
        for row in pieces:
            counts[row["kind"]] += row["end"] - row["start"]
        views[name] = {**view, "original_sha256": target["sha256"],
                       "byte_counts": dict(sorted(counts.items())), "intervals": pieces}
        if review_sha:
            views[name]["vendor_review_sha256"] = review_sha
        if name in ("op", "maine") and context_reserved_sha:
            views[name]["reserved_vendor_review_sha256"] = context_reserved_sha
        if name in ("op", "maine") and remaining_context_sha:
            views[name]["remaining_vendor_review_sha256"] = remaining_context_sha
        if name == "maine" and shifted_context_sha:
            views[name]["shifted_vendor_review_sha256"] = shifted_context_sha
        if name in ("op","maine") and string_context_sha:
            views[name]["string_vendor_review_sha256"] = string_context_sha
        if name in ("op","maine") and pi_pack_review_sha:
            views[name]["master_pi_loader_review_sha256"] = pi_pack_review_sha
        if name in ("op","maine") and large_master_sha:
            views[name]["master_large_review_sha256"] = large_master_sha
        if name == "zun" and crt_review_sha:
            views[name]["zun_crt_review_sha256"] = crt_review_sha
        if name == "main" and reserved_review_sha:
            views[name]["reserved_vendor_review_sha256"] = reserved_review_sha
        if name == "main" and env_review_sha:
            views[name]["setenvp_vendor_review_sha256"] = env_review_sha
        if name == "main" and shifted_main_sha:
            views[name]["shifted_vendor_review_sha256"] = shifted_main_sha
        if name == "main" and super_review_sha:
            views[name]["master_super_review_sha256"] = super_review_sha
        if name == "main" and super_helper_sha:
            views[name]["master_super_helpers_review_sha256"] = super_helper_sha
        if name == "main" and bgm_review_sha:
            views[name]["master_bgm_review_sha256"] = bgm_review_sha
        if name == "main" and grcg_review_sha:
            views[name]["master_grcg_review_sha256"] = grcg_review_sha
        if name == "main" and io_review_sha:
            views[name]["master_io_review_sha256"] = io_review_sha
        if name == "main" and c0_data_review_sha:
            views[name]["c0_vendor_data_review_sha256"] = c0_data_review_sha
        if runtime_sha and name == "main":
            views[name]["runtime_vendor_review_sha256"] = runtime_sha
        if strings_sha and name == "main":
            views[name]["string_runtime_review_sha256"] = strings_sha
        if master_review_sha:
            views[name]["master_vendor_review_sha256"] = master_review_sha
        if egc_shifts_sha and name == "main":
            views[name]["master_egc_shifts_review_sha256"] = egc_shifts_sha
        if ems_transfers_sha and name == "main":
            views[name]["master_ems_transfers_review_sha256"] = ems_transfers_sha
        if primary_circlefill_sha and name == "main":
            views[name]["master_primary_circlefill_review_sha256"] = primary_circlefill_sha
        if primary_circlex_sha and name == "main":
            views[name]["master_primary_circlex_review_sha256"] = primary_circlex_sha
        if additions_sha and name in additions:
            views[name]["master_additions_review_sha256"] = additions_sha
        if sin8_sha and name in sin8:
            views[name]["master_sin8_review_sha256"] = sin8_sha
        if cl_data_sha and name in cl_data:
            views[name]["cl_data_review_sha256"] = cl_data_sha
        if asm_sha and name in asm:
            views[name]["text_fx_asm_review_sha256"] = asm_sha
        if enemy_vm_sha and name in enemy_vm:
            views[name]["enemy_vm_asm_review_sha256"] = enemy_vm_sha
        if generic_asm_sha and name in generic_asm:
            views[name]["asm_family_review_sha256"] = generic_asm_sha
        if fonts_sha and name in fonts:
            views[name]["font_resource_review_sha256"] = fonts_sha
        if name == "main" and sprite_review_sha:
            views[name]["sprite_resource_review_sha256"] = sprite_review_sha
    counts = Counter()
    for view in views.values():
        counts.update(view["byte_counts"])
    if (counts["accepted-cxx-instructions"] != summary["instruction_bytes"] or
            counts["accepted-cxx-switch-table"] != summary["code_data_bytes"] or
            counts['accepted-cxx-initialized-data'] + counts['accepted-c-initialized-data'] !=
            summary.get('authored_data_bytes', 0) or
            counts["checked-uncredited-padding"] != summary["padding_bytes"] or
            counts["accepted-reviewed-asm-instructions"] != summary.get("reviewed_asm_code_bytes", 0) or
            counts["accepted-reviewed-asm-dispatch-table"] != summary.get("reviewed_asm_table_bytes", 0) or
            counts["accepted-reviewed-asm-semantic-code-table"] != summary.get("reviewed_asm_semantic_table_bytes", 0) or
            counts["accepted-reviewed-asm-initialized-data"] != summary.get("reviewed_asm_data_bytes", 0) or
            sum(counts[k] for k in ("checked-uncredited-asm-alignment", "checked-uncredited-asm-inert-branch",
                                   "checked-uncredited-asm-runtime-placeholder")) != summary.get("reviewed_asm_uncredited_bytes", 0)):
        raise ValueError("ownership partition disagrees with accepted source progress")
    return {"schema_version": 1, "kind": "gapless-observed-coordinate-inventory",
            "authored_denominator": None, "percentage": None,
            "unknown_policy": "retain every unknown interval; source/vendor/resource classification requires explicit complete-scope review; reviewed bitmap resources have zero authored credit; no inferred asset or runtime exclusion; reviewed ASM remains separate",
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

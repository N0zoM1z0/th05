#!/usr/bin/env python3
"""Adopt only explicitly reviewed text-renderer assembly ownership extents."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib

import replay_text_fx_data as data
import replay_text_fx_render as render
from lib.borland_library import library_members
from lib.pc98 import digest_file, digest_bytes

ROOT = data.ROOT
PROOF = "config/text_fx_asm_ownership.json"
DECISION = "config/reviewed_text_fx_asm_units.json"
LIBRARY = "_reference/ReC98/bin/masters.lib"
LIBRARY_SHA = "6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6"
LIMITS = ["candidate-local-attested targets; pristine provenance not independently proved",
          "semantic reconstruction; literal historical source and original assembler not recovered",
          "bounded vendor exclusion covers only the pinned masters.lib, not all historical derivations",
          "no ownership transfer to ZUN, compiler-generated code, raster resources or unknown spans",
          "global authored denominator and percentage remain unreviewed"]


def configurations():
    return tomllib.loads(render.CONFIG.read_text()), tomllib.loads(data.CONFIG.read_text())


def review_inputs() -> list[dict]:
    paths = {"scripts/review_text_fx_asm.py", "scripts/lib/borland_library.py",
             "docs/reconstruction/TEXT_FX_ASM_OWNERSHIP.md", str(render.PUBLIC.relative_to(ROOT))}
    rc, dc = configurations()
    paths.update(row["path"] for row in render.snapshots(rc, dc))
    return [{"path": path, "sha256": digest_file(ROOT / path)} for path in sorted(paths)]


def units() -> list[dict]:
    rc, dc = configurations()
    result = []
    render_record = json.loads(render.PUBLIC.read_text())
    data_record = json.loads(data.PUBLIC.read_text())
    render.check_public(render_record, rc, dc)
    for name, profile in dc["profiles"].items():
        for scope, size in (("code", 346), ("dispatch", 28), ("state", 4)):
            comparison = (render_record["profiles"][name]["rounds"][0]["comparison"] if scope == "code"
                          else data_record["profiles"][name]["rounds"][0]["comparisons"][scope])
            start = profile[scope + "_start"]
            result.append({"id": f"{name}-text-fx-{scope}", "context": name, "scope": scope,
                           "start": start, "end": start + size, "sha256": comparison["target_sha256"],
                           "authored_asm_bytes": 339 if scope == "code" else size})
    return result


def evidence() -> dict:
    rc, dc = configurations()
    rr, dr = json.loads(render.PUBLIC.read_text()), json.loads(data.PUBLIC.read_text())
    render.check_public(rr, rc, dc)
    return {"schema_version": 1, "kind": "reviewed-game-specific-assembly-ownership",
            "origin": "reviewed-native-handwritten-assembly-reconstruction",
            "historical_source_recovered": False, "global_percentage": None,
            "limits": LIMITS, "inputs": review_inputs(), "units": units(),
            "authored_asm_code_bytes": 678, "authored_asm_data_bytes": 64,
            "checked_alignment_bytes": 2, "checked_runtime_patch_placeholder_bytes": 12,
            "cxx_authored_credit": 0,
            "native_review_sha256": dc["native_review_sha256"],
            "vendor_search": {"path": LIBRARY, "sha256": LIBRARY_SHA, "size": 273721, "members": 640,
                              "absent_identifiers": ["GRAPH_PUTSA_FX", "GRPPSAFX", "GLYPH_WEIGHT"],
                              "native_callback_delta_bank_matches": 0},
            "targets": {name: {"sha256": p["target_sha256"], "view": p["target_view"]}
                        for name, p in rr["profiles"].items()},
            "replay_receipts": {"code": rr["replay_receipt_sha256"], "data": dr["replay_receipt_sha256"]}}


def validate_metadata(proof: dict) -> None:
    if proof != evidence():
        raise ValueError("reviewed ASM evidence differs from current sources, exact gates or ownership classification")


def validate_decision(proof: dict, decision: dict, proof_sha: str) -> None:
    if (decision.get("schema_version") != 1 or decision.get("classification") != proof["origin"]
            or decision.get("evidence_sha256") != proof_sha or decision.get("historical_source_recovered") is not False
            or decision.get("units") != [row["id"] for row in proof["units"]]
            or decision.get("cxx_authored_credit") != 0):
        raise ValueError("missing, stale or broadened explicit ASM ownership decision")


def native_review(native_path: Path, code_receipt: Path, data_receipt: Path) -> None:
    rc, dc = configurations()
    # Revalidation uses the same immutable accepted receipts; serialized public
    # results must already equal them, so no acceptance/provenance can be replaced.
    for receipt_path, module, config in ((data_receipt, data, dc), (code_receipt, render, rc)):
        receipt = json.loads(receipt_path.read_text())
        expected = {**receipt, "replay_receipt_sha256": digest_file(receipt_path)}
        if expected != json.loads(module.PUBLIC.read_text()):
            raise ValueError("native review must use the already accepted unchanged receipt")
        if module is data:
            data.accept(receipt_path, config)
        else:
            render.accept(receipt_path, config, dc)
    targets = data.targets_for(dc)
    data.native_review(native_path, dc, targets)
    raw = (ROOT / LIBRARY).read_bytes()
    if digest_bytes(raw) != LIBRARY_SHA or len(raw) != 273721 or len(library_members(raw)) != 640:
        raise ValueError("bounded original-assembly vendor search identity changed")
    if any(identifier.encode() in raw.upper() for identifier in ("GRAPH_PUTSA_FX", "GRPPSAFX", "GLYPH_WEIGHT")):
        raise ValueError("pinned library contains a candidate renderer identifier")
    for name, (_, target, _) in targets.items():
        profile = dc["profiles"][name]
        start = profile["dispatch_start"]
        if raw.count(target.program_image[start:start + 20]):
            raise ValueError("pinned library contains the native callback-delta bank")


def split_unit(row: dict) -> list[dict]:
    if row["scope"] != "code":
        return [{"start": row["start"], "end": row["end"], "kind": "accepted-reviewed-asm-initialized-data",
                 "unit": row["id"], "origin": "reviewed-native-handwritten-assembly-reconstruction"}]
    rc, _ = configurations()
    render.classification(rc)
    alignment = set(rc["alignment_offsets"])
    placeholders = {i for start, end in rc["runtime_patch_placeholder_ranges"] for i in range(start, end)}
    points = sorted({0, rc["size"], *(i for p in alignment | placeholders for i in (p, p + 1))})
    claims = []
    for left, right in zip(points, points[1:]):
        kind = ("checked-uncredited-asm-alignment" if left in alignment else
                "checked-uncredited-asm-runtime-placeholder" if left in placeholders else
                "accepted-reviewed-asm-instructions")
        claim = {"start": row["start"] + left, "end": row["start"] + right, "kind": kind,
                 "unit": row["id"], "origin": "reviewed-native-handwritten-assembly-reconstruction"}
        if claims and claims[-1]["end"] == claim["start"] and claims[-1]["kind"] == kind:
            claims[-1]["end"] = claim["end"]
        else:
            claims.append(claim)
    return claims


def reviewed_claims(root: Path, views: dict, *, verify_targets: bool = False) -> tuple[dict, str | None]:
    path = root / DECISION
    if not path.exists():
        return {}, None
    proof_path = root / PROOF
    proof, decision = json.loads(proof_path.read_text()), json.loads(path.read_text())
    validate_metadata(proof)
    validate_decision(proof, decision, digest_file(proof_path))
    targets = data.targets_for(configurations()[1]) if verify_targets else None
    claims = {name: [] for name in ("op", "maine")}
    for row in proof["units"]:
        name = row["context"]
        view = views[name]
        target = proof["targets"][name]["view"]
        if (view["size"], view["sha256"]) != (target["payload_size"], target["payload_sha256"]):
            raise ValueError("reviewed ASM coordinates differ from observed target view")
        if targets and digest_bytes(targets[name][1].program_image[row["start"]:row["end"]]) != row["sha256"]:
            raise ValueError("reviewed complete ASM extent differs from pinned native bytes")
        claims[name].extend(split_unit(row))
    return claims, digest_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-evidence", action="store_true")
    mode.add_argument("--structural-check", action="store_true")
    mode.add_argument("--verify-native", action="store_true")
    parser.add_argument("--native-review", type=Path)
    parser.add_argument("--code-receipt", type=Path)
    parser.add_argument("--data-receipt", type=Path)
    args = parser.parse_args()
    if args.write_evidence or args.verify_native:
        if not all((args.native_review, args.code_receipt, args.data_receipt)):
            parser.error("native review needs original boundary review and both accepted receipt paths")
        native_review(args.native_review.resolve(), args.code_receipt.resolve(), args.data_receipt.resolve())
    proof = evidence()
    if args.write_evidence:
        (ROOT / PROOF).write_text(json.dumps(proof, indent=2) + "\n")
        print("PASS: native ASM evidence written; explicit ownership adoption remains separate")
        return 0
    validate_metadata(json.loads((ROOT / PROOF).read_text()))
    validate_decision(proof, json.loads((ROOT / DECISION).read_text()), digest_file(ROOT / PROOF))
    print("PASS: reviewed ASM ownership: 678 instruction + 64 DATA bytes; 14 checked uncredited bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

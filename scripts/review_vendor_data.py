#!/usr/bin/env python3
"""Review complete relocation-free CL.LIB DATA; never grant authored credit.

Native --write/--check use retained pinned library/MAP/MZ inputs. Public
--structural-check verifies identities and review decisions, not private bytes.
No compiler, unpacker, game, Wine or Ghidra process is launched.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_vendor import PINS, VendorReview, need, sha

ROOT = Path(__file__).resolve().parents[1]
PROOF = "config/vendor_data_ownership.json"
DECISION = "config/reviewed_vendor_data_units.json"
SOURCE_PINS = "config/cl_data_sources.json"
SOURCE_PINS_SHA256 = "8c3188721df9b05207a6942884ae85eaabe3bdf81a6941109af645a5b7a2d88c"
PARENTS = {name: f"config/vendor_ownership{suffix}.json"
           for name, suffix in (("main", ""), ("op", ".op"), ("maine", ".maine"))}
BASES = {"main": 0x209D0, "op": 0xEFE0, "maine": 0x10110}
ALLOWED_RECORDS = {"THEADR", "COMENT", "LNAMES", "SEGDEF", "GRPDEF", "EXTDEF",
                   "PUBDEF", "LEDATA", "FIXUPP", "ALIAS", "MODEND"}


def source_pins(root: Path) -> dict:
    raw = (root / SOURCE_PINS).read_bytes()
    need(sha(raw) == SOURCE_PINS_SHA256, "reviewed CL DATA source pins changed")
    return json.loads(raw)


def identity(root: Path) -> dict:
    paths = [SOURCE_PINS, "scripts/review_vendor_data.py", "scripts/review_vendor.py",
             "scripts/lib/borland_library.py", "scripts/lib/omf.py",
             "scripts/lib/pc98.py", "scripts/lib/unit_context.py", "scripts/lib/unit_oracle.py",
             "scripts/lib/targets.py", "scripts/lib/diet.py", "scripts/lib/unit_extents.py",
             "config/toolchain.toml", "config/targets.toml", "config/ownership.toml", *PARENTS.values()]
    return {p: sha((root / p).read_bytes()) for p in paths}


def data_template(mod: dict, segment: int) -> tuple[bytes, list[dict]]:
    """Require one entire ordinary DATA SEGDEF, with no selected fixup or gap."""
    need(not set(mod["records"]) - ALLOWED_RECORDS, "unsupported OMF transformation")
    need(type(segment) is int and 0 < segment < len(mod["segs"]), "invalid DATA segment")
    seg = mod["segs"][segment]
    need(seg["cl"] == "DATA" and seg["name"] == "_DATA" and seg["size"] > 0,
         "expected a complete initialized _DATA contribution")
    need(not any(f["segment"] == segment for f in mod["fixups"]),
         "relocated DATA needs a separate linkage proof")
    size = seg["size"]
    body, covered, chunks = bytearray(size), bytearray(size), []
    for block in mod["blocks"]:
        if block["segment"] != segment:
            continue
        start, raw = block["offset"], block["data"]
        end = start + len(raw)
        need(type(start) is int and 0 <= start < end <= size and not any(covered[start:end]),
             "overlapping or out-of-bounds DATA LEDATA")
        body[start:end], covered[start:end] = raw, b"\1" * len(raw)
        chunks.append({"offset": start, "size": len(raw), "sha256": sha(raw)})
    need(all(covered), "complete DATA LEDATA coverage required")
    return bytes(body), chunks


def unique_data_match(image, body: bytes, start: int, data_base: int) -> None:
    """Compare unmodified bytes and the actual empty ordered relocation stream."""
    need(data_base <= start and start + len(body) <= len(image.program_image),
         "native DATA extent outside the stored DATA view")
    need(image.program_image[start:start + len(body)] == body, "native whole DATA mismatch")
    need(image.program_image.find(body, data_base) == start and
         image.program_image.find(body, start + 1) < 0, "ambiguous native DATA identity")
    need(not relative_fixups(image, start, len(body)), "native DATA has unexpected relocations")


def native_review(root: Path = ROOT) -> dict:
    pins = source_pins(root)
    lib = (root / ".analysis/toolchain/installed/tc40j/LIB/CL.LIB").read_bytes()
    need(sha(lib) == PINS["library_sha256"], "pinned CL.LIB changed")
    need(sha((root / "config/toolchain.toml").read_bytes()) == PINS["toolchain_manifest_sha256"],
         "toolchain manifest changed")
    rows, targets = [], {}
    for name, parent_path in PARENTS.items():
        parent = json.loads((root / parent_path).read_text())
        need(parent["library_sha256"] == sha(lib), "parent library identity differs")
        context = UnitContext(root, name)
        artifact, target, target_view = load_unit_target(context, context.config())
        need(artifact["sha256"] == parent["target_sha256"] and
             sha(target.program_image) == parent["target_payload_sha256"], "parent target identity differs")
        if name == "main":
            base = root / ".analysis/builds/main-calibration-b/source"
            exe_pin, map_pin = parent["calibration_exe_sha256"], parent["calibration_map_sha256"]
        else:
            base = root / parent["calibration"]["root"]
            exe_pin, map_pin = parent["calibration"]["exe_sha256"], parent["calibration"]["map_sha256"]
        exe_raw = (base / f"bin/th05/{name}.exe").read_bytes()
        map_raw = (base / f"obj/th05/{name}.map").read_bytes()
        need(sha(exe_raw) == exe_pin and sha(map_raw) == map_pin, "retained calibration identity differs")
        calibration = parse_mz(exe_raw)
        need(calibration.valid, "invalid calibration MZ")
        review = VendorReview(lib, map_raw, calibration, target)
        targets[name] = {"artifact": artifact["id"], "size": len(target.program_image),
                         "target_sha256": artifact["sha256"],
                         "payload_sha256": sha(target.program_image), "target_view": target_view}
        for member, pin in pins.items():
            mod = review.mods[member]
            need(mod["program_sha256"] == pin["member_program_sha256"], "library member identity differs")
            segments = [i for i, s in enumerate(mod["segs"]) if s and s["cl"] == "DATA" and s["size"]]
            need(len(segments) == 1, "expected one complete member DATA contribution")
            segment = segments[0]
            body, chunks = data_template(mod, segment)
            need(len(body) == pin["size"] and sha(body) == pin["data_sha256"], "member DATA identity differs")
            con = review.contribution(mod, segment)
            a = con["start"]
            need(calibration.program_image[a:a + len(body)] == body and
                 not relative_fixups(calibration, a, len(body)), "library/MAP/linked DATA disagreement")
            start = pin["starts"][name]
            unique_data_match(target, body, start, BASES[name])
            rows.append({"id": f"{name}-cl-data-{member}", "context": name, "member": member,
                         "segment": "_DATA", "start": start, "end": start + len(body),
                         "size": len(body), "data_sha256": sha(body),
                         "member_program_sha256": mod["program_sha256"],
                         "calibration_start": a, "calibration_size": con["size"],
                         "ordered_fixups": [], "omf_fixup_count": 0,
                         "ledatas": chunks, "complete_ledatas": True})
    result = {"schema_version": 1, "kind": "whole-relocation-free-cl-data-evidence",
              "library": "CL.LIB", "library_sha256": sha(lib), "decision": "PROPOSAL",
              "authored_credit": 0, "authored_denominator": None, "compiler_invocations": 0,
              "identities": identity(root), "targets": targets, "contributions": rows,
              "contribution_count": len(rows), "bytes": sum(r["size"] for r in rows)}
    validate_metadata(result, root=root)
    return result


def validate_metadata(proof: dict, *, root: Path = ROOT) -> None:
    """Public fail-closed review validation; native byte replay is separate."""
    pins = source_pins(root)
    need(proof.get("schema_version") == 1 and proof.get("kind") == "whole-relocation-free-cl-data-evidence",
         "unsupported CL DATA evidence")
    need(proof.get("library") == "CL.LIB" and proof.get("library_sha256") == PINS["library_sha256"] and
         proof.get("decision") == "PROPOSAL", "unexpected source or evidence decision")
    need(type(proof.get("authored_credit")) is int and proof["authored_credit"] == 0 and
         proof.get("authored_denominator") is None and type(proof.get("compiler_invocations")) is int and
         proof["compiler_invocations"] == 0, "vendor DATA cannot receive authored/build credit")
    need(proof.get("identities") == identity(root), "stale CL DATA verifier/input identities")
    targets = proof.get("targets")
    need(isinstance(targets, dict) and set(targets) == set(PARENTS), "target inventory differs")
    for context, target in targets.items():
        parent = json.loads((root / PARENTS[context]).read_text())
        need(target.get("artifact") == f"th05-{context}" and
             target.get("target_sha256") == parent["target_sha256"] and
             target.get("payload_sha256") == parent["target_payload_sha256"] and
             type(target.get("size")) is int and target["size"] > BASES[context], "wrong native target")
        if context != "main":
            need(target.get("target_view") == parent["target_view"] and
                 target["size"] == parent["target_payload_size"], "decoded target proof differs")
        else:
            need(target.get("target_view") is None and target["size"] == 145958, "wrong MAIN view")
    rows = proof.get("contributions")
    need(isinstance(rows, list) and len(rows) == len(pins) * len(PARENTS), "DATA row inventory differs")
    seen = set()
    for row in rows:
        name, member = row.get("context"), row.get("member")
        need(name in PARENTS and member in pins, "unreviewed member or artifact")
        pin = pins[member]
        key = f"{name}-cl-data-{member}"
        need(row.get("id") == key and key not in seen, "duplicate/incorrect DATA owner")
        seen.add(key)
        need(type(row.get("size")) is int and row["size"] == pin["size"] and
             type(row.get("start")) is int and row["start"] == pin["starts"][name] and
             type(row.get("end")) is int and
             row["end"] == row["start"] + row["size"] <= targets[name]["size"] and
             row.get("segment") == "_DATA", "complete native DATA boundary differs")
        need(row.get("data_sha256") == pin["data_sha256"] and
             row.get("member_program_sha256") == pin["member_program_sha256"], "source DATA digest differs")
        need(row.get("ordered_fixups") == [] and type(row.get("omf_fixup_count")) is int and
             row["omf_fixup_count"] == 0 and row.get("complete_ledatas") is True and
             type(row.get("calibration_size")) is int and row["calibration_size"] == row["size"] and
             type(row.get("calibration_start")) is int and
             row["calibration_start"] == pin["calibration_starts"][name],
             "relocated, incomplete or changed DATA contribution")
        chunks, position = row.get("ledatas"), 0
        need(isinstance(chunks, list) and chunks, "missing complete DATA producer records")
        for chunk in sorted(chunks, key=lambda c: c["offset"]):
            need(type(chunk.get("offset")) is int and chunk["offset"] == position and
                 type(chunk.get("size")) is int and chunk["size"] > 0, "DATA record gap/overlap")
            digest = chunk.get("sha256")
            need(isinstance(digest, str) and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                 "invalid DATA record digest")
            position += chunk["size"]
        need(position == row["size"], "DATA record coverage differs")
        # These eight independently reviewed source templates each occupy one
        # complete ordinary DATA record. Do not silently widen that evidence.
        need(chunks == [{"offset": 0, "size": row["size"], "sha256": row["data_sha256"]}],
             "reviewed whole DATA record identity differs")
    need(proof.get("contribution_count") == len(rows) and
         proof.get("bytes") == sum(r["size"] for r in rows) == 1857, "CL DATA totals differ")


def reviewed_claims(root: Path, views: dict, *, verify_targets: bool = False) -> tuple[dict, str | None]:
    if not (root / DECISION).exists():
        return {}, None
    raw = (root / PROOF).read_bytes()
    proof, decision = json.loads(raw), json.loads((root / DECISION).read_text())
    validate_metadata(proof, root=root)
    need(decision.get("schema_version") == 1 and decision.get("classification") ==
         "third-party-library-initialized-data" and decision.get("evidence_sha256") == sha(raw),
         "stale or invalid CL DATA decision")
    selected = decision.get("units")
    proposed = {r["id"]: r for r in proof["contributions"]}
    need(isinstance(selected, list) and selected and all(isinstance(x, str) for x in selected) and
         len(selected) == len(set(selected)) and set(selected) <= proposed.keys(), "invalid explicit DATA selection")
    if verify_targets:
        need(native_review(root) == proof, "native CL DATA replay differs")
    claims = {name: [] for name in PARENTS}
    for key in selected:
        row = proposed[key]
        view = views[row["context"]]
        need(view["sha256"] == proof["targets"][row["context"]]["payload_sha256"] and
             view["size"] == proof["targets"][row["context"]]["size"], "ownership view differs")
        claims[row["context"]].append({"start": row["start"], "end": row["end"],
            "kind": "verified-vendor-initialized-data", "content_kind": "library-initialized-data",
            "instruction_bytes": 0, "library": "CL.LIB", "member": row["member"],
            "scope_id": row["id"]})
    return claims, sha((root / DECISION).read_bytes())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    for flag in ("write", "check", "structural-check"):
        group.add_argument(f"--{flag}", action="store_true")
    args = p.parse_args()
    if args.structural_check:
        validate_metadata(json.loads((ROOT / PROOF).read_text()))
        print("PASS: public CL DATA identities/structure; private bytes not replayed")
    else:
        evidence = native_review()
        if args.write:
            (ROOT / PROOF).write_text(json.dumps(evidence, indent=2) + "\n")
        else:
            need(evidence == json.loads((ROOT / PROOF).read_text()), "native CL DATA evidence changed")
        print(f"PASS: {evidence['contribution_count']} complete native CL DATA extents / {evidence['bytes']} bytes; zero authored credit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

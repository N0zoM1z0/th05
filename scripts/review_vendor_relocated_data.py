#!/usr/bin/env python3
"""Recover complete CL.LIB initialized DATA that contains real OMF fixups.

The pinned library records, actual calibration MAP/MZ, and all three native
payloads must agree. This classifies foreign library DATA, never authored C++.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups
from review_vendor import PINS as LIB_PINS, VendorReview, need, sha
from review_vendor_data import BASES, PARENTS

ROOT = Path(__file__).resolve().parents[1]
PROOF = "config/vendor_relocated_data_ownership.json"
DECISION = "config/reviewed_vendor_relocated_data_units.json"
MEMBERS = {
    "exit": {
        "size": 12,
        "program_sha256": "56724f7cf9262534a85824a0c99662abdcbca62923f298ea05b8b29c00803c21",
        "raw_sha256": "15ec7bf0b50732b49f8228e07d24365338f9e3ab994b00af08e5a3bffe55fd8b",
        "starts": {"main": 0x22A78, "op": 0x11858, "maine": 0x1190C},
        "fixups": [(8, 3), (4, 3), (0, 3)],
    },
    "files": {
        "size": 400,
        "program_sha256": "b34a5164c6e65c285abb1aa4c20f361f405ebf539653f5ae523acaa5b5b4826b",
        "raw_sha256": "5b8c2c15d419c2372157b44f22e35fbb7df3fca2a022d7d8e3b02aad6dca7e7a",
        "starts": {"main": 0x22A84, "op": 0x11864, "maine": 0x11918},
        "fixups": [(98, 1), (78, 1), (58, 1), (38, 1), (18, 1)],
    },
    "xxv": {
        "size": 296,
        "program_sha256": "b89c4c08bba1551b607344627c107d06bf192274d270d9c1924f79cad439596a",
        "raw_sha256": "275d37444b55c143153f1e7c75fb9ae2e18cbd0e6be4a635b70a4f711c0f1d64",
        "starts": {"main": 0x22DB6, "op": 0x11B96, "maine": 0x11C4A},
        "fixups": [(14, 3), (10, 3)],
    },
    # Fixup-free small CL.LIB DATA members between already verified neighbours.
    "atexit": {
        "anchor": "exit",
        "size": 2,
        "program_sha256": "71e2cc923c16b7a3865c676998bd9b977607767a60a5b50cfd42d727584b087a",
        "raw_sha256": "96a296d224f285c67bee93c30f8a309157f0daa35dc5b87e410b78630a09cfc7",
        "starts": {"main": 0x22A76, "op": 0x11856, "maine": 0x1190A},
        "fixups": [],
    },
    "stklen": {
        "anchor": "ctype",
        "size": 2,
        "program_sha256": "999875ad91846423ebdba9d820c13442673becefa65eb948e2163ae155ffbd2b",
        "raw_sha256": "0298d122906dcfc10892cb53a73992fc5b9f493ea4c9badb27b791b4127a7fe7",
        "starts": {"main": 0x22CB2, "op": 0x11A92, "maine": 0x11B46},
        "fixups": [],
    },
    "cputype": {
        "anchor": "signal",
        "size": 2,
        "program_sha256": "4273bf05f930aa3dcbe04c1dbe46f2f890644ddd1b3ecb87563fda80400b0fcc",
        "raw_sha256": "96a296d224f285c67bee93c30f8a309157f0daa35dc5b87e410b78630a09cfc7",
        "starts": {"main": 0x22EDE, "op": 0x11CBE, "maine": 0x11D72},
        "fixups": [],
    },
    "fbrk": {
        "anchor": "signal",
        "size": 2,
        "program_sha256": "72cca1458fe282b18091b13d7333333ebad9428435c14ce23685ebde28756abc",
        "raw_sha256": "96a296d224f285c67bee93c30f8a309157f0daa35dc5b87e410b78630a09cfc7",
        "starts": {"main": 0x22EE0, "op": 0x11CC0, "maine": 0x11D74},
        "fixups": [],
    },
    "_pathops": {
        "anchor": "xx",
        "size": 16,
        "program_sha256": "41f6ded7642bf119b7710fd4af35d85e7e28f734196a05533c71f09d67f5c432",
        "raw_sha256": "374708fff7719dd5979ec875d56cd2286f6d3cf7ec317a3b25632aab28ec37bb",
        "starts": {"main": 0x22F08, "op": 0x11CE8, "maine": 0x11D9C},
        "fixups": [],
    },
    "srchenv": {
        "anchor": "xx",
        "size": 1,
        "program_sha256": "cf5674d8ba1020c5e04bbf3cd9a58217d111b872d173ee8b45d954fee68f7eb1",
        "raw_sha256": "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d",
        "starts": {"main": 0x22F18, "op": 0x11CF8, "maine": 0x11DAC},
        "fixups": [],
    },
    "srchstr": {
        "anchor": "xx",
        "size": 2,
        "program_sha256": "34696bea1949cef30d5aad7f591a2139866cbb3f2d4091633d4a78e8600ca8dd",
        "raw_sha256": "1472d0645f552820b5472b91341c2d9a118c8a96f4a72758d6aeeb14c10a1107",
        "starts": {"main": 0x22F1A, "op": 0x11CFA, "maine": 0x11DAE},
        "fixups": [],
    },
    "setvbuf": {
        "anchor": "xx",
        "size": 4,
        "program_sha256": "7ff5a72d3a1c4be1c7b7855d2c787fe7ef8cd0be61335cf3ca27ff7f03f4f1b8",
        "raw_sha256": "df3f619804a92fdb4057192dc43dd748ea778adc52bc498ce80524c014b81119",
        "starts": {"main": 0x22F1C, "op": 0x11CFC, "maine": 0x11DB0},
        "fixups": [],
    },
    "sysnerr": {
        "anchor": "xx",
        "size": 2,
        "program_sha256": "f562c74c929309d1d8334f4ef93d8631c94612b8e8e03c63b3f107ce8c0c117b",
        "raw_sha256": "e4f60d0aa6d7f3d3b6a6494b1c861b99f649c6f9ec51abaf201b20f297327c95",
        "starts": {"main": 0x22F20, "op": 0x11D00, "maine": 0x11DB4},
        "fixups": [],
    },
    "setenvp": {
        "anchor": "strings",
        "size": 4,
        "program_sha256": "a35c3378de5ce9b318c15d0670a6e49807ade277da773ad61102f3fc7ad131e0",
        "raw_sha256": "df3f619804a92fdb4057192dc43dd748ea778adc52bc498ce80524c014b81119",
        "starts": {"main": 0x22F34, "op": 0x11D14, "maine": 0x11DC8},
        "fixups": [],
    },
    # Startup/exit records and the partly zero-filled NEW DATA, placed by layout.
    "new/_INIT_": {
        "anchor": "loadprog",
        "member": "new",
        "segment": "_INIT_",
        "size": 6,
        "program_sha256": "910a632344f47b81d5e152ab5e9fd7b2a399032fec92d9ef309995050a23dfb0",
        "raw_sha256": "4e3d6ec906193734e7d8546c9924efb090911fb8c0b22b9a4201ce1d4df23542",
        "starts": {"main": 0x22FC6, "op": 0x11DA8, "maine": 0x11E5A},
        "fixups": [(2, 3)],
    },
    "setupio/_INIT_": {
        "anchor": "loadprog",
        "member": "setupio",
        "segment": "_INIT_",
        "size": 6,
        "program_sha256": "aa046c3ee43eabe28a4ce0ed9e0620064abc63a4cb6ce4ff3c1dd8c8b12b6e5d",
        "raw_sha256": "3686cb37b7fe4758ac2024a76e30a4c6ee2fdc25c66aa21dd55a9569b91ea504",
        "starts": {"main": 0x22FCC, "op": 0x11DAE, "maine": 0x11E60},
        "fixups": [(2, 1)],
    },
    "cputype/_INIT_": {
        "anchor": "loadprog",
        "member": "cputype",
        "segment": "_INIT_",
        "zero_gaps": True,
        "size": 6,
        "program_sha256": "4273bf05f930aa3dcbe04c1dbe46f2f890644ddd1b3ecb87563fda80400b0fcc",
        "raw_sha256": "ceafee88e83b97cb5bc6b13a26f591db8aab79f02b7af3ec0e0d9b842050af74",
        "starts": {"main": 0x22FD2, "op": 0x11DB4, "maine": 0x11E66},
        "fixups": [(2, 1)],
    },
    "_pathops/_INIT_": {
        "anchor": "loadprog",
        "member": "_pathops",
        "segment": "_INIT_",
        "size": 6,
        "program_sha256": "41f6ded7642bf119b7710fd4af35d85e7e28f734196a05533c71f09d67f5c432",
        "raw_sha256": "a55a43f7426e1b4d8a8d2e1bf259fe39b33a2870ea3c697c58723f29bbb02b40",
        "starts": {"main": 0x22FD8, "op": 0x11DBA, "maine": 0x11E6C},
        "fixups": [(2, 1)],
    },
    "setenvp/_INIT_": {
        "anchor": "loadprog",
        "member": "setenvp",
        "segment": "_INIT_",
        "zero_gaps": True,
        "size": 6,
        "program_sha256": "a35c3378de5ce9b318c15d0670a6e49807ade277da773ad61102f3fc7ad131e0",
        "raw_sha256": "ceafee88e83b97cb5bc6b13a26f591db8aab79f02b7af3ec0e0d9b842050af74",
        "starts": {"main": 0x22FDE, "op": 0x11DC0, "maine": 0x11E72},
        "fixups": [(2, 1)],
    },
    "new/_EXIT_": {
        "anchor": "loadprog",
        "member": "new",
        "segment": "_EXIT_",
        "size": 6,
        "program_sha256": "910a632344f47b81d5e152ab5e9fd7b2a399032fec92d9ef309995050a23dfb0",
        "raw_sha256": "f9d7da3ccfd452664ff7ddca02a7fcd0eb50f3b0ffaf5b503787c1a05dbf1bc8",
        "starts": {"main": 0x22FE4, "op": 0x11DC6, "maine": 0x11E78},
        "fixups": [(2, 3)],
    },
    "new": {
        "anchor": "ctype",
        "zero_gaps": True,
        "size": 24,
        "program_sha256": "910a632344f47b81d5e152ab5e9fd7b2a399032fec92d9ef309995050a23dfb0",
        "raw_sha256": "956fcd7415783b1e7f7ff3970fe286f73e59367bfa56284802874787555fc043",
        "starts": {"main": 0x22C9A, "op": 0x11A7A, "maine": 0x11B2E},
        "fixups": [(6, 3)],
    },
}
INPUTS = ["scripts/review_vendor_relocated_data.py", "scripts/review_vendor.py",
          "scripts/review_vendor_data.py", "scripts/lib/borland_library.py",
          "scripts/lib/omf.py", "scripts/lib/pc98.py", "scripts/lib/unit_context.py",
          "scripts/lib/unit_oracle.py", "config/toolchain.toml", "config/targets.toml",
          "config/ownership.toml", *PARENTS.values()]


def identities(root: Path) -> dict:
    return {p: sha((root / p).read_bytes()) for p in INPUTS}


def complete_data(mod: dict, segment: int, zero_gaps: bool = False) -> tuple[bytes, list[dict]]:
    """Read every original DATA LEDATA, retaining actual fixups for the linker."""
    size = mod["segs"][segment]["size"]
    body, covered, chunks = bytearray(size), bytearray(size), []
    for block in mod["blocks"]:
        if block["segment"] != segment:
            continue
        a, data = block["offset"], block["data"]
        b = a + len(data)
        need(0 <= a < b <= size and not any(covered[a:b]),
             "overlapping or out-of-bounds DATA LEDATA")
        body[a:b], covered[a:b] = data, b"\1" * len(data)
        chunks.append({"offset": a, "size": len(data), "sha256": sha(data)})
    # TLINK zero-fills SEGDEF bytes that no LEDATA covers; only listed pins rely on it.
    need(size > 0 and (zero_gaps or all(covered)), "incomplete DATA LEDATA coverage")
    return bytes(body), chunks


def linked_images(review: VendorReview, mod: dict, segment: int, start: int,
                  original_dgroup: int, zero_gaps: bool = False
                  ) -> tuple[bytes, bytes, list[int], list[dict], list[dict]]:
    """Apply only the two observed 16-bit DATA fixup kinds, never normalize bytes."""
    raw, chunks = complete_data(mod, segment, zero_gaps)
    con = review.contribution(mod, segment)
    cal, native = bytearray(raw), bytearray(raw)
    ordered_mz, actions = [], []
    selected = [f for f in mod["fixups"] if f["segment"] == segment]
    for f in selected:
        site, kind = f["site"], f["kind"]
        need(not f["relative"] and f["displacement"] == 0 and
             f["target_method"] == 0 and f["frame_index"] in (None, 1),
             "unsupported DATA fixup form")
        if kind == 1 and mod["segs"][f["target_index"]]["cl"] == "CODE":
            # Near startup records: an offset into the member's combined CODE
            # segment, linked exactly like the far records below.
            code = review.contribution(mod, f["target_index"])
            frame = review.segbases[code["segment"].casefold()] // 16 * 16
            word = int.from_bytes(raw[site:site + 2], "little")
            linked = ((word + code["start"] - frame) & 0xffff).to_bytes(2, "little")
            cal[site:site + 2] = native[site:site + 2] = linked
            after_cal = after_native = linked
        elif kind == 1:
            # Five FILES near pointers resolve into their own _DATA SEGDEF.
            need(f["frame_method"] == 1 and
                 mod["groups"][f["frame_index"]]["name"].casefold() == "dgroup" and
                 f["target_index"] == segment, "unexpected near DATA binding")
            word = int.from_bytes(raw[site:site + 2], "little")
            calibration_value = (word + con["start"] - review.groups["dgroup"]) & 0xffff
            original_value = (word + start - original_dgroup) & 0xffff
            cal[site:site + 2] = calibration_value.to_bytes(2, "little")
            native[site:site + 2] = original_value.to_bytes(2, "little")
            after_cal, after_native = cal[site:site + 2], native[site:site + 2]
        elif kind == 3:
            # EXIT/XXV store actual far pointers to their own linked CODE.
            need(f["frame_method"] == 5, "unexpected far DATA binding")
            code_si = f["target_index"]
            need(mod["segs"][code_si]["cl"] == "CODE", "far target is not CODE")
            code = review.contribution(mod, code_si)
            frame = (review.groups[code["group"].casefold()]
                     if code["group"] != "(none)" else
                     review.segbases[code["segment"].casefold()] // 16 * 16)
            old_off = int.from_bytes(raw[site:site + 2], "little")
            old_seg = int.from_bytes(raw[site + 2:site + 4], "little")
            linked_far = ((old_off + code["start"] - frame) & 0xffff).to_bytes(2, "little")
            linked_far += ((old_seg + frame // 16) & 0xffff).to_bytes(2, "little")
            cal[site:site + 4] = native[site:site + 4] = linked_far
            after_cal = after_native = linked_far
            ordered_mz.append(site + 2)
        else:
            raise ValueError("unsupported DATA relocation kind: " + str(kind))
        actions.append({"site": site, "kind": kind, "frame_method": f["frame_method"],
                        "target_method": f["target_method"], "target_index": f["target_index"],
                        "calibration_bytes_sha256": sha(after_cal),
                        "original_bytes_sha256": sha(after_native)})
    need(len(raw) == con["size"], "incomplete DATA contribution")
    return bytes(cal), bytes(native), ordered_mz, actions, chunks



def anchor_delta(root: Path, review: VendorReview, context: str, anchor: str) -> int:
    if anchor in MEMBERS and "anchor" not in MEMBERS[anchor]:
        mod = review.mods[anchor]
        segment = next(i for i, s in enumerate(mod["segs"])
                       if s and s["name"] == "_DATA" and s["cl"] == "DATA" and s["size"])
        return MEMBERS[anchor]["starts"][context] - review.contribution(mod, segment)["start"]
    rows = json.loads((root / "config/vendor_data_ownership.json").read_text())["contributions"]
    row = next(r for r in rows if r["id"] == f"{context}-cl-data-{anchor}")
    return row["start"] - row["calibration_start"]

def native_review(root: Path = ROOT) -> dict:
    lib = (root / ".analysis/toolchain/installed/tc40j/LIB/CL.LIB").read_bytes()
    need(sha(lib) == LIB_PINS["library_sha256"], "foreign CL.LIB changed")
    rows, targets = [], {}
    for context, parent_path in PARENTS.items():
        parent = json.loads((root / parent_path).read_text())
        need(parent["library_sha256"] == sha(lib), "parent library identity differs")
        ctx = UnitContext(root, context)
        artifact, target, view = load_unit_target(ctx, ctx.config())
        if context == "main":
            base = root / ".analysis/builds/main-calibration-b/source"
            exe_pin, map_pin = parent["calibration_exe_sha256"], parent["calibration_map_sha256"]
        else:
            base = root / parent["calibration"]["root"]
            exe_pin, map_pin = parent["calibration"]["exe_sha256"], parent["calibration"]["map_sha256"]
        exe = (base / f"bin/th05/{context}.exe").read_bytes()
        mapping = (base / f"obj/th05/{context}.map").read_bytes()
        need(sha(exe) == exe_pin and sha(mapping) == map_pin, "calibration changed")
        cal = parse_mz(exe)
        need(cal.valid and artifact["sha256"] == parent["target_sha256"] and
             sha(target.program_image) == parent["target_payload_sha256"],
             "calibration or original payload identity changed")
        review = VendorReview(lib, mapping, cal, target)
        targets[context] = {"artifact": artifact["id"], "size": len(target.program_image),
                            "payload_sha256": sha(target.program_image), "view": view,
                            "calibration_exe_sha256": exe_pin, "calibration_map_sha256": map_pin}
        for member, pin in MEMBERS.items():
            # Keys name the member, or "member/_INIT_" for a startup/exit record.
            mod = review.mods[pin.get("member", member)]
            need(mod["program_sha256"] == pin["program_sha256"], "CL member program changed")
            segname = pin.get("segment", "_DATA")
            segments = [i for i, s in enumerate(mod["segs"])
                        if s and s["name"] == segname and
                        s["cl"] in ("DATA", "INITDATA", "EXITDATA") and s["size"]]
            need(len(segments) == 1, "ambiguous DATA segment")
            segment = segments[0]
            con = review.contribution(mod, segment)
            start, size = pin["starts"][context], pin["size"]
            need(con["size"] == size and len(target.program_image) >= start + size,
                 "DATA extent/target bounds differ")
            cal_bytes, original_bytes, mz, actions, chunks = linked_images(
                review, mod, segment, start, BASES[context], pin.get("zero_gaps", False))
            need([(a["site"], a["kind"]) for a in actions] == pin["fixups"],
                 "original OMF fixup order differs")
            need(sha(complete_data(mod, segment, pin.get("zero_gaps", False))[0]) == pin["raw_sha256"],
                 "unlinked DATA bytes changed")
            need(cal.program_image[con["start"]:con["start"] + size] == cal_bytes,
                 "full calibration DATA byte mismatch")
            need(target.program_image[start:start + size] == original_bytes,
                 "full original DATA byte mismatch")
            need(relative_fixups(cal, con["start"], size) == mz and
                 relative_fixups(target, start, size) == mz, "ordered original MZ relocations differ")
            if "anchor" in pin:
                # Small members are placed by the calibration layout: they keep
                # the original-minus-calibration offset of a verified neighbour.
                need(start - con["start"] == anchor_delta(root, review, context, pin["anchor"]),
                     "DATA placement differs from its verified neighbour")
            else:
                need(target.program_image.find(original_bytes, BASES[context]) == start and
                     target.program_image.find(original_bytes, start + 1) < 0,
                     "DATA content occurrence ambiguous in original")
            rows.append({"id": f"{context}-cl-relocated-data-{member}", "context": context,
                         "member": member, "segment": segname, "start": start,
                         "end": start + size, "size": size, "calibration_start": con["start"],
                         "raw_sha256": pin["raw_sha256"], "member_program_sha256": pin["program_sha256"],
                         "original_linked_sha256": sha(original_bytes),
                         "calibration_linked_sha256": sha(cal_bytes),
                         "omf_fixups": actions, "ordered_original_mz_fixups": mz,
                         "complete_ledatas": chunks})
    return {"schema_version": 1, "kind": "source-linked-complete-cl-initialized-data",
            "decision": "PROPOSAL", "library_sha256": sha(lib), "authored_credit": 0,
            "compiler_invocations": 0, "identities": identities(root), "targets": targets,
            "contributions": rows, "contribution_count": len(rows),
            "total_bytes": sum(row["size"] for row in rows)}


def validate_metadata(proof: dict, root: Path = ROOT) -> None:
    need(proof.get("schema_version") == 1 and
         proof.get("kind") == "source-linked-complete-cl-initialized-data" and
         proof.get("decision") == "PROPOSAL" and proof.get("library_sha256") ==
         LIB_PINS["library_sha256"] and proof.get("authored_credit") == 0 and
         proof.get("compiler_invocations") == 0 and proof.get("identities") == identities(root),
         "stale or misclassified relocated DATA evidence")
    targets = proof.get("targets")
    need(isinstance(targets, dict) and set(targets) == set(PARENTS), "missing target view")
    for context, target in targets.items():
        parent = json.loads((root / PARENTS[context]).read_text())
        need(target.get("artifact") == f"th05-{context}" and
             target.get("size") == (145958 if context == "main" else parent["target_payload_size"]) and
             target.get("payload_sha256") == parent["target_payload_sha256"] and
             target.get("calibration_exe_sha256") ==
             (parent["calibration_exe_sha256"] if context == "main" else parent["calibration"]["exe_sha256"]) and
             target.get("calibration_map_sha256") ==
             (parent["calibration_map_sha256"] if context == "main" else parent["calibration"]["map_sha256"]),
             "original/calibration parent changed")
    rows = proof.get("contributions")
    need(isinstance(rows, list) and len(rows) == len(MEMBERS) * len(PARENTS),
         "partial relocated DATA inventory")
    seen = set()
    for row in rows:
        context, member = row.get("context"), row.get("member")
        need(context in PARENTS and member in MEMBERS, "unknown relocated source")
        pin = MEMBERS[member]
        key = f"{context}-cl-relocated-data-{member}"
        need(row.get("id") == key and key not in seen and row.get("segment") == pin.get("segment", "_DATA")
             and row.get("size") == pin["size"] and
             row.get("start") == pin["starts"][context] and
             row.get("end") == row["start"] + pin["size"] <= targets[context]["size"] and
             row.get("member_program_sha256") == pin["program_sha256"] and
             row.get("raw_sha256") == pin["raw_sha256"], "incorrect complete relocated extent")
        seen.add(key)
        actions = row.get("omf_fixups")
        need(isinstance(actions, list) and
             [(a.get("site"), a.get("kind")) for a in actions] == pin["fixups"] and
             row.get("ordered_original_mz_fixups") ==
             [site + 2 for site, kind in pin["fixups"] if kind == 3],
             "unreviewed DATA fixup shape/order")
        for action in actions:
            need(("segment" in pin and action.get("frame_method") in (1, 4, 5) or
                  action.get("frame_method") == (1 if member == "files" else 5)) and
                 action.get("target_method") == 0 and
                 ("segment" in pin or action.get("target_index") == (2 if member == "files" else 1)) and
                 all(isinstance(action.get(field), str) and len(action[field]) == 64
                     for field in ("calibration_bytes_sha256", "original_bytes_sha256")),
                 "unsupported DATA fixup binding")
        need(isinstance(row.get("calibration_start"), int) and
             all(isinstance(row.get(field), str) and len(row[field]) == 64
                 for field in ("original_linked_sha256", "calibration_linked_sha256")) and
             isinstance(row.get("complete_ledatas"), list) and row["complete_ledatas"] and
             (pin.get("zero_gaps") or sum(c["size"] for c in row["complete_ledatas"]) == pin["size"]),
             "incomplete linked/LEDATA evidence")
    need(proof.get("contribution_count") == len(rows) and
         proof.get("total_bytes") == sum(r["size"] for r in rows), "DATA totals differ")


def reviewed_claims(root: Path, views: dict, *, verify_targets: bool = False) -> tuple[dict, str | None]:
    if not (root / DECISION).exists():
        return {}, None
    raw = (root / PROOF).read_bytes()
    proof = json.loads(raw)
    validate_metadata(proof, root)
    decision = json.loads((root / DECISION).read_text())
    selected = decision.get("units")
    proposed = {r["id"]: r for r in proof["contributions"]}
    need(decision.get("schema_version") == 1 and
         decision.get("classification") == "third-party-library-initialized-data" and
         decision.get("evidence_sha256") == sha(raw) and
         decision.get("authored_credit") == 0 and
         isinstance(selected, list) and len(selected) == len(proposed) and
         len(set(selected)) == len(selected) and set(selected) == set(proposed),
         "unreviewed or stale relocated DATA decision")
    if verify_targets:
        need(native_review(root) == proof, "native DATA link proof changed")
    claims = {context: [] for context in PARENTS}
    for key in selected:
        row = proposed[key]
        context = row["context"]
        need(views[context]["size"] == proof["targets"][context]["size"] and
             views[context]["sha256"] == proof["targets"][context]["payload_sha256"],
             "unrelated target view")
        claims[context].append({"start": row["start"], "end": row["end"],
                                "kind": "verified-vendor-initialized-data",
                                "content_kind": "library-initialized-data", "instruction_bytes": 0,
                                "library": "CL.LIB", "member": row["member"], "scope_id": key})
    return claims, sha((root / DECISION).read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    for command in ("write", "check", "structural-check"):
        g.add_argument("--" + command, action="store_true")
    args = ap.parse_args()
    if args.structural_check:
        validate_metadata(json.loads((ROOT / PROOF).read_text()))
        print("PASS: public CL relocated DATA structure (native bytes not replayed)")
    else:
        evidence = native_review()
        if args.write:
            (ROOT / PROOF).write_text(json.dumps(evidence, indent=2) + "\n")
        else:
            need(evidence == json.loads((ROOT / PROOF).read_text()), "native CL relocated DATA changed")
        print(f"PASS: {evidence['contribution_count']} complete relocated DATA scopes / "
              f"{evidence['total_bytes']} original bytes (zero authored credit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

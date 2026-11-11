#!/usr/bin/env python3
"""Reconstruct MAINE CL.LIB CODE through its original, shifted linker frames.

The retained calibration uses DGROUP=10100h and three C++ string method
entries six bytes earlier than the decoded original. The original target
contains independent segment-word and function-entry evidence for both
placements. Rebind the *original OMF source*, never copy linked target bytes.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
from types import MethodType

from lib.pc98 import digest_file
from review_context_remaining import reconstruct
from review_context_reserved import native_context
from review_vendor import PINS as LIB_PINS, need
from review_vendor_context import PINS as CONTEXT_PINS

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "config/maine_shifted_vendor.json"
DECISION = ROOT / "config/reviewed_maine_shifted_vendor.json"
MEMBERS = {"new": (754, 46), "xxas": (143, 3), "signal": (769, 55),
           "_pathops": (208, 7), "xmsg": (955, 49)}
CLASS_SYMBOLS = ("@string@$bctr$qmx6string", "@string@$bctr$qnxc",
                 "@string@$bdtr$qv")
ORIGINAL_DGROUP = 0x10110
STRING_CODE_SHIFT = 6


def actual_link_frames(view):
    need(view.groups["dgroup"] == 0x10100,
         "native MAINE calibration DGROUP differs from pinned reference")
    xxas = next(c for c in view.contribs if c["module"].casefold() == "xxas" and
                c["cl"] == "CODE")
    mod = view.mods["xxas"]
    group_fixups = [f for f in mod["fixups"] if f["segment"] == 1 and
                    f["target_method"] == 1]
    need(len(group_fixups) == 1 and group_fixups[0]["site"] == 42 and
         mod["groups"][group_fixups[0]["target_index"]]["name"] == "DGROUP",
         "original member has no authentic group-segment binding")
    f = group_fixups[0]
    source = next(b["data"] for b in mod["blocks"] if b["segment"] == 1)
    target_word = int.from_bytes(
        view.target.program_image[xxas["start"]+f["site"]:xxas["start"]+f["site"]+2], "little")
    source_word = int.from_bytes(source[f["site"]:f["site"]+2], "little")
    original_group = ((target_word-source_word) & 0xffff) * 16
    need(original_group == ORIGINAL_DGROUP,
         "original MAINE GRPDEF relocation does not resolve the observed DATA frame")
    # Independently check two other member source segment words in the target.
    signal = next(c for c in view.contribs if c["module"].casefold() == "signal" and
                  c["cl"] == "CODE")
    for site in (10,124,239):
        need(int.from_bytes(view.target.program_image[signal["start"]+site:
                 signal["start"]+site+2], "little") == ORIGINAL_DGROUP//16,
             "native MAINE original segment words disagree with DGROUP relocation")
    original_symbols = {}
    for symbol in CLASS_SYMBOLS:
        frame, off = view.external(symbol)
        start = frame+off
        prefix = view.cal.program_image[start:start+24]
        actual = view.target.program_image[start+STRING_CODE_SHIFT:
                                           start+STRING_CODE_SHIFT+24]
        need(len(prefix) == 24 and prefix == actual and
             prefix[:3] == b"\x55\x8b\xec" and
             view.target.program_image.find(prefix) == start+STRING_CODE_SHIFT,
             "original source-linked class method was not located independently")
        original_symbols[symbol] = {"calibration_entry": start,
                                    "original_entry": start+STRING_CODE_SHIFT}
    return original_symbols


def native_views():
    view, pins = native_context("maine")
    symbols = actual_link_frames(view)
    calibration = copy.copy(view)
    calibration.target = view.cal
    original = copy.copy(view)
    original.cal = view.target
    original.groups = {**view.groups, "dgroup": ORIGINAL_DGROUP}
    base_contribution = view.contribution
    base_external = view.external

    def shifted_contribution(self, mod, seg):
        row = base_contribution(mod, seg)
        if row["group"].casefold() == "dgroup":
            return {**row, "start": row["start"]+16, "frame": row["frame"]+16}
        return row

    def shifted_external(self, name):
        frame, offset = base_external(name)
        if frame == view.groups["dgroup"]:
            frame = ORIGINAL_DGROUP
        if name in symbols:
            offset += STRING_CODE_SHIFT
        return frame, offset

    original.contribution = MethodType(shifted_contribution, original)
    original.external = MethodType(shifted_external, original)
    return view, calibration, original, pins, symbols


def replay():
    view, cal, original, pins, symbols = native_views()
    rows = []
    for name,(size,count) in MEMBERS.items():
        candidates = [c for c in view.contribs if
                      c["module"].casefold() == name and c["cl"] == "CODE" and
                      c["size"] == size]
        need(len(candidates) == 1, "missing or ambiguous original CODE MAP contribution")
        c = candidates[0]
        baseline = reconstruct(cal, name, c["start"],size,count)
        native = reconstruct(original,name,c["start"],size,count)
        need(native["source_CODE_sha256"] == baseline["source_CODE_sha256"] and
             native["member_program_sha256"] == baseline["member_program_sha256"],
             "calibration and original do not use identical CL.LIB source CODE")
        native["calibration_linked_CODE_sha256"] = baseline["linked_CODE_sha256"]
        native["calibration_MZ_relocations"] = baseline["ordered_MZ_relocations"]
        rows.append(native)
    return {"schema_version":1, "kind":"maine-original-CL-code-shifted-link-context",
            "artifact":"th05-maine", "members":rows,
            "original_DGROUP_base": ORIGINAL_DGROUP,
            "calibration_DGROUP_base":view.groups["dgroup"],
            "shifted_original_class_methods":symbols,
            "source_written_CODE_bytes":sum(x["size"] for x in rows),
            "original_payload_sha256": pins["payload"],
            "packed_original_sha256":pins["packed"],
            "calibration_exe_sha256":pins["calibration_exe"],
            "calibration_map_sha256":pins["calibration_map"],
            "library_sha256":LIB_PINS["library_sha256"],
            "verifier_sha256":digest_file(ROOT/"scripts/review_maine_shifted_vendor.py"),
            "source_verifier_sha256":digest_file(ROOT/"scripts/review_context_remaining.py"),
            "authored_credit":0, "non_CODE_bytes_claimed":0}


def validate_public(record):
    pin=CONTEXT_PINS["maine"]
    need(record.get("schema_version")==1 and
         record.get("kind")=="maine-original-CL-code-shifted-link-context" and
         record.get("artifact")=="th05-maine" and
         record.get("original_DGROUP_base")==ORIGINAL_DGROUP and
         record.get("calibration_DGROUP_base")==0x10100 and
         record.get("original_payload_sha256")==pin["payload"] and
         record.get("packed_original_sha256")==pin["packed"] and
         record.get("calibration_exe_sha256")==pin["calibration_exe"] and
         record.get("calibration_map_sha256")==pin["calibration_map"] and
         record.get("library_sha256")==LIB_PINS["library_sha256"] and
         record.get("verifier_sha256")==digest_file(ROOT/"scripts/review_maine_shifted_vendor.py") and
         record.get("source_verifier_sha256")==digest_file(ROOT/"scripts/review_context_remaining.py") and
         record.get("authored_credit")==record.get("non_CODE_bytes_claimed")==0,
         "original symbol frames, source verifier or target identity changed")
    symbols=record.get("shifted_original_class_methods")
    need(isinstance(symbols,dict) and set(symbols)==set(CLASS_SYMBOLS) and
         all(isinstance(x.get("calibration_entry"),int) and
             x.get("original_entry")==x["calibration_entry"]+STRING_CODE_SHIFT
             for x in symbols.values()),"unreviewed original string method rebasing")
    rows=record.get("members",[])
    need([r.get("member") for r in rows]==list(MEMBERS) and
         record.get("source_written_CODE_bytes")==sum(x[0] for x in MEMBERS.values()),
         "unreviewed extra original vendor member")
    for row in rows:
        size,count=MEMBERS[row["member"]]
        need(row.get("size")==size and
             row.get("end")==row.get("start")+size and
             len(row.get("OMF_actions",[]))==count and
             sum(x.get("size",0) for x in row.get("LEDATA",[]))==size and
             row.get("authored_credit")==row.get("data_or_bss_bytes_claimed")==0 and
             isinstance(row.get("ordered_MZ_relocations"),list) and
             row.get("ordered_MZ_relocations")==row.get("calibration_MZ_relocations"),
             "original source extent, OMF fixups or relocations incomplete")
        for name in ("member_program_sha256","source_CODE_sha256","linked_CODE_sha256",
                     "calibration_linked_CODE_sha256"):
            need(isinstance(row.get(name),str) and re.fullmatch("[0-9a-f]{64}",row[name]),
                 "source/linked SHA256 missing")
    if DECISION.exists():
        dec=json.loads(DECISION.read_text())
        need(dec.get("schema_version")==1 and
             dec.get("artifact")=="th05-maine" and
             dec.get("decision")=="ADOPT_ONLY_COMPLETE_ORIGINAL_OMF_CODE" and
             dec.get("members")==list(MEMBERS) and
             dec.get("evidence_sha256")==digest_file(PROOF) and
             dec.get("source_CODE_bytes")==record["source_written_CODE_bytes"] and
             dec.get("authored_credit")==dec.get("non_CODE_bytes_claimed")==0,
             "explicit original CODE adoption differs from evidence")


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():
        return [], None
    need(root.resolve()==ROOT.resolve(), "wrong original reconstruction checkout")
    record=json.loads(PROOF.read_text())
    validate_public(record)
    need(view["sha256"]==record["original_payload_sha256"],
         "MAINE original decoded target identity differs")
    if verify_targets:
        need(replay()==record,"source rebind differs from original native MAINE CODE")
    return ([{"start":r["start"],"end":r["end"],"kind":"verified-vendor-code",
             "library":"CL.LIB","member":r["member"],"authored_credit":0}
            for r in record["members"]],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    a=p.add_mutually_exclusive_group(required=True)
    a.add_argument("--write",action="store_true")
    a.add_argument("--check",action="store_true")
    a.add_argument("--structural-check",action="store_true")
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             "refusing overwrite of accepted original provenance")
        record=replay()
        PROOF.write_text(json.dumps(record,indent=2)+"\n")
        print("PASS: complete original MAINE CL.LIB CODE:",record["source_written_CODE_bytes"])
    else:
        record=json.loads(PROOF.read_text())
        validate_public(record)
        if args.check:
            need(replay()==record,"original independent OMF linked-code evidence changed")
            print("PASS: original MAINE OMF CODE + original/calibration MZ fixups")
        else:
            print("PASS: current public MAINE linked-source record")

if __name__=="__main__":
    main()

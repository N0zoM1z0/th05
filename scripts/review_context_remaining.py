#!/usr/bin/env python3
"""Recover deferred OP/MAINE CL.LIB CODE from original OMF, not game bytes.

These members have complete CODE LEDATA. The older broad verifier deferred
GRPDEF-target FIXUPP and TLINK's far-JMP shortening; this focused review
resolves both from original source records and native MAP symbol frames.
_DATA, _BSS and _INIT_ contributions are intentionally outside this claim.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file
from lib.unit_oracle import relative_fixups
from review_context_reserved import native_context
from review_vendor import PINS as LIB_PINS, need, sha
from review_vendor_context import PINS as CONTEXT_PINS

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = {"op": {"xxas": (143, 3), "signal": (769, 55), "setenvp": (88, 10)},
           "maine": {"setenvp": (88, 10)}}


def proof_path(name):
    return ROOT / f"config/context_remaining.{name}.json"


def decision_path(name):
    return ROOT / f"config/reviewed_context_remaining.{name}.json"


def reconstruct(view, member, start, size, fixup_count):
    mod = view.mods[member]
    con = next((c for c in view.contribs if c["module"].casefold() == member and
                c["cl"] == "CODE" and c["start"] == start and c["size"] == size), None)
    need(con is not None, "original MAP CODE owner absent")
    indices = [i for i, s in enumerate(mod["segs"]) if s and
               s["name"] == con["segment"] and s["cl"] == "CODE"]
    need(len(indices) == 1 and mod["segs"][indices[0]]["size"] == size,
         "unreviewed original CODE SEGDEF")
    si = indices[0]
    code_blocks = [b for b in mod["blocks"] if b["segment"] == si]
    source = bytearray(size)
    coverage = bytearray(size)
    for b in code_blocks:
        low, high = b["offset"], b["offset"] + len(b["data"])
        need(0 <= low < high <= size and not any(coverage[low:high]),
             "original CODE LEDATA overlaps or exceeds SEGDEF")
        source[low:high] = b["data"]
        coverage[low:high] = b"\1" * (high-low)
    need(all(coverage), "original CODE source records have an unwritten hole")
    source_sha = sha(source)
    need(not set(mod["records"]) - {"THEADR", "COMENT", "LNAMES", "SEGDEF",
                                   "GRPDEF", "EXTDEF", "PUBDEF", "LEDATA",
                                   "FIXUPP", "MODEND", "ALIAS"},
         "original vendor member has an unreviewed transformation")
    data = bytearray(source)
    used = set()
    actions = []
    relocations = []
    code_frame = view.segbases[con["segment"].casefold()] // 16 * 16
    for f in mod["fixups"]:
        if f["segment"] != si:
            continue
        site, kind = f["site"], f["kind"]
        need(kind in (1, 2, 3), "unknown OMF fixup width")
        tm, ti = f["target_method"], f["target_index"]
        if tm == 0:
            target_con = view.contribution(mod, ti)
            target_seg = mod["segs"][ti]
            group = target_con["group"]
            target_frame = (view.groups[group.casefold()] if group != "(none)" else
                            view.segbases[target_seg["name"].casefold()] // 16 * 16)
            target_offset = target_con["start"] - target_frame
            binding = "segment:" + target_seg["name"]
        elif tm == 1:
            # OMF GRPDEF target carries the whole group frame and zero offset.
            need(0 < ti < len(mod["groups"]), "group target index invalid")
            group = mod["groups"][ti]
            target_frame = view.groups[group["name"].casefold()]
            target_offset = 0
            binding = "group:" + group["name"]
        elif tm == 2:
            need(0 < ti < len(mod["exts"]), "external target index invalid")
            symbol = mod["exts"][ti]
            target_frame, target_offset = view.external(symbol)
            binding = "external:" + symbol
        else:
            raise ValueError("unsupported native OMF FIXUPP target")
        fm = f["frame_method"]
        if fm == 5:
            frame = target_frame
        elif fm == 1:
            frame = view.groups[mod["groups"][f["frame_index"]]["name"].casefold()]
        elif fm == 0:
            frame = (view.segbases[mod["segs"][f["frame_index"]]["name"].casefold()]
                     // 16 * 16)
        else:
            raise ValueError("unsupported original OMF FIXUPP frame")
        old = int.from_bytes(data[site:site+2], "little")
        linear = target_frame + target_offset + f["displacement"]
        begin = site
        end = site + {1: 2, 2: 2, 3: 4}[kind]
        if kind == 1:
            value = old + linear - (con["start"]+site+2 if f["relative"] else frame)
            payload = (value & 0xffff).to_bytes(2, "little")
            operation = "relative16" if f["relative"] else "offset16"
        elif kind == 2:
            need(not f["relative"], "unreviewed relative segment FIXUPP")
            payload = ((old + frame//16) & 0xffff).to_bytes(2, "little")
            relocations.append(site)
            operation = "segment16"
        else:
            need(not f["relative"], "unreviewed relative far FIXUPP")
            old_segment = int.from_bytes(data[site+2:site+4], "little")
            segment = (old_segment + frame//16) & 0xffff
            if site and segment == code_frame//16 and data[site-1] in (0x9a, 0xea):
                displacement = (old + linear - (con["start"] + site + 4)) & 0xffff
                if data[site-1] == 0x9a:
                    payload = b"\x90\x0e\xe8" + displacement.to_bytes(2, "little")
                    operation = "TLINK-same-segment-far-call"
                else:
                    payload = b"\x90\x90\xe9" + displacement.to_bytes(2, "little")
                    operation = "TLINK-same-segment-far-jump"
                begin = site - 1
            else:
                off = (old + linear - frame) & 0xffff
                payload = off.to_bytes(2, "little") + segment.to_bytes(2, "little")
                relocations.append(site+2)
                operation = "far-pointer"
        need(end <= size and len(payload) == end-begin and
             not used.intersection(range(begin,end)),
             "CODE FIXUPP overlaps a prior source write")
        used.update(range(begin,end))
        data[begin:end] = payload
        actions.append({"site": site, "kind": kind, "binding": binding,
                        "operation": operation, "written_start": begin, "written_end": end,
                        "linked_sha256": sha(payload)})
    need(len(actions) == fixup_count, "original CODE FIXUPP records missing")
    linked = bytes(data)
    original = view.target.program_image[start:start+size]
    cal = view.cal.program_image[start:start+size]
    need(linked == original == cal, "source-resolved original/calibration CODE mismatch: " +
         member + " (" + str(sum(a != b for a,b in zip(linked, original))) + " bytes)")
    need(relative_fixups(view.target,start,size) == relocations and
         relative_fixups(view.cal,start,size) == relocations,
         "original ordered MZ relocations disagree with native OMF FIXUPP")
    need(view.target.program_image.find(original) == start and
         view.target.program_image.find(original,start+1) < 0,
         "original complete vendor CODE occurrence ambiguous")
    return {"member": member, "start": start, "end": start+size, "size": size,
            "member_program_sha256": mod["program_sha256"],
            "source_CODE_sha256": source_sha, "linked_CODE_sha256": sha(linked),
            "LEDATA": [{"offset": b["offset"], "size": len(b["data"]),
                         "sha256": sha(b["data"])} for b in code_blocks],
            "ordered_MZ_relocations": relocations, "OMF_actions": actions,
            "data_or_bss_bytes_claimed": 0, "authored_credit": 0}


def replay(name):
    need(name in MEMBERS, "unknown artifact")
    view, pin = native_context(name)
    old = json.loads((ROOT/f"config/vendor_ownership.{name}.json").read_text())
    deferred = {x["member"]:x for x in old["deferred"]}
    rows = []
    for member, (size, count) in MEMBERS[name].items():
        need(member in deferred and deferred[member]["size"] == size,
             "this original CL.LIB member was not deferred at this extent")
        x = reconstruct(view, member, deferred[member]["start"], size, count)
        need(x["member_program_sha256"] == deferred[member]["member_program_sha256"],
             "original member is not the pinned CL.LIB object")
        rows.append(x)
    return {"schema_version": 1, "kind": "original-omf-remaining-code",
            "artifact": "th05-"+name, "members": rows,
            "source_written_CODE_bytes": sum(x["size"] for x in rows),
            "original_payload_sha256": pin["payload"],
            "packed_original_sha256": pin["packed"],
            "calibration_exe_sha256": pin["calibration_exe"],
            "calibration_map_sha256": pin["calibration_map"],
            "library_sha256": LIB_PINS["library_sha256"],
            "verifier_sha256": digest_file(ROOT/"scripts/review_context_remaining.py"),
            "source_parser_sha256": digest_file(ROOT/"scripts/review_vendor.py"),
            "non_CODE_bytes_claimed": 0, "authored_credit": 0}


def validate_public(record,name):
    need(name in MEMBERS and record.get("schema_version") == 1 and
         record.get("kind") == "original-omf-remaining-code" and
         record.get("artifact") == "th05-"+name and
         record.get("library_sha256") == LIB_PINS["library_sha256"] and
         record.get("original_payload_sha256") == CONTEXT_PINS[name]["payload"] and
         record.get("packed_original_sha256") == CONTEXT_PINS[name]["packed"] and
         record.get("calibration_exe_sha256") == CONTEXT_PINS[name]["calibration_exe"] and
         record.get("calibration_map_sha256") == CONTEXT_PINS[name]["calibration_map"] and
         record.get("verifier_sha256") == digest_file(ROOT/"scripts/review_context_remaining.py") and
         record.get("source_parser_sha256") == digest_file(ROOT/"scripts/review_vendor.py") and
         record.get("non_CODE_bytes_claimed") == record.get("authored_credit") == 0,
         "remaining vendor source or pinned verifier identity drift")
    deferred = {x["member"]:x for x in json.loads(
        (ROOT/f"config/vendor_ownership.{name}.json").read_text())["deferred"]}
    members = record.get("members")
    need(isinstance(members,list) and [x.get("member") for x in members] == list(MEMBERS[name]),
         "non-reviewed CL.LIB member added")
    for x in members:
        member=x["member"]
        size, fixups=MEMBERS[name][member]
        need((x.get("start"),x.get("end"),x.get("size")) ==
             (deferred[member]["start"],deferred[member]["end"],size) and
             x.get("member_program_sha256")==deferred[member]["member_program_sha256"] and
             x.get("authored_credit")==x.get("data_or_bss_bytes_claimed")==0 and
             len(x.get("OMF_actions",[]))==fixups and
             sum(b.get("size",0) for b in x.get("LEDATA",[]))==size and
             isinstance(x.get("ordered_MZ_relocations"),list),
             "unreviewed member extent, source records, or FIXUPP count")
        for digest in [x.get("source_CODE_sha256"), x.get("linked_CODE_sha256")] + [
                z.get("sha256") for z in x["LEDATA"]] + [
                z.get("linked_sha256") for z in x["OMF_actions"]]:
            need(isinstance(digest,str) and re.fullmatch("[0-9a-f]{64}",digest),
                 "bad linked or source OMF digest")
    need(record.get("source_written_CODE_bytes")==sum(size for size,_ in MEMBERS[name].values()),
         "source CODE total not reviewed")
    if decision_path(name).exists():
        d=json.loads(decision_path(name).read_text())
        need(d.get("schema_version")==1 and d.get("artifact")=="th05-"+name and
             d.get("decision")=="ADOPT_ONLY_COMPLETE_ORIGINAL_OMF_CODE" and
             d.get("evidence_sha256")==digest_file(proof_path(name)) and
             d.get("members")==list(MEMBERS[name]) and
             d.get("source_CODE_bytes")==record["source_written_CODE_bytes"] and
             d.get("authored_credit")==0 and d.get("non_CODE_bytes_claimed")==0,
             "explicit original vendor review selection differs")


def reviewed_claims(root,name,view,*,verify_targets=False):
    if name not in MEMBERS or not decision_path(name).exists():
        return [],None
    need(root.resolve()==ROOT.resolve(), "wrong original review checkout")
    record=json.loads(proof_path(name).read_text())
    validate_public(record,name)
    need(record["original_payload_sha256"]==view["sha256"],
         "remaining original vendor CODE belongs to different decoded payload")
    if verify_targets:
        need(replay(name)==record, "real original OMF/MAP native binding proof differs")
    return ([{"start":x["start"],"end":x["end"],"kind":"verified-vendor-code",
             "library":"CL.LIB","member":x["member"],"authored_credit":0}
            for x in record["members"]], digest_file(decision_path(name)))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--context",required=True,choices=MEMBERS)
    modes=p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write",action="store_true")
    modes.add_argument("--check",action="store_true")
    modes.add_argument("--structural-check",action="store_true")
    args=p.parse_args()
    path=proof_path(args.context)
    if args.write:
        need(not path.exists() and not decision_path(args.context).exists(),
             "original reviewer cannot overwrite existing evidence")
        result=replay(args.context)
        path.write_text(json.dumps(result,indent=2)+"\n")
        print("PASS: exact original",args.context,
              result["source_written_CODE_bytes"],"complete vendor CODE bytes")
    else:
        record=json.loads(path.read_text())
        validate_public(record,args.context)
        if args.check:
            need(replay(args.context)==record,"native linked original CODE differs")
            print("PASS: original OMF source, ordered fixups, linked CODE:",args.context)
        else:
            print("PASS: structural original CODE ledger:",args.context)


if __name__=="__main__":
    main()

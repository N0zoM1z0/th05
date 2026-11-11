#!/usr/bin/env python3
"""Review five complete MAIN CL.LIB CODE owners in the original link context.

The source is the authentic library's CODE LEDATA/FIXUPP. The original
C0L/DGROUP frame, foreign DATA/BSS offsets, and string-method entries differ
from the native calibration. Derive all shifts from the actual linked OMF
sites and function prologues, then resolve the entire CODE and ordered MZ
relocation scope in both original and retained calibration independently.
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
from review_vendor import PINS, need
from review_vendor_reserved import load_native

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "config/main_shifted_vendor.json"
DECISION = ROOT / "config/reviewed_main_shifted_vendor.json"
MEMBERS = {"new": (754, 46), "xxas": (143, 3), "signal": (769, 55),
           "_pathops": (208, 7), "xmsg": (955, 49)}
STRING_METHODS = ("@string@$bdtr$qv", "@string@$bctr$qnxc",
                  "@string@$bctr$qmx6string")

# _pathops already has an independent complete vendor owner in MAIN's
# earlier runtime review; reverify it here for context, never double-adopt.
SELECTED = ("new", "xxas", "signal", "xmsg")


def code_contribution(view, member):
    size, _ = MEMBERS[member]
    items = [c for c in view.contribs if c["module"].casefold() == member and
             c["cl"] == "CODE" and c["size"] == size]
    need(len(items) == 1, "missing/ambiguous actual original CODE MAP owner " + member)
    return items[0]


def source_word(mod, site):
    blocks = [b for b in mod["blocks"] if b["segment"] == 1]
    hits = [b for b in blocks if b["offset"] <= site and
            site+2 <= b["offset"]+len(b["data"])]
    need(len(hits) == 1, "original source FIXUPP has no complete LEDATA")
    b = hits[0]
    a = site-b["offset"]
    return int.from_bytes(b["data"][a:a+2], "little")


def linked_word(view, member, site, *, original):
    base = code_contribution(view,member)["start"]+site
    raw = view.target.program_image if original else view.cal.program_image
    return int.from_bytes(raw[base:base+2], "little")


def observed_frames(view):
    group_fix = next(f for f in view.mods["xxas"]["fixups"]
                     if f["segment"] == 1 and f["site"] == 42 and
                     f["target_method"] == 1 and f["kind"] == 2)
    need(view.mods["xxas"]["groups"][group_fix["target_index"]]["name"] == "DGROUP",
         "original xxas does not reference the authentic DGROUP")
    original_group = (
        (linked_word(view,"xxas",42,original=True) -
         source_word(view.mods["xxas"],42)) & 0xffff) * 16
    group_delta = original_group-view.groups["dgroup"]
    need((original_group,view.groups["dgroup"],group_delta)==
         (0x209D0,0x209E0,-16),
         "original MAIN DGROUP shift lacks real group-segment evidence")
    for site in (10,124,239):
        need(linked_word(view,"signal",site,original=True)==original_group//16,
             "original MAIN signal handler segment relocation disagrees with xxas")
    # These are genuine linked CODE offset16 sites, not arbitrary target samples.
    own_data = [("new",0x47),("signal",0x15),("_pathops",0x0d)]
    own_bss = [("signal",0x13b),("signal",0x13f),("signal",0x208)]
    data_deltas = [((linked_word(view,m,s,original=True)-
                     linked_word(view,m,s,original=False)+0x8000)&0xffff)-0x8000
                   for m,s in own_data]
    bss_deltas = [((linked_word(view,m,s,original=True)-
                    linked_word(view,m,s,original=False)+0x8000)&0xffff)-0x8000
                  for m,s in own_bss]
    need(data_deltas==[-18]*3 and bss_deltas==[-20]*3,
         "original OMF DATA/BSS source-linked positions are inconsistent")
    data_delta,bss_delta=data_deltas[0],bss_deltas[0]
    # Distinguish _TEXTC class frame relocation from the method's offset
    # using the *source* far pointer FIXUPP and actual linked segment word.
    segments={}
    for member in ("new","xmsg"):
        mod=view.mods[member]
        for f in mod["fixups"]:
            if f["segment"] != 1 or f["kind"] != 3 or f["target_method"] != 2:
                continue
            symbol=mod["exts"][f["target_index"]]
            if symbol not in STRING_METHODS:
                continue
            need(f["frame_method"] == 5 and not f["relative"],
                 "original string method is not an ordinary 16:16 binding")
            low=code_contribution(view,member)["start"]+f["site"]+2
            source_segment=source_word(mod,f["site"]+2)
            linked_segment=int.from_bytes(view.target.program_image[low:low+2],"little")
            frame=((linked_segment-source_segment)&0xffff)*16
            segments.setdefault(symbol,set()).add(frame)
    need(set(segments)==set(STRING_METHODS) and
         all(len(frames)==1 for frames in segments.values()),
         "original string function segment frame is not independently bound")
    methods={}
    for symbol in STRING_METHODS:
        source_frame,cal_off=view.external(symbol)
        source_start=source_frame+cal_off
        prologue=view.cal.program_image[source_start:source_start+24]
        target_start=view.target.program_image.find(prologue)
        need(prologue[:3]==b"\x55\x8b\xec" and
             target_start>=0 and
             view.target.program_image.find(prologue,target_start+1)<0,
             "original native C++ string method entry is not uniquely located")
        frame=next(iter(segments[symbol]))
        delta=target_start-source_start
        need((frame-source_frame,delta)==(-16,-19),
             "original class entry relocation is inconsistent with original machine code")
        methods[symbol]={"calibration_entry":source_start,
                         "original_entry":target_start,
                         "original_segment_frame":frame,
                         "original_segment_offset":target_start-frame}
    return original_group,group_delta,data_delta,bss_delta,methods


def native_views():
    view=load_native()
    group,group_delta,data_delta,bss_delta,methods=observed_frames(view)
    cal=copy.copy(view)
    cal.target=view.cal
    orig=copy.copy(view)
    orig.cal=view.target
    orig.groups={**view.groups,"dgroup":group}
    original_contribution=view.contribution
    original_external=view.external

    def shifted_contribution(self,mod,si):
        c=original_contribution(mod,si)
        if c["group"].casefold() != "dgroup":
            return c
        cl=mod["segs"][si]["cl"]
        delta=group_delta+(data_delta if cl=="DATA" else
                           bss_delta if cl=="BSS" else 0)
        return {**c,"frame":c["frame"]+group_delta,"start":c["start"]+delta}

    def shifted_external(self,name):
        frame,off=original_external(name)
        if name in methods:
            return (methods[name]["original_segment_frame"],
                    methods[name]["original_segment_offset"])
        if frame==view.groups["dgroup"]:
            return group,off+(bss_delta if name=="___SignalPtr" else 0)
        return frame,off

    orig.contribution=MethodType(shifted_contribution,orig)
    orig.external=MethodType(shifted_external,orig)
    return view,cal,orig,group,data_delta,bss_delta,methods


def replay():
    view,cal,original,group,data_delta,bss_delta,methods=native_views()
    rows=[]
    for member,(size,fixups) in MEMBERS.items():
        c=code_contribution(view,member)
        calibrated=reconstruct(cal,member,c["start"],size,fixups)
        native=reconstruct(original,member,c["start"],size,fixups)
        need(calibrated["source_CODE_sha256"]==native["source_CODE_sha256"] and
             calibrated["member_program_sha256"]==native["member_program_sha256"] and
             calibrated["ordered_MZ_relocations"]==native["ordered_MZ_relocations"],
             "original/calibration OMF owner, source or relocation order differs")
        native["calibration_linked_CODE_sha256"]=calibrated["linked_CODE_sha256"]
        native["calibration_MZ_relocations"]=calibrated["ordered_MZ_relocations"]
        rows.append(native)
    return {"schema_version":1,"kind":"main-original-CL-source-CODE-link-frame-recovery",
            "artifact":"th05-main","members":rows,
            "original_DGROUP_base":group,
            "calibration_DGROUP_base":view.groups["dgroup"],
            "original_DATA_offset_delta":data_delta,
            "original_BSS_offset_delta":bss_delta,
            "string_method_entries":methods,
            "original_target_sha256":PINS["target_sha256"],
            "original_payload_sha256":PINS["target_payload_sha256"],
            "calibration_map_sha256":PINS["calibration_map_sha256"],
            "library_sha256":PINS["library_sha256"],
            "verifier_sha256":digest_file(ROOT/"scripts/review_main_shifted_vendor.py"),
            "source_verifier_sha256":digest_file(ROOT/"scripts/review_context_remaining.py"),
            "source_parser_sha256":digest_file(ROOT/"scripts/review_vendor.py"),
            "source_written_CODE_bytes":sum(x["size"] for x in rows),
            "other_source_bytes_claimed":0,"authored_credit":0}


def validate_public(record):
    need(record.get("schema_version")==1 and
         record.get("kind")=="main-original-CL-source-CODE-link-frame-recovery" and
         record.get("artifact")=="th05-main" and
         record.get("original_DGROUP_base")==0x209D0 and
         record.get("calibration_DGROUP_base")==0x209E0 and
         record.get("original_DATA_offset_delta")==-18 and
         record.get("original_BSS_offset_delta")==-20 and
         record.get("original_target_sha256")==PINS["target_sha256"] and
         record.get("original_payload_sha256")==PINS["target_payload_sha256"] and
         record.get("calibration_map_sha256")==PINS["calibration_map_sha256"] and
         record.get("library_sha256")==PINS["library_sha256"] and
         record.get("verifier_sha256")==digest_file(ROOT/"scripts/review_main_shifted_vendor.py") and
         record.get("source_verifier_sha256")==digest_file(ROOT/"scripts/review_context_remaining.py") and
         record.get("source_parser_sha256")==digest_file(ROOT/"scripts/review_vendor.py") and
         record.get("other_source_bytes_claimed")==record.get("authored_credit")==0,
         "reviewed MAIN CL source context or pinned native verifier changed")
    methods=record.get("string_method_entries")
    need(isinstance(methods,dict) and set(methods)==set(STRING_METHODS) and
         all(isinstance(v.get("calibration_entry"),int) and
             v.get("original_entry")==v["calibration_entry"]-19 and
             v.get("original_segment_frame")==0x1fd70 and
             v.get("original_segment_offset")==v["original_entry"]-0x1fd70
             for v in methods.values()),
         "original MAIN class frame/method entry evidence incomplete")
    rows=record.get("members")
    need(isinstance(rows,list) and [x.get("member") for x in rows]==list(MEMBERS) and
         record.get("source_written_CODE_bytes")==sum(x[0] for x in MEMBERS.values()),
         "reviewed MAIN original CL CODE member list/size differs")
    for r in rows:
        sz,n=MEMBERS[r["member"]]
        need(r.get("size")==sz and r.get("end")==r.get("start")+sz and
             r.get("authored_credit")==r.get("data_or_bss_bytes_claimed")==0 and
             sum(x.get("size",0) for x in r.get("LEDATA",[]))==sz and
             len(r.get("OMF_actions",[]))==n and
             r.get("ordered_MZ_relocations")==r.get("calibration_MZ_relocations"),
             "source bytes/OMF actions/relocations incomplete")
        for key in ("member_program_sha256","source_CODE_sha256",
                    "linked_CODE_sha256","calibration_linked_CODE_sha256"):
            need(isinstance(r.get(key),str) and re.fullmatch("[0-9a-f]{64}",r[key]),
                 "invalid native original CODE digest")
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get("schema_version")==1 and d.get("artifact")=="th05-main" and
             d.get("decision")=="ADOPT_ONLY_COMPLETE_ORIGINAL_OMF_CODE" and
             d.get("members")==list(SELECTED) and
             d.get("evidence_sha256")==digest_file(PROOF) and
             d.get("source_CODE_bytes")==sum(MEMBERS[m][0] for m in SELECTED) and
             d.get("authored_credit")==d.get("other_source_bytes_claimed")==0,
             "explicit original MAIN vendor decision missing/stale")


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():
        return [],None
    need(root.resolve()==ROOT.resolve(),"wrong source-reconstruction checkout")
    record=json.loads(PROOF.read_text());validate_public(record)
    need(view["sha256"]==record["original_payload_sha256"],
         "reviewed CODE is for another original MAIN target")
    if verify_targets:
        need(replay()==record,"original source OMF CODE replay differs")
    return ([{"start":x["start"],"end":x["end"],"kind":"verified-vendor-code",
             "library":"CL.LIB","member":x["member"],"authored_credit":0}
            for x in record["members"] if x["member"] in SELECTED],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write",action="store_true")
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--structural-check",action="store_true")
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             "refusing to overwrite an already reviewed original source")
        record=replay()
        PROOF.write_text(json.dumps(record,indent=2)+"\n")
        print("PASS: complete MAIN original CL CODE:",record["source_written_CODE_bytes"])
    else:
        record=json.loads(PROOF.read_text());validate_public(record)
        if args.check:
            need(replay()==record,"real source-linked original/MAIN calibration differs")
            print("PASS: original MAIN OMF CODE and original/calibrated ordered fixups")
        else:
            print("PASS: current public MAIN vendor source proof")


if __name__=="__main__":
    main()

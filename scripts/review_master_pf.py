#!/usr/bin/env python3
"""Recover native Master PFINT21/PFOPEN CODE without claiming a writable slot.

Five complete source-LEDATA ranges cover three whole procedures and the two
written parts of the 351-byte pfint21 hook. Its default dw ?, _Thru
word was deliberately not emitted in OMF LEDATA, so it stays unknown.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_oracle import relative_fixups
from review_master import need, object_text, pinned, sha, source_blocks, stored_lzh
from review_master_bgm import linked_scope

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "config/master_vendor_ownership.json"
PROOF = ROOT / "config/master_pf_ownership.json"
DECISION = ROOT / "config/reviewed_master_pf.json"
WRITTEN = (
    ("PFSTART", 0x4288, 160),
    ("PFEND", 0x4328, 56),
    ("pfint21", 0x4360, 100),
    ("pfint21", 0x43c6, 249),
    ("PFOPEN", 0x44c0, 240),
)
GAP = (0x43c4, 2)
PAD = 0x44bf


def replay():
    parent = json.loads(PARENT.read_text())
    archive = stored_lzh(pinned(ROOT, parent["inputs"]["inner_archive"]))
    source_root = ROOT / parent["candidate_source_root"]
    frozen = {r["name"]:r["sha256"] for r in parent["frozen_source_closure"]}
    assembly = object_text(pinned(ROOT, parent["inputs"]["saved_object"]))
    calibrated = parse_mz(pinned(ROOT, parent["inputs"]["calibration_exe"]))
    original = parse_mz(pinned(ROOT, parent["inputs"]["target"]))
    sources = {}
    for name, path, origfile in (
        ("PFSTART", "libs/master.lib/pfint21.asm", "PFINT21.ASM"),
        ("PFEND", "libs/master.lib/pfint21.asm", "PFINT21.ASM"),
        ("pfint21", "libs/master.lib/pfint21.asm", "PFINT21.ASM"),
        ("PFOPEN", "th03/formats/pfopen.asm", "PFOPEN.ASM"),
    ):
        compiled = (source_root/path).read_bytes()
        need(sha(compiled) == frozen[path], "genuine TASM native source drifted")
        native_blocks = [v for v in source_blocks(compiled, "utf8") if v["name"]==name]
        author_blocks = [v for v in source_blocks(archive[origfile], "cp932")
                         if v["name"].casefold()==name.casefold()]
        need(len(native_blocks)==len(author_blocks)==1,
             "incomplete native/author Master PF procedure source")
        sources[name] = {
            "native_source":path,
            "native_source_sha256":sha(compiled),
            "native_procedure_sha256":sha(native_blocks[0]["text"].encode("utf8")),
            "author_archive_member":origfile,
            "author_procedure_sha256":sha(author_blocks[0]["text"].encode("utf8")),
            "source_adaptation":"ReC98 TH05 GAME=5 assembler port; original 0.23 code is not claimed identical",
        }
    # The original upstream and active TASM source independently declare
    # a runtime-written dispatch sentinel, not two initialized machine bytes.
    for file, encoding in ((source_root/"libs/master.lib/pfint21.asm","utf8"),
                           (None,"cp932")):
        content = (file.read_bytes() if file else archive["PFINT21.ASM"]).decode(encoding).lower()
        need(any("default" in line.split(";")[0] and
                 "dw" in line.split(";")[0] and "?" in line.split(";")[0]
                 for line in content.splitlines()),
             "source has no uninitialized runtime dispatch word")
    offset,length = GAP
    low = offset - 0x272
    need(not any(low < block["offset"]+len(block["content"]) and
                 low+length > block["offset"] for block in assembly["blocks"]),
         "writable dispatch word was emitted as initialized OMF CODE")
    need(original.program_image[offset:offset+length] ==
         calibrated.program_image[offset:offset+length] == b"\0\0",
         "original linker bytes differ in separately unowned dispatch slot")
    need(original.program_image[PAD] == calibrated.program_image[PAD] == 0,
         "external one-byte assembler alignment differs")
    ranges = []
    for name, start, size in WRITTEN:
        cal, native, objhash, relocs, actions = linked_scope(assembly,start,size)
        need(cal==calibrated.program_image[start:start+size] and
             native==original.program_image[start:start+size],
             "complete original source-written Master PF CODE differs")
        need(relocs == relative_fixups(calibrated,start,size) ==
             relative_fixups(original,start,size),
             "original ordered MZ segment fixups differ")
        ranges.append({
            "name":name,"start":start,"end":start+size,"size":size,
            "native_source":sources[name],
            "source_unlinked_CODE_sha256":objhash,
            "original_linked_CODE_sha256":sha(native),
            "ordered_original_MZ":relocs,
            "source_OMF_fixup_count":len(actions),
            "authored_credit":0,
        })
    return {
        "schema_version":1,
        "kind":"original-Master-PF-source-CODE-and-uninitialized-dispatch",
        "artifact":"th05-main",
        "ranges":ranges,
        "source_written_CODE_bytes":sum(x["size"] for x in ranges),
        "unowned_dispatch_word":{"start":offset,"size":length},
        "unowned_alignment":{"start":PAD,"size":1},
        "parent_review_sha256":digest_file(PARENT),
        "verifier_sha256":digest_file(ROOT/"scripts/review_master_pf.py"),
        "authored_credit":0,
    }


def validate_public(proof):
    need(proof.get("schema_version")==1 and
         proof.get("kind")=="original-Master-PF-source-CODE-and-uninitialized-dispatch" and
         proof.get("artifact")=="th05-main" and
         proof.get("source_written_CODE_bytes")==805 and
         proof.get("unowned_dispatch_word")=={"start":GAP[0],"size":GAP[1]} and
         proof.get("unowned_alignment")=={"start":PAD,"size":1} and
         proof.get("parent_review_sha256")==digest_file(PARENT) and
         proof.get("verifier_sha256")==digest_file(ROOT/"scripts/review_master_pf.py") and
         proof.get("authored_credit")==0, "unreviewed Master PF code proof")
    ranges=proof.get("ranges",[])
    need([(x.get("name"),x.get("start"),x.get("size")) for x in ranges]==list(WRITTEN),
         "unknown or incomplete original Master PF CODE range")
    for row in ranges:
        need(row["end"]==row["start"]+row["size"] and
             row.get("authored_credit")==0 and
             isinstance(row.get("ordered_original_MZ"),list),
             "PF source-written byte extent or MZ relocations incomplete")
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get("decision")=="ADOPT_ONLY_PF_SOURCE_WRITTEN_CODE" and
             d.get("evidence_sha256")==digest_file(PROOF) and
             d.get("source_written_CODE_bytes")==805 and
             d.get("authored_credit")==0,
             "explicit PF ownership review is stale")


def reviewed_claims(root,view,*,verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),"wrong original source checkout")
    proof=json.loads(PROOF.read_text());validate_public(proof)
    if verify_targets:need(replay()==proof,"native PF source or target changed")
    return ([{"start":x["start"],"end":x["end"],"kind":"verified-vendor-code",
              "library":"Master 0.23-derived GAME=5","member":x["name"],
              "authored_credit":0} for x in proof["ranges"]],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--write",action="store_true")
    m.add_argument("--check",action="store_true")
    m.add_argument("--structural-check",action="store_true")
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),"cannot overwrite reviewed PF proof")
        data=replay();PROOF.write_text(json.dumps(data,indent=2)+"\n")
        print("PASS: source-written PF CODE",data["source_written_CODE_bytes"])
    else:
        data=json.loads(PROOF.read_text());validate_public(data)
        if args.check:need(replay()==data,"original source PF code differs")
        print("PASS: source and original PF code, retained runtime slot")
if __name__=="__main__": main()

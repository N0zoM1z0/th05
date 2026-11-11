#!/usr/bin/env python3
"""Complete source-backed 16-bit Master machine-detection and I/O procedures.

Compare original author Master ASM against the genuine TASM input, with only
specific branch-range and macro spellings normalized. Original and calibration
linked CODE and MZ relocations must match every byte of each full procedure.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from lib.pc98 import digest_file, parse_mz
from lib.unit_oracle import relative_fixups
from review_master import need, pinned, sha, source_blocks, stored_lzh, object_text
from review_master_bgm import linked_scope

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "config/master_vendor_ownership.json"
PROOF = ROOT / "config/master_machine_ownership.json"
DECISION = ROOT / "config/reviewed_master_machine.json"
MEMBERS = (
    ("PALETTE_BLACK_IN", 0x0600, 68),
    ("PALETTE_BLACK_OUT", 0x0644, 62),
    ("BOPENR", 0x0682, 84),
    ("BREAD", 0x06d6, 48),
    ("GET_MACHINE_98", 0x1b4a, 126),
    ("GET_MACHINE_AT", 0x1bc8, 342),
    ("GET_MACHINE_DOSBOX", 0x1d1e, 50),
)
BRANCHES = {
    ("jnzzun1", "jmpget_at_machine_exit", "zun1:"):
        "jeget_at_machine_exit",
    ("jzzun2", "jmpnot_dosv", "zun2:"):
        "jnznot_dosv",
    ("jzzun3", "jmpnot_dosv", "zun3:"):
        "jnznot_dosv",
}


def tokens(text):
    return [re.sub(r"\s+", "", s.split(";", 1)[0].lower().replace("@@", ""))
            for s in text.splitlines() if s.split(";", 1)[0].strip()]


def canonical(text, name, *, compiled):
    x = tokens(text)
    if not compiled:
        return x
    out = []
    i = 0
    while i < len(x):
        tri = tuple(x[i:i+3])
        if name == "BOPENR" and tri == (
                "ifldata", "pushwordptr[bp+fname+2]", "endif"):
            out.append("_push[bp+fname+2]")
            i += 3
            continue
        if name == "GET_MACHINE_AT" and tri in BRANCHES:
            out.append(BRANCHES[tri])
            i += 3
            continue
        t = x[i]
        t = t.replace("nopcall", "call")
        if name == "BOPENR":
            t = t.replace("movbyteptrpferrno,", "movpferrno,")
            t = t.replace("pushwordptr[bp+fname]", "push[bp+fname]")
        if name == "BREAD":
            t = t.replace("pushwordptr[bp+bf]", "push[bp+bf]")
        if name == "GET_MACHINE_98":
            t = t.replace("movax,fmr_98", "movax,fmr")
            t = t.replace("db0e9h,057h,001h", "jmpget_machine_dosbox")
        if name == "GET_MACHINE_AT":
            t = t.replace("movax,fmr_at", "movax,fmr")
            t = t.replace("db0e9h,001h,000h", "jmpget_machine_dosbox")
        out.append(t)
        i += 1
    return out


def evidence():
    parent = json.loads(PARENT.read_text())
    archive = stored_lzh(pinned(ROOT, parent["inputs"]["inner_archive"]))
    source_index = {}
    for filename, raw in archive.items():
        if not filename.upper().endswith(".ASM"):
            continue
        try:
            parts = source_blocks(raw, "cp932")
        except UnicodeDecodeError:
            continue
        for part in parts:
            source_index.setdefault(part["name"].lower(), []).append(
                (filename, part["text"]))
    binary = parse_mz(pinned(ROOT, parent["inputs"]["target"]))
    calibration = parse_mz(pinned(ROOT, parent["inputs"]["calibration_exe"]))
    omf = object_text(pinned(ROOT, parent["inputs"]["saved_object"]))
    inventory = {x["name"]: x for x in parent["active_procedure_inventory"]}
    frozen = {x["name"]:x for x in parent["frozen_source_closure"]}
    out = []
    for name, start, size in MEMBERS:
        bound = inventory[name]
        need((bound["start"], bound["end"]) == (start, start+size),
             "original native function boundaries differ: "+name)
        file = bound["source"]
        src = (ROOT/parent["candidate_source_root"]/file).read_bytes()
        need(file in frozen and sha(src) == frozen[file]["sha256"],
             "actual original source-built file differs")
        compiled = [r["text"] for r in source_blocks(src, "utf8")
                    if r["name"] == name]
        original = source_index.get(name.lower(), [])
        need(len(compiled)==1 and bool(original), "missing native Master original source")
        second = canonical(compiled[0], name, compiled=True)
        matching = [(f,ref) for f,ref in original
                    if canonical(ref, name, compiled=False)==second]
        need(len(matching)==1, "original Master instruction operands differ or source ambiguous: "+name)
        ref_file, ref = matching[0]
        first = canonical(ref, name, compiled=False)
        built, native, objsha, fixups, actions = linked_scope(omf, start, size)
        need(built == calibration.program_image[start:start+size] and
             native == binary.program_image[start:start+size],
             "complete original Master CODE does not match: "+name)
        need(fixups == relative_fixups(calibration,start,size) ==
             relative_fixups(binary,start,size), "original ordered relocations differ")
        need(binary.program_image.find(native)==start and
             binary.program_image.find(native,start+1)<0, "original CODE ambiguous")
        if name in ("GET_MACHINE_98", "GET_MACHINE_AT"):
            # The adaptation's explicit E9 words are real relative JMPs to the
            # independently source-named GET_MACHINE_DOSBOX public. They must
            # not become arbitrary machine-code constants.
            offset = {"GET_MACHINE_98":0x1bc4, "GET_MACHINE_AT":0x1d1a}[name]
            jump = native[offset-start:offset-start+3]
            need(jump[0] == 0xe9 and
                 offset + 3 + int.from_bytes(jump[1:3],"little",signed=True)==0x1d1e,
                 "TASM adapted jump does not reach original named DOSBOX routine")
        out.append({"member":name,"start":start,"end":start+size,"size":size,
                    "author_archive_member":ref_file,
                    "author_source_sha256":sha(ref.encode("utf8")),
                    "native_source":file,"native_source_sha256":sha(src),
                    "normalized_source_sha256":sha("\n".join(first).encode("utf8")),
                    "object_CODE_sha256":objsha,"original_CODE_sha256":sha(native),
                    "ordered_MZ":fixups,"fixup_count":len(actions),
                    "authored_credit":0})
    return {"schema_version":1,"kind":"original-Master-machine-and-buffered-IO",
            "members":out,"source_written_CODE_bytes":sum(z["size"] for z in out),
            "original_parent_sha256":digest_file(PARENT),
            "verifier_sha256":digest_file(ROOT/"scripts/review_master_machine.py"),
            "authored_credit":0}


def public_check(record):
    need(record.get("schema_version")==1 and
         record.get("kind")=="original-Master-machine-and-buffered-IO" and
         record.get("source_written_CODE_bytes")==sum(s for _,_,s in MEMBERS) and
         record.get("original_parent_sha256")==digest_file(PARENT) and
         record.get("verifier_sha256")==digest_file(ROOT/"scripts/review_master_machine.py") and
         record.get("authored_credit")==0,"source or verifier identity differs")
    rows=record.get("members",[])
    need([(r.get("member"),r.get("start"),r.get("size")) for r in rows]==list(MEMBERS),
         "unreviewed or incomplete original Master source scope")
    if DECISION.exists():
        d=json.loads(DECISION.read_text())
        need(d.get("evidence_sha256")==digest_file(PROOF) and
             d.get("decision")=="ADOPT_COMPLETE_MASTER_MACHINE_CODE" and
             d.get("source_written_CODE_bytes")==record["source_written_CODE_bytes"] and
             d.get("authored_credit")==0,"original Master source adoption drifted")


def reviewed_claims(root, view, *, verify_targets=False):
    if not DECISION.exists():return [],None
    need(root.resolve()==ROOT.resolve(),"wrong Master source checkout")
    proof=json.loads(PROOF.read_text())
    public_check(proof)
    if verify_targets:need(evidence()==proof,"original Master machine evidence differs")
    return ([{"start":r["start"],"end":r["end"],"kind":"verified-vendor-code",
              "library":"master.lib 0.23","member":r["member"],"authored_credit":0}
             for r in proof["members"]],digest_file(DECISION))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--write",action="store_true")
    group.add_argument("--check",action="store_true")
    group.add_argument("--structural-check",action="store_true")
    args=p.parse_args()
    if args.write:
        need(not PROOF.exists() and not DECISION.exists(),
             "do not overwrite reviewed source evidence")
        row=evidence()
        PROOF.write_text(json.dumps(row,indent=2)+"\n")
        print("PASS original Master full source CODE",row["source_written_CODE_bytes"])
    else:
        row=json.loads(PROOF.read_text());public_check(row)
        if args.check: need(evidence()==row,"full native source/MZ proof differs")
        print("PASS original Master machine source and complete CODE")
if __name__=="__main__":main()

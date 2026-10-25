#!/usr/bin/env python3
"""Native CL.LIB ownership proposals for OP/MAINE; MAIN delegates unchanged.

Ownership classification replays a pinned distributed library's actual OMF
against one retained link and the original target. It is not authored-source
acceptance and claims no fresh compiler runs. No mode adopts a proposal.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

import review_vendor as legacy
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target, proof_sha256
from lib.unit_oracle import relative_fixups

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "op": {
        "packed": "c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb",
        "payload": "7c112a4a7dc4231e9be2d0f69555f0736f69165c80621a3fcd67324dad77ec47",
        "size": 77798, "pregame_end": 0xA39C,
        "receipt": "ff17c8d51cc7da16ab6776a1b3d0672935e6e8f568944588fe162c11bf19edb9",
        "proof": "33578d1886b8969cd6061a3bf6c78e22ce9a2932c9809222e0e6630e65b50fc4",
        "relocations": "d85beb6c4bdeb661dd6624db27adbc9848e272a1b167d79affaf59d344a5522a",
        "calibration_exe": "732f9659e987c1837a6def7b3d83b3b150b39c991928bba14eadec09272b4eb6",
        "calibration_map": "da2598ec3f3c707fdc968d0d9dcca5cddf333beb9b8241d76d123ee0970af907",
        "count": 63, "bytes": 23708,
        "deferred": ["xxas", "farheap", "signal", "exec", "setenvp"],
    },
    "maine": {
        "packed": "8308c416e756a07766f9f66dbf5575fa12c09189059226931a9562e7272b6997",
        "payload": "4c5d12f7cfdcf45665c923c46203fc03ab56cd467513e3d19305b914e4e5bf2e",
        "size": 77396, "pregame_end": 0xA545,
        "receipt": "572adef4e1159958a6c155bd4e469821815ded5f62df4dfc1d6d45c1c13cca86",
        "proof": "57591b3f082b01f19150ba4a71b1a84a84845a3f9998a6bdc74a527d8fc9201a",
        "relocations": "29e514bfc7ed234dbbd8ecda8607e3d9755f01dac0974de43b382fffc1208cd8",
        "calibration_exe": "60352c7ebb454be48da8516d5647df6d757e0f2d5a6262dbb678167cb925f1a4",
        "calibration_map": "27bece1e57bc7c11e7dc5a949baeacb10cd88391d581130c250616ecfaaa5277",
        "count": 55, "bytes": 20870,
        "deferred": ["farheap", "exec", "setenvp"],
    },
}
REVIEWER_SOURCES = [
    "scripts/review_vendor_context.py", "scripts/review_vendor.py",
    "scripts/lib/borland_library.py", "scripts/lib/omf.py", "scripts/lib/pc98.py",
    "scripts/lib/unit_context.py", "scripts/lib/unit_oracle.py",
    "scripts/lib/unit_extents.py", "scripts/lib/targets.py",
]
OPERATIONS = {"offset16", "segment16", "self-relative16", "far-pointer16:16",
              "TLINK same-segment far-call NOP/PUSHCS/CALL"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def context_pin(context):
    need(context in PINS, "unsupported decoded vendor context")
    return PINS[context]


def metadata_path(root, context="main"):
    need(context in ("main", "op", "maine"), "unsupported vendor context")
    return root / ("config/vendor_ownership.json" if context == "main" else
                   f"config/vendor_ownership.{context}.json")


def evidence_digest(meta):
    body = {k: v for k, v in meta.items() if k not in ("evidence_digest", "reviewer_sources")}
    return sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode())


def validate_target_context(context, config, artifact, target, proof):
    """Check original/decoded identities before nomination, without inventing MZ."""
    pin = context_pin(context.name)
    need(config.get("artifact") == artifact.get("id") == context.artifact,
         "vendor target artifact/context differs")
    need(artifact.get("sha256") == pin["packed"], "packed original target identity differs")
    need((len(target.program_image), sha(target.program_image)) == (pin["size"], pin["payload"]),
         "decoded payload identity differs")
    need(proof is not None and proof.get("artifact") == context.artifact and
         proof.get("packed_target_sha256") == pin["packed"] and
         proof.get("receipt_sha256") == pin["receipt"] and
         proof.get("relocations_sha256") == pin["relocations"] and
         proof_sha256(proof) == pin["proof"], "decoded receipt/proof/ordered relocation pin differs")
    need(config.get("target_view") == {"receipt_sha256": pin["receipt"], "proof_sha256": pin["proof"]},
         "decoded manifest pin differs")


def _hash(value):
    need(isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value), "malformed vendor evidence hash")


def _integer(value, low, high):
    need(type(value) is int and low <= value <= high, "vendor integer bounds")
    return value


def validate_metadata(meta, *, root=ROOT, context=None):
    if meta.get("artifact") == "th05-main":
        need(context in (None, "main"), "vendor metadata belongs to another context")
        return legacy.validate_metadata(meta, root=root)
    name = meta.get("context")
    pin = context_pin(name)
    need(context in (None, name) and meta.get("artifact") == "th05-" + name,
         "vendor metadata artifact/context differs")
    need(type(meta.get("schema_version")) is int and meta["schema_version"] == 1 and
         meta.get("kind") == "artifact-specific-cl-vendor-proposal",
         "vendor proposal schema")
    need(meta.get("decision") == "PROPOSAL" and meta.get("ownership_decision") is None and
         type(meta.get("authored_credit")) is int and meta["authored_credit"] == 0 and
         meta.get("denominator_changed") is False and type(meta.get("compiler_invocations")) is int and
         meta["compiler_invocations"] == 0, "proposal must not adopt or grant credit")
    need(meta.get("library") == "CL.LIB" and meta.get("library_sha256") == legacy.PINS["library_sha256"] and
         meta.get("toolchain_manifest_sha256") == legacy.PINS["toolchain_manifest_sha256"], "vendor library/toolchain identity")
    need(sha((root / "config/toolchain.toml").read_bytes()) == meta["toolchain_manifest_sha256"],
         "toolchain manifest drift")
    need(meta.get("target_sha256") == pin["packed"] and meta.get("target_payload_sha256") == pin["payload"] and
         meta.get("target_payload_size") == pin["size"] and meta.get("pregame_end") == pin["pregame_end"],
         "vendor original/decoded identity")
    cal = meta.get("calibration", {})
    need(cal == {"root": f".analysis/builds/{name}-calibration-a/source",
                 "exe_sha256": pin["calibration_exe"], "map_sha256": pin["calibration_map"],
                 "actual_retained_link_producers": 1}, "retained calibration artifact identity")
    proof = meta.get("target_view", {})
    need(proof.get("artifact") == meta["artifact"] and proof.get("packed_target_sha256") == pin["packed"] and
         proof.get("receipt_sha256") == pin["receipt"] and proof.get("relocations_sha256") == pin["relocations"] and
         proof_sha256(proof) == pin["proof"], "decoded public proof pin differs")
    need([r.get("file") for r in meta.get("reviewer_sources", [])] == REVIEWER_SOURCES,
         "reviewer source coverage differs")
    for row in meta["reviewer_sources"]:
        path = root / row["file"]
        need(path.is_file() and not path.is_symlink() and sha(path.read_bytes()) == row.get("sha256"),
             "reviewer/decoded loader source drift: " + row["file"])
    rows, deferred = meta.get("contributions", []), meta.get("deferred", [])
    need(len(rows) == meta.get("proposed_contribution_count") == pin["count"] and
         sum(x["size"] for x in rows) == meta.get("proposed_bytes") == pin["bytes"], "vendor contribution totals")
    need([x.get("member") for x in deferred] == pin["deferred"] and
         all(x.get("decision") == "DEFERRED_UNKNOWN" for x in deferred), "unsupported members must stay deferred")
    names, extents = set(), []
    for row in rows + deferred:
        name = row.get("member")
        need(isinstance(name, str) and re.fullmatch("[a-zA-Z0-9_@$]{1,8}", name) and name not in names,
             "duplicate/unsafe vendor member")
        names.add(name)
        a = _integer(row.get("start"), 0, pin["pregame_end"] - 1)
        n = _integer(row.get("size"), 1, 65535)
        need(row.get("end") == a+n <= pin["pregame_end"], "vendor contribution bounds")
        extents.append((a,a+n)); _hash(row.get("member_program_sha256"))
    extents.sort()
    need(all(b <= c for (_,b),(c,_) in zip(extents,extents[1:])), "vendor contributions overlap")
    for row in rows:
        size = row["size"]
        need(row.get("status") == "proven-complete-vendor-CODE-proposal" and
             row.get("segment") == "_TEXT" and row.get("class_name") == "CODE" and
             row.get("SEGDEF") == dict(name="_TEXT",cl="CODE",size=size,acbp=0x28) and
             row.get("complete_gapless_CODE_LEDATA") is True and row.get("unique_original_occurrence") is True,
             "complete vendor CODE proof missing")
        for key in ("original_unlinked_CODE_sha256", "linked_CODE_sha256"):
            _hash(row.get(key))
        blocks = []
        for block in row.get("CODE_LEDATA", []):
            a = _integer(block.get("offset"), 0, size-1)
            n = _integer(block.get("size"), 1, size)
            _integer(block.get("record_offset"),0,1048576); _hash(block.get("sha256"))
            blocks.append((a,a+n))
        cursor = 0
        for a,b in sorted(blocks):
            need(a == cursor and a < b <= size, "vendor LEDATA gap/overlap")
            cursor = b
        need(cursor == size, "incomplete vendor LEDATA coverage")
        written, expected_mz = set(), []
        for action in row.get("fixup_actions", []):
            site = _integer(action.get("site"),0,size-1)
            kind = action.get("kind")
            fm, tm = action.get("frame_method"), action.get("target_method")
            need(type(kind) is int and kind in (1,2,3) and
                 type(fm) is int and fm in (0,1,5) and
                 type(tm) is int and tm in (0,2) and action.get("operation") in OPERATIONS,
                 "unsupported vendor fixup action")
            # OMF's one/two-byte indices contain at most 15 value bits.
            # Methods 0/1 carry a SEGDEF/GRPDEF index; method 5 has none.
            if fm == 5:
                need(action.get("frame_index") is None, "target-derived frame has no index")
            else:
                _integer(action.get("frame_index"),1,0x7FFF)
            for key in ("target_index", "segment"):
                _integer(action.get(key),1,0x7FFF)
            _integer(action.get("record_offset"),0,1048576)
            relative = action.get("relative")
            need(type(relative) is bool and
                 relative is (action["operation"] == "self-relative16"),
                 "vendor fixup relative flag/operation differs")
            _integer(action.get("displacement"),0,65535)
            binding = action.get("binding")
            need(isinstance(binding,str) and binding.startswith(("segment:","external:")) and
                 "/" not in binding and "\\" not in binding, "unsafe/unresolved vendor binding")
            smart = action["operation"] == "TLINK same-segment far-call NOP/PUSHCS/CALL"
            allowed_operations = {1: {"offset16", "self-relative16"}, 2: {"segment16"},
                                  3: {"far-pointer16:16", "TLINK same-segment far-call NOP/PUSHCS/CALL"}}
            need(action["operation"] in allowed_operations[kind], "vendor fixup kind/operation differs")
            start = _integer(action.get("write_start"),0,size-1)
            n = _integer(action.get("write_size"),2,5)
            need((start,n) == ((site-1,5) if smart else (site,{1:2,2:2,3:4}[kind])),
                 "vendor FIXUPP write width/site differs")
            need(start+n <= size and not written.intersection(range(start,start+n)), "vendor fixup write overlap/bounds")
            written.update(range(start,start+n)); _hash(action.get("expected_bytes_sha256"))
            for key in ("resolved_frame","resolved_target_frame"):
                need(_integer(action.get(key),0,0xFFFF0) % 16 == 0, "unaligned vendor fixup frame")
            _integer(action.get("resolved_target_offset"),0,65535)
            if action["operation"] in ("segment16","far-pointer16:16"):
                expected_mz.append(site if kind == 2 else site+2)
        need(row.get("ordered_MZ_fixups") == expected_mz and len(expected_mz) == len(set(expected_mz)),
             "vendor ordered MZ differs from fixup actions")
    need(evidence_digest(meta) == meta.get("evidence_digest"), "vendor proposal evidence digest differs")
    def public_only(value):
        if isinstance(value, dict):
            need(not set(value).intersection({"raw","data","source_text","text","instructions",
                                              "program_records","bytes_hex"}),
                 "private vendor bytes/source in public metadata")
            for child in value.values(): public_only(child)
        elif isinstance(value,list):
            for child in value: public_only(child)
        elif isinstance(value,str):
            need(not value.startswith(("/home/","/mnt/","C:\\","D:\\")), "private absolute vendor path")
    public_only(meta)
    return dict(kind="public-vendor-structure-only",artifact=meta["artifact"],contributions=len(rows),
                proposed_bytes=pin["bytes"],byte_proof_replayed=False,decision="PROPOSAL",denominator_changed=False)


def review_inputs(root=ROOT, context="main"):
    if context == "main":
        return legacy.review_inputs(root)
    pin = context_pin(context)
    ctx = UnitContext(root,context); config = ctx.config()
    need(config.get("target_view") == {"receipt_sha256":pin["receipt"],"proof_sha256":pin["proof"]},
         "decoded manifest identity changed")
    artifact,target,proof = load_unit_target(ctx,config)
    validate_target_context(ctx,config,artifact,target,proof)
    base = root / f".analysis/builds/{context}-calibration-a/source"
    mapraw = (base/f"obj/th05/{context}.map").read_bytes()
    calraw = (base/f"bin/th05/{context}.exe").read_bytes()
    libraw = (root/".analysis/toolchain/installed/tc40j/LIB/CL.LIB").read_bytes()
    need(sha(mapraw) == pin["calibration_map"] and sha(calraw) == pin["calibration_exe"] and
         sha(libraw) == legacy.PINS["library_sha256"], "private calibration/MAP/library pin differs")
    cal = parse_mz(calraw); need(cal.valid,"invalid actual calibration MZ")
    review = legacy.VendorReview(libraw,mapraw,cal,target)
    rows, deferred = [], []
    for con in review.contribs:
        if con["cl"] != "CODE" or not con["size"] or con["module"].casefold() not in review.mods:
            continue
        a,n = con["start"],con["size"]
        if a+n > pin["pregame_end"] or cal.program_image[a:a+n] != target.program_image[a:a+n] or \
                relative_fixups(cal,a,n) != relative_fixups(target,a,n):
            continue
        mod = review.mods[con["module"].casefold()]
        try:
            rows.append(review.verify(mod,con))
        except (ValueError,KeyError) as error:
            deferred.append(dict(member=mod["name"],start=a,end=a+n,size=n,
                member_program_sha256=mod["program_sha256"],reason=str(error),decision="DEFERRED_UNKNOWN"))
    result = dict(schema_version=1,kind="artifact-specific-cl-vendor-proposal",context=context,
        artifact=ctx.artifact,decision="PROPOSAL",ownership_decision=None,authored_credit=0,
        denominator_changed=False,compiler_invocations=0,library="CL.LIB",
        library_sha256=sha(libraw),toolchain_manifest_sha256=legacy.PINS["toolchain_manifest_sha256"],
        source_provenance="Pinned distributed Borland CL.LIB binary OMF members; no original C source-text claim.",
        target_sha256=artifact["sha256"],target_payload_sha256=sha(target.program_image),
        target_payload_size=len(target.program_image),pregame_end=pin["pregame_end"],target_view=proof,
        calibration=dict(root=f".analysis/builds/{context}-calibration-a/source",exe_sha256=sha(calraw),
                         map_sha256=sha(mapraw),actual_retained_link_producers=1),
        proposed_contribution_count=len(rows),proposed_bytes=sum(x["size"]for x in rows),
        contributions=rows,deferred=deferred,
        scope_limit="Only complete gapless CODE SEGDEFs; unsupported members, surrounding gaps and all DATA/BSS stay unknown.",
        reviewer_sources=[dict(file=p,sha256=sha((root/p).read_bytes()))for p in REVIEWER_SOURCES])
    result["evidence_digest"] = evidence_digest(result)
    validate_metadata(result,root=root,context=context)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context",choices=("main","op","maine"),default="main")
    modes = parser.add_mutually_exclusive_group(required=True)
    for mode in ("check","write","structural-check"):
        modes.add_argument("--"+mode,action="store_true")
    args = parser.parse_args(); path = metadata_path(ROOT,args.context)
    if args.structural_check:
        result = validate_metadata(json.loads(path.read_text()),context=args.context)
    else:
        meta = review_inputs(ROOT,args.context)
        if args.write: path.write_text(json.dumps(meta,indent=2)+"\n")
        else: need(json.loads(path.read_text()) == meta,"saved vendor proposal differs from real native replay")
        result = dict(kind="native-private-vendor-byte-review",context=args.context,
                      contributions=meta["proposed_contribution_count"],proposed_bytes=meta["proposed_bytes"],
                      compiler_invocations=0,decision="PROPOSAL",metadata_written=args.write,denominator_changed=False)
    print(json.dumps(result,indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

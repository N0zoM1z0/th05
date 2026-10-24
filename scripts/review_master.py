#!/usr/bin/env python3
"""Revalidate a bounded Master 0.23 ownership PROPOSAL without DOS tools.

--structural-check needs only public metadata and reviewer sources. --check
also rereads all pinned private inputs, not saved report pass/status fields.
Neither mode adopts ownership, excludes bytes, or grants authored credit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz

ROOT = Path(__file__).resolve().parents[1]
FROZEN_EVIDENCE_SHA256 = "a2395fdfca147e7008f544e886486ee1fd682eae1a650db63aad7e9c95455a52"
PINS = {
    "target": "c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0",
    "calibration_exe": "630b909739501bab6a9ef2c2b65e517332277c8ea66895af2ee4ba9d3e04d380",
    "calibration_map": "e2092c37785d852420f84f9830cbcc82dcd5157696b348c329fb1e52a15bbed3",
    "saved_object": "dffea9bd300f8a3ccb889a1188cd6569a3880bcdf6a540b482c48e7af383bbcf",
    "listing_object": "dffea9bd300f8a3ccb889a1188cd6569a3880bcdf6a540b482c48e7af383bbcf",
    "calibration_object": "dffea9bd300f8a3ccb889a1188cd6569a3880bcdf6a540b482c48e7af383bbcf",
    "listing": "f2b8f2859f1bb0e13f7333bc55541bea0e7a3ac03d3541de88a8a7c309fc1afa",
    "listing_receipt": "79ed365a3cd27998383d198f81a2e2a0e14cbb9cb22bced87e25250bbda85375",
    "historical_tasm": "ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26",
    "outer_archive": "9df4ba0ec1c3d81f2d77677c8c99f563281db4a4d9d87718a956d4c92156747f",
    "inner_archive": "acc5369d3fb445d5cd6b92abbedb7b433819465be2f85bbbff53bd1f77bc40b6",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def relative(value):
    need(isinstance(value, str) and value and "\\" not in value,
         "unsafe evidence filename")
    p = Path(value)
    need(not p.is_absolute() and ".." not in p.parts and ":" not in value,
         "unsafe evidence filename")
    return p


def pinned(root, row):
    p = root / relative(row["file"])
    need(not p.is_symlink() and p.is_file(), "missing regular input: " + str(p))
    need(p.resolve().is_relative_to(root.resolve()), "input escapes evidence root")
    raw = p.read_bytes()
    need(len(raw) == row["size"] and sha(raw) == row["sha256"],
         "input identity drift: " + row["file"])
    return raw


def evidence_digest(meta):
    body = {k: v for k, v in meta.items() if k not in ("evidence_digest", "reviewer_sources")}
    return sha(json.dumps(body, sort_keys=True, separators=(",", ":")).encode())


def validate_metadata(meta, *, root=ROOT):
    need(meta.get("schema_version") == 1 and meta.get("kind") == "master-vendor-ownership-proposal"
         and meta.get("artifact") == "th05-main", "metadata schema/artifact")
    need(meta.get("decision") == "PROPOSAL" and meta.get("ownership_decision") is None
         and meta.get("authored_credit") == 0 and meta.get("denominator_changed") is False
         and meta.get("compiler_invocations") == 0, "proposal cannot adopt ownership or grant credit")
    need(meta.get("module") == {"name": "th05_main.asm", "segment": "_TEXT",
         "start": 0x272, "size": 0x4376, "end": 0x45E8}, "mixed module bounds")
    for role, digest in PINS.items():
        need(meta["inputs"].get(role, {}).get("sha256") == digest, "input pin: " + role)
    rows = meta.get("procedures", [])
    need(len(rows) == 20 and sum(x["size"] for x in rows) == 376,
         "twenty complete procedure extents required")
    need(sum(x["instruction_bytes"] for x in rows) == 367
         and sum(len(x["padding"]) for x in rows) == 9, "instruction/padding totals")
    seen, prior = set(), 0x272
    for row in rows:
        a, z = row["start"], row["end"]
        need(type(a) is int and type(z) is int and prior <= a < z <= 0x45E8
             and z-a == row["size"], "overlapping/invalid procedure boundary")
        prior = z
        need(row["name"].casefold() not in seen, "duplicate procedure")
        seen.add(row["name"].casefold())
        need(row["decision"] == "PROPOSAL" and row["ordered_mz_fixups"] == []
             and not row["inline_data"], "unsupported procedure policy/ordered fixups")
        need(row["instruction_bytes"] == row["size"]-len(row["padding"]), "padding accounting")
        for pad in row["padding"]:
            need(pad["size"] == 1 and a <= pad["start"] < z
                 and (pad["start"]-0x272) % 2 == 1 and pad["value"] == 0x90,
                 "invalid assembler EVEN padding")
    deferred = meta.get("deferred_source_mismatches", [])
    need(len(deferred) == 40 and all(x.get("decision") == "DEFERRED" for x in deferred),
         "forty source-mismatch candidates must remain deferred")
    need(sum(x["size"] for x in meta.get("uncovered_gaps", [])) == 196
         and all(x.get("decision") == "UNKNOWN" for x in meta["uncovered_gaps"]),
         "uncovered gaps must remain unknown")
    need(meta.get("macro_context", {}).get("active_model") == {
         "CALLMODEL": "FAR", "RETSIZE": 2, "DATASIZE": 2, "listing_model": 5},
         "FAR/data2 context required")
    need(evidence_digest(meta) == meta.get("evidence_digest") == FROZEN_EVIDENCE_SHA256,
         "frozen reviewed evidence scope changed")
    need([x.get("file") for x in meta.get("reviewer_sources", [])] ==
         ["scripts/review_master.py", "scripts/lib/omf.py", "scripts/lib/pc98.py"],
         "complete public reviewer source coverage required")
    for row in meta["reviewer_sources"]:
        pinned(root, row)
    def public_only(value):
        if isinstance(value, dict):
            for key, child in value.items():
                need(key not in {"raw", "data", "source_text", "text", "instructions",
                                 "program_records", "bytes_hex"}, "raw/source evidence is private")
                public_only(child)
        elif isinstance(value, list):
            for child in value:
                public_only(child)
        elif isinstance(value, str):
            need(not value.startswith(("/home/", "/mnt/", "C:\\", "D:\\")), "private absolute path")
    public_only(meta)
    return dict(kind="public-metadata-structure-only", procedures=20, full_bytes=376,
                instruction_bytes=367, padding_bytes=9, byte_proof_replayed=False,
                decision="PROPOSAL", authored_credit=0, denominator_changed=False)


def decoded(raw, encoding):
    return raw.decode(encoding).replace("\r\n", "\n").replace("\r", "\n")


def source_blocks(raw, encoding):
    lines = decoded(raw, encoding).split("\n")
    result = []
    for i, line in enumerate(lines):
        code = line.split(";", 1)[0]
        macro = re.match(r"\s*(func|retfunc)\s+([\w@$?]+)\b", code, re.I)
        proc = re.match(r"\s*([\w@$?]+)\s+proc(?:\s|$)", code, re.I)
        if not (macro or proc):
            continue
        name = macro[2] if macro else proc[1]
        end_pattern = r"^\s*endfunc\b" if macro else r"^\s*"+re.escape(name)+r"\s+endp\b"
        for j in range(i+1, len(lines)):
            if re.match(end_pattern, lines[j].split(";", 1)[0], re.I):
                result.append(dict(name=name, start_line=i+1, end_line=j+1,
                                   text="\n".join(lines[i:j+1])))
                break
    return result


def macro_blocks(raw, encoding, name):
    lines = decoded(raw, encoding).split("\n")
    result = []
    for i, line in enumerate(lines):
        if not re.match(r"\s*"+re.escape(name)+r"\s+macro\b", line, re.I):
            continue
        depth = 1
        for j in range(i+1, len(lines)):
            code = lines[j].split(";", 1)[0]
            if re.match(r"\s*\w+\s+macro\b", code, re.I):
                depth += 1
            elif re.match(r"\s*endm\b", code, re.I):
                depth -= 1
            if depth == 0:
                result.append("\n".join(lines[i:j+1]))
                break
    return result


def crc16(raw):
    crc = 0
    for value in raw:
        crc ^= value
        for _ in range(8):
            crc = (crc >> 1) ^ (0xA001 if crc & 1 else 0)
    return crc


def stored_lzh(raw):
    """Fail closed on anything beyond the pinned level1/-lh0-/no-extension form."""
    members, folded, pos = {}, set(), 0
    while pos < len(raw) and raw[pos]:
        end = pos+raw[pos]+2
        need(end <= len(raw), "LZH truncated header")
        h = raw[pos:end]
        need(len(h) >= 27 and sum(h[2:]) & 255 == h[1], "LZH header checksum")
        need(h[2:7] == b"-lh0-" and h[20] == 1, "unsupported LZH method/level")
        packed, size = struct.unpack_from("<II", h, 7)
        n = h[21]
        need(len(h) == n+27 and h[-2:] == b"\0\0" and packed == size,
             "unsupported LZH extensions/size")
        name = h[22:22+n].decode("ascii")
        need(name and name not in (".", "..") and not any(c in name for c in "/\\:\0")
             and name.casefold() not in folded, "unsafe/duplicate LZH member")
        content = raw[end:end+packed]
        need(len(content) == size, "LZH truncated member")
        need(crc16(content) == int.from_bytes(h[22+n:24+n], "little"), "LZH member CRC")
        members[name] = content
        folded.add(name.casefold())
        pos = end+packed
    need(pos+1 == len(raw) and raw[pos] == 0, "LZH terminator/trailing bytes")
    return members


def active_address(line):
    fields = line.split("\t")
    m = re.match(r"^\s*([0-9a-f]{4})(?:\s|$)", fields[1], re.I) if len(fields)>1 else None
    return int(m[1], 16) if m else None


def listing_procedures(raw, size=0x4376):
    """Active expansion rows only; include depth differs from macro depth."""
    owners, stack, result = [(0, "th05_main.asm", None)], [], []
    entered = ended = False
    for number, line in enumerate(raw.decode("latin1").splitlines(), 1):
        address = active_address(line)
        if not entered:
            entered = address == 0 and bool(re.search(r"\b_TEXT\s+segment\b", line, re.I))
            continue
        if address is not None and re.search(r"\b_TEXT\s+ends\b", line, re.I):
            need(address == size and not stack, "listing complete _TEXT end")
            ended = True
            break
        prefix = line.split("\t", 1)[0].split()
        if len(prefix) not in (1, 2) or not all(x.isdigit() for x in prefix):
            continue
        depth = int(prefix[0]) if len(prefix) == 2 else 0
        include = re.search(r"\binclude\s+(\S+)\s*$", line, re.I)
        if depth == 0 and address is None and include is None:
            continue
        while owners[-1][0] > depth:
            owners.pop()
        owner = owners[-1][1]
        if include and not line.split("\t")[-1].lstrip().startswith(";"):
            filename = include[1].replace("\\", "/")
            relative(filename)
            owners.append((depth+1, filename, number))
        if address is None:
            continue
        code = " ".join(line.split("\t")[2:]).split(";", 1)[0]
        declaration = re.match(r"\s*([A-Za-z_$?@][\w$?@]*)\s+(proc|endp)\b(?:\s+(near|far))?", code, re.I)
        if declaration:
            name, kind, distance = declaration.groups()
            if kind.casefold() == "proc":
                stack.append(dict(name=name, distance=distance or "far-by-large-model",
                                  local_start=address, start_listing_line=number,
                                  source=owner, padding=[], inline_data=False))
            else:
                need(stack and stack[-1]["name"].casefold() == name.casefold(), "unpaired active ENDP")
                row = stack.pop()
                row.update(local_end=address, end_listing_line=number)
                result.append(row)
        elif stack:
            if re.search(r"\bEVEN\s*$", code, re.I) and address % 2:
                stack[-1]["padding"].append(dict(local_start=address, size=1, listing_line=number))
            if re.search(r"\b(?:db|dw|dd|dq|dt)\b", code, re.I):
                stack[-1]["inline_data"] = True
    need(entered and ended and not stack, "incomplete active listing")
    return sorted(result, key=lambda x: (x["local_start"], x["local_end"], x["name"]))


def idx(b, c):
    need(c < len(b), "truncated OMF index")
    v = b[c]
    if v & 128:
        need(c+1 < len(b), "truncated long OMF index")
        return ((v & 127) << 8) | b[c+1], c+2
    return v, c+1


def object_text(raw):
    """Parse all real OMF records; retain gaps and ordered relocation fields."""
    names, segs, blocks, fixups = [""], [None], [], []
    last = None
    for r in parse_omf(raw):
        b = r.data
        if r.name == "LNAMES":
            c = 0
            while c < len(b):
                n = b[c]
                need(c+1+n <= len(b), "LNAMES bounds")
                names.append(b[c+1:c+1+n].decode("ascii"))
                c += n+1
        elif r.name == "SEGDEF":
            need(len(b)>=6 and b[0] & 0xE0 and not b[0] & 2, "unsupported SEGDEF")
            ni, c = idx(b, 3)
            ci, c = idx(b, c)
            _, c = idx(b, c)
            need(c == len(b) and 0<ni<len(names) and 0<ci<len(names), "SEGDEF bounds")
            segs.append(dict(name=names[ni], class_name=names[ci], size=int.from_bytes(b[1:3], "little"), acbp=b[0]))
        elif r.name == "LEDATA":
            si, c = idx(b, 0)
            need(0<si<len(segs) and c+2<=len(b), "LEDATA bounds")
            off, content = int.from_bytes(b[c:c+2], "little"), b[c+2:]
            need(off+len(content)<=segs[si]["size"], "LEDATA outside segment")
            last = dict(segment=si, offset=off, content=content)
            blocks.append(last)
        elif r.name == "FIXUPP":
            need(last is not None, "FIXUPP without LEDATA")
            c = 0
            while c < len(b):
                need(c+3<=len(b), "FIXUPP truncated")
                loc, dat = b[c], b[c+2]
                need(loc & 128 and not dat & 128 and not dat & 8, "threaded FIXUPP unsupported")
                site, kind = ((loc & 3)<<8)|b[c+1], (loc>>2)&15
                fm, tm = (dat>>4)&7, dat&3
                c += 3
                if fm <= 2:
                    fd, c = idx(b, c)
                else:
                    need(fm in (4, 5), "unsupported frame method")
                    fd = None
                td, c = idx(b, c)
                disp = 0
                if not dat & 4:
                    need(c+2<=len(b), "FIXUPP displacement")
                    disp, c = int.from_bytes(b[c:c+2], "little"), c+2
                need(kind in (1,2,3) and site+{1:2,2:2,3:4}[kind]<=len(last["content"]), "FIXUPP field bounds")
                fixups.append(dict(segment=last["segment"], offset=last["offset"]+site,
                                   kind=kind, absolute=bool(loc&64), frame_method=fm,
                                   frame_index=fd, target_method=tm, target_index=td,
                                   displacement=disp))
        elif r.name == "LIDATA":
            si, _ = idx(b, 0)
            need(0<si<len(segs) and segs[si]["name"] != "_TEXT",
                 "iterated data in reviewed CODE unsupported")
            last = None  # Non-CODE LIDATA never becomes procedure byte evidence.
        elif r.name in ("LIDATA32", "LEDATA32", "FIXUPP32", "SEGDEF32"):
            raise ValueError("unsupported OMF transformation: "+r.name)
    matches = [i for i, s in enumerate(segs) if s and s["name"] == "_TEXT"]
    need(len(matches)==1, "unique object _TEXT required")
    si = matches[0]
    need(segs[si] == dict(name="_TEXT", class_name="CODE", size=0x4376, acbp=0x48), "object _TEXT context")
    return dict(segment=si, blocks=[x for x in blocks if x["segment"]==si],
                fixups=[x for x in fixups if x["segment"]==si])


def linked_object_procedure(obj, start, size, bias=0x272):
    lo, hi = start-bias, start-bias+size
    out, coverage = bytearray(size), bytearray(size)
    for block in obj["blocks"]:
        a, z = max(lo, block["offset"]), min(hi, block["offset"]+len(block["content"]))
        if a>=z:
            continue
        need(not any(coverage[a-lo:z-lo]), "overlapping procedure LEDATA")
        coverage[a-lo:z-lo] = bytes([1])*(z-a)
        out[a-lo:z-lo] = block["content"][a-block["offset"]:z-block["offset"]]
    need(all(coverage), "procedure has uncovered LEDATA")
    occupied, actions = set(), []
    for f in obj["fixups"]:
        a, width = f["offset"], {1:2,2:2,3:4}[f["kind"]]
        if a+width<=lo or a>=hi:
            continue
        need(lo<=a and a+width<=hi, "fixup crosses complete procedure boundary")
        field = set(range(a, a+width))
        need(not occupied & field, "overlapping procedure FIXUPP")
        occupied |= field
        # Only the actually observed local _TEXT offset fixup is supported.
        # The target segment's actual MAP contribution determines the bias.
        need(f["kind"]==1 and f["absolute"] and f["frame_method"]==5
             and f["target_method"]==0 and f["target_index"]==obj["segment"]
             and f["displacement"]==0, "unreviewed procedure link transformation")
        i = a-lo
        value = (int.from_bytes(out[i:i+2], "little")+bias)&0xFFFF
        out[i:i+2] = value.to_bytes(2, "little")
        actions.append(dict(offset=i, operation="actual MAP _TEXT offset addition", addend=bias))
    return bytes(out), actions


def verify_raw_procedure(row, original, linked, obj):
    a, z = row["start"], row["end"]
    need(original.valid and linked.valid, "invalid MZ input")
    need(0<=a<z<=len(original.program_image) and z<=len(linked.program_image), "MZ procedure bounds")
    before, after = original.program_image[a:z], linked.program_image[a:z]
    need(before == after and sha(before)==row["linked_sha256"], "original complete raw procedure differs")
    for image in (original, linked):
        sites = [r.linear-a for r in image.relocations if a-1<=r.linear<z]
        need(sites == row["ordered_mz_fixups"] == [], "original/candidate ordered MZ fixups differ")
    reconstructed, actions = linked_object_procedure(obj, a, z-a)
    need(reconstructed == after, "actual OMF/link reconstruction differs")
    need(actions == row["object_link_actions"], "object link action provenance differs")
    for pad in row["padding"]:
        need(before[pad["start"]-a] == pad["value"] == 0x90, "original assembler padding changed")


def verify_macro_context(meta, listing, upstream, candidate):
    ctx = meta["macro_context"]
    lines = listing.decode("latin1").splitlines()
    need(len([x for x in lines if re.search(r"\.model\s+use16\s+large\s+_TEXT\b", x, re.I)])==1,
         "listing large model missing/ambiguous")
    for name in ("RETSIZE", "DATASIZE"):
        matches = [i+1 for i,x in enumerate(lines) if re.search(r"=0002\s+"+name+r"\s+EQU\s+2\b", x, re.I)]
        need(matches == [ctx["active_listing_lines"][name]], "listing active FAR/data2 arm differs")
    make = decoded(upstream["MAKEFILE"], "cp932")
    need(re.search(r"^\.asm\{\$\(LARGEDIR\)\}\.obj\s*:\s*\n\s*\$\(AS\).*?/DFARMODEL\b", make, re.M),
         "upstream original large-model build flag")
    original, current = upstream["FUNC.INC"], candidate["libs/master.lib/func.inc"]
    need(re.search(r"IFDEF FARMODEL\s+CALLMODEL equ FAR\s+RETSIZE EQU 2\s+DATASIZE EQU 2\s+ENDIF",
                   decoded(original, "cp932"), re.I), "upstream FAR/data2 definition")
    need(re.search(r"ELSEIF\s+@MODEL EQ 5\s+RETSIZE EQU 2\s+DATASIZE EQU 2",
                   decoded(current, "utf8"), re.I), "candidate FAR/data2 definition")
    for row in ctx["literal_macros"]:
        a = macro_blocks(upstream[row["upstream_file"]], "cp932", row["name"])
        b = macro_blocks(candidate[row["candidate_file"]], "utf8", row["name"])
        need(a and a==b and [sha(x.encode()) for x in a]==row["variant_sha256"]
             and sha(a[0].encode())==row["sha256"],
             "complete macro text differs: "+row["name"])
        if row["name"] != "WAITREADY":
            selector = "RETSIZE" if row["name"]=="_call" else "DATASIZE"
            for content, encoding in ((original,"cp932"),(current,"utf8")):
                arm = re.search(r"(?ims)^IF "+selector+r" EQ 2\s*\n(.*?)^ELSE\s*$",
                                decoded(content,encoding))
                need(arm and a[0] in arm[1], "macro is not in proven FAR/data2 arm")
    for name in ("func", "retfunc"):
        a, b = macro_blocks(original, "cp932", name), macro_blocks(current, "utf8", name)
        need(len(a)==len(b)==1, "missing/ambiguous function wrapper")
        expected, n = re.subn(r"(?im)^(\s*name\s+proc) CALLMODEL\s*$", r"\1", a[0])
        need(n==1 and expected==b[0], "unreviewed function wrapper change")
    need(decoded(upstream["PF.INC"], "cp932")==decoded(candidate["libs/master.lib/pf.inc"], "utf8"),
         "PF.INC complete text differs")
    for row in ctx["constants"]:
        values = []
        for raw, encoding in ((upstream[row["upstream_file"]], "cp932"),
                              (candidate[row["candidate_file"]], "utf8")):
            values.append(re.findall(r"(?im)^\s*"+row["name"]+r"\s+equ\s+(\S+)", decoded(raw, encoding)))
        need(values == [[row["expression"]], [row["expression"]]], "port/register constant context")


def review_inputs(meta, *, root=ROOT):
    validate_metadata(meta, root=root)
    raw = {role: pinned(root, row) for role,row in meta["inputs"].items()}
    producer = json.loads(raw["listing_receipt"])
    need(producer["command"][:9] == ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx",
         "/kh32768", "/t", "/dGAME=5", "/la", "th05_main.asm"]
         and len(producer["command"])==11 and producer["tasm_invocations"]==1
         and producer["returncode"]==0, "historical bounded listing producer context")
    need(producer["listing"]["sha256"]==sha(raw["listing"])
         and producer["actual_active_tasm"]["sha256"]==sha(raw["historical_tasm"]),
         "historical listing/tool identities differ")
    need(raw["saved_object"] == raw["listing_object"] == raw["calibration_object"],
         "saved/listing/calibration complete OMF differ")
    description = describe_omf(raw["saved_object"])
    dependency_names = list(dict.fromkeys(["th05_main.asm", *[x.replace("\\", "/") for x in description["dependency_paths"]]]))
    need(dependency_names == [x["name"] for x in meta["frozen_source_closure"]], "actual OMF dependency closure/order differs")
    need(producer["frozen_source_closure"] == [dict(path=x["name"],size=x["size"],sha256=x["sha256"])
         for x in meta["frozen_source_closure"]], "historical source closure disagrees")
    candidate = {}
    for row in meta["frozen_source_closure"]:
        local = dict(file=meta["candidate_source_root"]+"/"+row["name"], size=row["size"], sha256=row["sha256"])
        before = pinned(root, local)
        local["file"] = meta["calibration_source_root"]+"/"+row["name"]
        need(before == pinned(root, local), "frozen source closure differs")
        candidate[row["name"]] = before
    upstream = stored_lzh(raw["inner_archive"])
    need(len(upstream)==653, "independently pinned archive member count")
    for name, content in upstream.items():
        extracted = root / relative(meta["upstream_source_root"]+"/"+name)
        need(extracted.is_file() and not extracted.is_symlink() and extracted.read_bytes()==content,
             "extracted upstream member differs: "+name)
    verify_macro_context(meta, raw["listing"], upstream, candidate)
    actual = listing_procedures(raw["listing"])
    inventory = [dict(name=x["name"], source=x["source"], start=x["local_start"]+0x272,
                      end=x["local_end"]+0x272, start_listing_line=x["start_listing_line"],
                      end_listing_line=x["end_listing_line"]) for x in actual]
    need(inventory == meta["active_procedure_inventory"], "actual active procedure boundaries/source differ")
    ordered = [x for x in inventory if x["end"]>x["start"]]
    cursor, gaps = 0x272, []
    for row in ordered:
        need(cursor <= row["start"], "overlapping active procedures")
        if cursor < row["start"]:
            gaps.append(dict(start=cursor, end=row["start"], size=row["start"]-cursor, decision="UNKNOWN"))
        cursor = row["end"]
    if cursor<0x45E8:
        gaps.append(dict(start=cursor, end=0x45E8, size=0x45E8-cursor, decision="UNKNOWN"))
    need(gaps == meta["uncovered_gaps"], "uncovered gaps changed")
    contributions = []
    for line in raw["calibration_map"].decode("cp437").splitlines():
        m = re.fullmatch(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M=th05_main.asm\s+ACBP=48\s*", line, re.I)
        if m:
            contributions.append((int(m[1],16)*16+int(m[2],16), int(m[3],16)))
    need(contributions == [(0x272,0x4376)], "actual complete MAP _TEXT contribution")
    original, linked = parse_mz(raw["target"]), parse_mz(raw["calibration_exe"])
    need(sha(original.program_image)==meta["target_payload_sha256"], "original payload pin")
    obj = object_text(raw["saved_object"])
    index = {}
    for name, content in upstream.items():
        if name.endswith(".ASM"):
            for block in source_blocks(content, "cp932"):
                index.setdefault(block["name"].casefold(), []).append((name, block))
    for row in meta["procedures"]:
        matches = [x for x in actual if x["name"].casefold()==row["name"].casefold()
                   and x["local_start"]+0x272==row["start"]]
        need(len(matches)==1, "ambiguous listing procedure")
        proc = matches[0]
        pads = [dict(start=x["local_start"]+0x272, size=1, value=0x90, listing_line=x["listing_line"]) for x in proc["padding"]]
        need(proc["local_end"]+0x272==row["end"] and proc["source"]==row["candidate_file"]
             and proc["distance"]==row["distance"] and pads==row["padding"]
             and not proc["inline_data"], "procedure boundary/context/padding disagrees")
        local_blocks = [x for x in source_blocks(candidate[row["candidate_file"]], "utf8")
                        if x["name"].casefold()==row["name"].casefold()]
        hits = [(name,a,b) for name,a in index.get(row["name"].casefold(), [])
                for b in local_blocks if a["text"]==b["text"]]
        need(len(hits)==1, "complete upstream source block absent/ambiguous/different")
        name, a, b = hits[0]
        need(name==row["upstream_file"] and [a["start_line"],a["end_line"]]==row["upstream_lines"]
             and [b["start_line"],b["end_line"]]==row["candidate_lines"]
             and sha(a["text"].encode())==row["source_block_sha256"], "complete literal source scope differs")
        verify_raw_procedure(row, original, linked, obj)
    for row in meta["deferred_source_mismatches"]:
        local = [x for x in source_blocks(candidate[row["candidate_file"]], "utf8")
                 if x["name"].casefold()==row["name"].casefold()]
        hits = [(name,a,b) for name,a in index.get(row["name"].casefold(), [])
                for b in local if a["text"]==b["text"]]
        need(len(hits)!=1, "deferred source classification changed; explicit review required")
    return dict(kind="native-master-procedure-review", decision="PROPOSAL", procedures=20,
                full_bytes=376, instruction_bytes=367, padding_bytes=9,
                deferred_source_mismatches=40, uncovered_gap_bytes=196,
                byte_proof_replayed=True, compiler_invocations=0,
                authored_credit=0, denominator_changed=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--structural-check", action="store_true")
    args = parser.parse_args()
    try:
        meta = json.loads((ROOT/"config/master_vendor_ownership.json").read_text())
        print(json.dumps(validate_metadata(meta) if args.structural_check else review_inputs(meta), indent=2))
    except (ValueError, KeyError, TypeError, IndexError, OSError) as error:
        parser.exit(1, "Master review failed: "+str(error)+"\n")


if __name__ == "__main__":
    main()

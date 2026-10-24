#!/usr/bin/env python3
"""Review pinned vendor CODE ownership without compiling or running game code.

--check/--write require the retained private CL/MAP/MZ inputs. --structural-check
checks only public metadata and makes no claim of independently replaying bytes.
Only demonstrated 16-bit OMF cases are supported; unsupported fixups fail closed.
"""

from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re

from lib.borland_library import library_members
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.unit_context import UnitContext, load_unit_target
from lib.unit_oracle import relative_fixups

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_PARSER_SHA256 = (
    "729f4283a999a88519bc2c545b96c541f2b36565da24737d7493c03c52214c84"
)
PINS = {
    "library_sha256": "7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7",
    "calibration_exe_sha256": "630b909739501bab6a9ef2c2b65e517332277c8ea66895af2ee4ba9d3e04d380",
    "calibration_map_sha256": "e2092c37785d852420f84f9830cbcc82dcd5157696b348c329fb1e52a15bbed3",
    "target_sha256": "c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0",
    "target_payload_sha256": "25860b4e1061c9d78f1cf7862716b02a88b150addfecf31de265acbca8361a41",
    "toolchain_manifest_sha256": "4803f9748f817ed9eae8db05006534d6a18bf1c634069dc487dbd4ebb75e1a16",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def idx(data, cursor):
    need(cursor < len(data), "truncated OMF index")
    value = data[cursor]
    cursor += 1
    if value & 128:
        need(cursor < len(data), "truncated OMF long index")
        value = ((value & 127) << 8) | data[cursor]
        cursor += 1
    return value, cursor


class VendorReview:
    """Private byte evidence for complete pinned members; no ledger mutations."""

    def __init__(self, libraw: bytes, mapraw: bytes, cal, target):
        self.cal, self.target = cal, target
        contribs = []
        groups = collections.defaultdict(set)
        segbases = {}
        pubmap = collections.defaultdict(set)
        for line in mapraw.decode("cp437").splitlines():
            m = re.match(
                r"\s*([0-9A-F]+)H\s+[0-9A-F]+H\s+[0-9A-F]+H\s+(\S+)\s+(\S+)\s*$",
                line,
                re.I,
            )
            if m:
                segbases[m[2].casefold()] = int(m[1], 16)
            m = re.match(
                r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=([0-9A-F]+)",
                line,
                re.I,
            )
            if m:
                seg, off, size = int(m[1], 16), int(m[2], 16), int(m[3], 16)
                contribs.append(
                    dict(
                        frame=seg * 16,
                        start=seg * 16 + off,
                        size=size,
                        cl=m[4],
                        segment=m[5],
                        group=m[6],
                        module=m[7],
                        acbp=m[8],
                    )
                )
                if m[6] != "(none)":
                    groups[m[6].casefold()].add(seg * 16)
            m = re.match(
                r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?(.+?)\s*$", line, re.I
            )
            if m and " C=" not in line:
                pubmap[m[3]].add((int(m[1], 16) * 16, int(m[2], 16)))
        need(all(len(x) == 1 for x in groups.values()), "ambiguous MAP group frame")
        groups = {k: next(iter(x)) for k, x in groups.items()}
        mods = {}
        for member in library_members(libraw):
            # The library parser already checks every original ordinary record. THEADR is
            # a metadata-only parse envelope, excluded from every member/program digest.
            recs = parse_omf(bytes.fromhex("800200007e") + member.program_records)
            names = [""]
            segs = [None]
            grps = [None]
            exts = [None]
            pubs = []
            blocks = []
            fix = []
            last = None
            for r in recs:
                b = r.data
                if r.name == "LNAMES":
                    c = 0
                    while c < len(b):
                        n = b[c]
                        c += 1
                        need(c + n <= len(b), "LNAMES length")
                        names.append(b[c : c + n].decode("cp437"))
                        c += n
                elif r.name == "SEGDEF":
                    need(
                        len(b) >= 6 and b[0] & 0xE0 and not (b[0] & 2),
                        "unsupported absolute/32 SEGDEF",
                    )
                    ni, c = idx(b, 3)
                    ci, c = idx(b, c)
                    oi, c = idx(b, c)
                    need(c == len(b), "SEGDEF trailing")
                    need(
                        0 < ni < len(names)
                        and 0 < ci < len(names)
                        and 0 <= oi < len(names),
                        "SEGDEF name index out of bounds",
                    )
                    segs.append(
                        dict(
                            name=names[ni],
                            cl=names[ci],
                            size=int.from_bytes(b[1:3], "little"),
                            acbp=b[0],
                        )
                    )
                elif r.name == "GRPDEF":
                    ni, c = idx(b, 0)
                    members = []
                    while c < len(b):
                        need(b[c] == 255, "unsupported GRPDEF")
                        si, c = idx(b, c + 1)
                        members.append(si)
                    grps.append(dict(name=names[ni], members=members))
                elif r.name in ("EXTDEF", "LEXTDEF"):
                    c = 0
                    while c < len(b):
                        n = b[c]
                        c += 1
                        need(c + n <= len(b), "EXTDEF length")
                        name = b[c : c + n].decode("cp437")
                        c += n
                        ti, c = idx(b, c)
                        exts.append(name)
                elif r.name == "PUBDEF":
                    gi, c = idx(b, 0)
                    si, c = idx(b, c)
                    if si == 0:
                        c += 2
                    while c < len(b):
                        n = b[c]
                        c += 1
                        name = b[c : c + n].decode("cp437")
                        c += n
                        off = int.from_bytes(b[c : c + 2], "little")
                        c += 2
                        ti, c = idx(b, c)
                        pubs.append((name, si, off))
                elif r.name == "LEDATA":
                    si, c = idx(b, 0)
                    need(
                        0 < si < len(segs) and c + 2 <= len(b),
                        "LEDATA segment/offset bounds",
                    )
                    off = int.from_bytes(b[c : c + 2], "little")
                    data = b[c + 2 :]
                    need(
                        off + len(data) <= segs[si]["size"],
                        "LEDATA outside SEGDEF extent",
                    )
                    last = dict(
                        segment=si, offset=off, data=data, record_offset=r.offset - 5
                    )
                    blocks.append(last)
                elif r.name == "FIXUPP":
                    need(last is not None, "FIXUPP without LEDATA")
                    c = 0
                    while c < len(b):
                        loc = b[c]
                        need(loc & 128, "thread FIXUPP deferred")
                        need(c + 3 <= len(b), "truncated FIXUPP")
                        relative = not bool(loc & 64)
                        kind = (loc >> 2) & 15
                        site = ((loc & 3) << 8) | b[c + 1]
                        dat = b[c + 2]
                        c += 3
                        need(not dat & 128 and not dat & 8, "threaded FIXUPP deferred")
                        fm = (dat >> 4) & 7
                        tm = dat & 3
                        if fm <= 2:
                            fd, c = idx(b, c)
                        elif fm in (4, 5):
                            fd = None
                        else:
                            raise ValueError("unsupported frame method " + str(fm))
                        td, c = idx(b, c)
                        disp = 0
                        if not dat & 4:
                            need(c + 2 <= len(b), "fixup displacement")
                            disp = int.from_bytes(b[c : c + 2], "little")
                            c += 2
                        need(kind in (1, 2, 3), "unsupported location " + str(kind))
                        width = {1: 2, 2: 2, 3: 4}[kind]
                        need(site + width <= len(last["data"]), "FIXUPP crosses LEDATA")
                        fix.append(
                            dict(
                                segment=last["segment"],
                                site=last["offset"] + site,
                                kind=kind,
                                relative=relative,
                                frame_method=fm,
                                frame_index=fd,
                                target_method=tm,
                                target_index=td,
                                displacement=disp,
                                record_offset=r.offset - 5,
                            )
                        )
            mods[member.name.casefold()] = dict(
                name=member.name,
                program_sha256=sha(member.program_records),
                program_records=member.program_records,
                segs=segs,
                groups=grps,
                exts=exts,
                pubs=pubs,
                blocks=blocks,
                fixups=fix,
                records=collections.Counter(r.name for r in recs),
            )
        self.contribs, self.groups, self.segbases = contribs, groups, segbases
        self.pubmap, self.mods = pubmap, mods
        self.rawpub = collections.defaultdict(list)
        for mod in mods.values():
            for name, si, off in mod["pubs"]:
                if not si:
                    continue
                try:
                    con = self.contribution(mod, si)
                    need(off <= con["size"], "PUBDEF outside segment")
                    segname = mod["segs"][si]["name"].casefold()
                    frame = (
                        groups[con["group"].casefold()]
                        if con["group"] != "(none)"
                        else segbases[segname] // 16 * 16
                    )
                    self.rawpub[name].append(
                        (frame, con["start"] + off - frame, mod["name"])
                    )
                except (ValueError, KeyError):
                    # Unlinked members may have no MAP contribution. A later
                    # referenced external still must resolve uniquely or fail.
                    pass

    def contribution(self, mod, si):
        seg = mod["segs"][si]
        matches = [
            x
            for x in self.contribs
            if x["module"].casefold() == mod["name"].casefold()
            and x["segment"].casefold() == seg["name"].casefold()
            and x["cl"] == seg["cl"]
        ]
        need(
            len(matches) == 1,
            "missing/duplicate contribution " + mod["name"] + "/" + seg["name"],
        )
        m = matches[0]
        need(m["size"] == seg["size"], "SEGDEF/MAP extent differs")
        return m

    def external(self, name):
        rows = {(f, o) for f, o, m in self.rawpub.get(name, [])}
        direct = self.pubmap.get(name, set())
        if rows and direct:
            need(rows == direct, "public MAP/library resolution disagrees " + name)
        result = rows or direct
        need(len(result) == 1, "unresolved/ambiguous external " + name)
        frame, off = next(iter(result))
        return frame, off

    def verify(self, mod, con):
        matches = [
            i
            for i, s in enumerate(mod["segs"])
            if s and s["name"] == con["segment"] and s["cl"] == "CODE"
        ]
        need(len(matches) == 1, "ambiguous complete CODE SEGDEF")
        si = matches[0]
        seg = mod["segs"][si]
        size = seg["size"]
        need(size == con["size"], "complete CODE size")
        allowed = {
            "THEADR",
            "COMENT",
            "LNAMES",
            "SEGDEF",
            "GRPDEF",
            "EXTDEF",
            "PUBDEF",
            "LEDATA",
            "FIXUPP",
            "ALIAS",
            "MODEND",
        }
        need(not set(mod["records"]) - allowed, "unsupported transformation record")
        body = bytearray(size)
        cover = bytearray(size)
        blks = [x for x in mod["blocks"] if x["segment"] == si]
        for block in blks:
            a = block["offset"]
            b = a + len(block["data"])
            need(b <= size and not any(cover[a:b]), "overlap/outside CODE LEDATA")
            body[a:b] = block["data"]
            cover[a:b] = b"\1" * (b - a)
        need(all(cover), "CODE LEDATA gap")
        object_sha = sha(body)
        writes = set()
        actions = []
        mz = []

        def target_binding(f):
            tm = f["target_method"]
            ti = f["target_index"]
            if tm == 0:
                need(0 < ti < len(mod["segs"]), "FIXUPP target SEGDEF index bounds")
                targetcon = self.contribution(mod, ti)
                targetseg = mod["segs"][ti]
                name = targetseg["name"]
                frame = (
                    self.groups[targetcon["group"].casefold()]
                    if targetcon["group"] != "(none)"
                    else self.segbases[name.casefold()] // 16 * 16
                )
                return frame, targetcon["start"] - frame, "segment:" + name
            if tm == 2:
                need(0 < ti < len(mod["exts"]), "FIXUPP target EXTDEF index bounds")
                name = mod["exts"][ti]
                frame, off = self.external(name)
                return frame, off, "external:" + name
            raise ValueError("unsupported target method " + str(tm))

        for f in mod["fixups"]:
            if f["segment"] != si:
                continue
            site = f["site"]
            kind = f["kind"]
            width = {1: 2, 2: 2, 3: 4}[kind]
            a = site
            b = site + width
            tf, to, name = target_binding(f)
            fm = f["frame_method"]
            if fm == 5:
                frame = tf
            elif fm == 1:
                frame = self.groups[mod["groups"][f["frame_index"]]["name"].casefold()]
            elif fm == 0:
                frame = (
                    self.segbases[mod["segs"][f["frame_index"]]["name"].casefold()]
                    // 16
                    * 16
                )
            else:
                raise ValueError("unsupported frame method")
            old = int.from_bytes(body[site : site + 2], "little")
            disp = f["displacement"]
            targetlinear = tf + to + disp
            if kind == 1:
                value = (
                    old
                    + targetlinear
                    - (con["start"] + site + 2 if f["relative"] else frame)
                ) & 65535
                after = value.to_bytes(2, "little")
                mode = "self-relative16" if f["relative"] else "offset16"
            elif kind == 2:
                need(not f["relative"], "relative segment word")
                value = (old + frame // 16) & 65535
                after = value.to_bytes(2, "little")
                mz.append(site)
                mode = "segment16"
            else:
                need(not f["relative"], "relative far pointer")
                oldseg = int.from_bytes(body[site + 2 : site + 4], "little")
                off = (old + targetlinear - frame) & 65535
                segment = (oldseg + frame // 16) & 65535
                after = off.to_bytes(2, "little") + segment.to_bytes(2, "little")
                mode = "far-pointer16:16"
                # Observed TLINK same-segment far CALL shortening pattern: preserve
                # its five-byte footprint as NOP / PUSH CS / CALL rel16, bound to real symbol.
                sourceframe = self.segbases[con["segment"].casefold()] // 16 * 16
                if site and body[site - 1] == 0x9A and segment == sourceframe // 16:
                    rel = (old + targetlinear - (con["start"] + site + 4)) & 65535
                    smart = b"\x90\x0e\xe8" + rel.to_bytes(2, "little")
                    actual = self.cal.program_image[
                        con["start"] + site - 1 : con["start"] + site + 4
                    ]
                    if actual == smart:
                        a = site - 1
                        after = smart
                        mode = "TLINK same-segment far-call NOP/PUSHCS/CALL"
                    else:
                        mz.append(site + 2)
                else:
                    mz.append(site + 2)
            need(not writes.intersection(range(a, b)), "overlapping FIXUPP writes")
            writes.update(range(a, b))
            body[a:b] = after
            actions.append(
                {
                    **f,
                    "binding": name,
                    "resolved_target_frame": tf,
                    "resolved_target_offset": to,
                    "resolved_frame": frame,
                    "operation": mode,
                    "write_start": a,
                    "write_size": b - a,
                    "expected_bytes_sha256": sha(after),
                }
            )
        expected = bytes(body)
        candidate = self.cal.program_image[con["start"] : con["start"] + size]
        original = self.target.program_image[con["start"] : con["start"] + size]
        need(
            expected == candidate,
            "reconstructed OMF/link bytes differ ("
            + str(sum(a != b for a, b in zip(expected, candidate)))
            + " bytes)",
        )
        need(candidate == original, "candidate/original complete bytes differ")
        need(
            relative_fixups(self.cal, con["start"], size) == mz,
            "calibration ordered MZ fixups differ from OMF",
        )
        need(
            relative_fixups(self.target, con["start"], size) == mz,
            "target ordered MZ fixups differ from OMF",
        )
        need(
            self.target.program_image.find(original) == con["start"]
            and self.target.program_image.find(original, con["start"] + 1) < 0,
            "nonunique complete occurrence",
        )
        return dict(
            status="proven-complete-vendor-CODE-proposal",
            member=mod["name"],
            start=con["start"],
            end=con["start"] + size,
            size=size,
            segment=con["segment"],
            class_name=con["cl"],
            member_program_sha256=mod["program_sha256"],
            original_unlinked_CODE_sha256=object_sha,
            linked_CODE_sha256=sha(expected),
            SEGDEF=seg,
            CODE_LEDATA=[
                dict(
                    offset=b["offset"],
                    size=len(b["data"]),
                    record_offset=b["record_offset"],
                    sha256=sha(b["data"]),
                )
                for b in blks
            ],
            complete_gapless_CODE_LEDATA=True,
            member_record_counts=dict(mod["records"]),
            ordered_MZ_fixups=mz,
            fixup_actions=actions,
            unique_original_occurrence=True,
        )


def deferred_reservations(review, mod, con):
    """Describe unresolved SEGDEF reservations; never silently zero-fill them."""
    si = next(
        i
        for i, s in enumerate(mod["segs"])
        if s and s["name"] == con["segment"] and s["cl"] == "CODE"
    )
    cover = bytearray(con["size"])
    ledata = []
    for block in mod["blocks"]:
        if block["segment"] != si:
            continue
        start, payload = block["offset"], block["data"]
        end = start + len(payload)
        need(
            end <= len(cover) and not any(cover[start:end]),
            "deferred LEDATA overlap/bounds",
        )
        cover[start:end] = b"\1" * len(payload)
        ledata.append(dict(offset=start, size=len(payload), sha256=sha(payload)))
    lidata = []

    def expand(data, cursor, depth=0):
        need(depth < 16 and cursor + 4 <= len(data), "LIDATA depth/truncation")
        repeat = int.from_bytes(data[cursor : cursor + 2], "little")
        count = int.from_bytes(data[cursor + 2 : cursor + 4], "little")
        cursor += 4
        if count:
            parts = []
            for _ in range(count):
                part, cursor = expand(data, cursor, depth + 1)
                parts.append(part)
                need(sum(map(len, parts)) <= con["size"], "LIDATA expansion bound")
            atom = b"".join(parts)
        else:
            need(cursor < len(data), "LIDATA literal length")
            length = data[cursor]
            cursor += 1
            need(cursor + length <= len(data), "LIDATA literal truncation")
            atom, cursor = data[cursor : cursor + length], cursor + length
        need(len(atom) * repeat <= con["size"], "LIDATA repeat bound")
        return atom * repeat, cursor

    # Raw records are parsed again solely to inspect the deferred LIDATA form.
    for record in parse_omf(bytes.fromhex("800200007e") + mod["program_records"]):
        if record.name != "LIDATA":
            continue
        segment, cursor = idx(record.data, 0)
        need(cursor + 2 <= len(record.data), "LIDATA offset truncation")
        offset = int.from_bytes(record.data[cursor : cursor + 2], "little")
        cursor += 2
        parts = []
        while cursor < len(record.data):
            part, cursor = expand(record.data, cursor)
            parts.append(part)
            need(sum(map(len, parts)) <= con["size"], "LIDATA total bound")
        payload = b"".join(parts)
        need(
            segment == si and offset + len(payload) <= len(cover),
            "unsupported deferred LIDATA segment/bounds",
        )
        need(not any(cover[offset : offset + len(payload)]), "LIDATA overlaps LEDATA")
        cover[offset : offset + len(payload)] = b"\1" * len(payload)
        need(
            payload
            == review.cal.program_image[
                con["start"] + offset : con["start"] + offset + len(payload)
            ],
            "LIDATA/calibration mismatch",
        )
        lidata.append(dict(offset=offset, size=len(payload), sha256=sha(payload)))
    gaps = []
    cursor = 0
    while cursor < len(cover):
        if cover[cursor]:
            cursor += 1
            continue
        end = cursor + 1
        while end < len(cover) and not cover[end]:
            end += 1
        a, b = con["start"] + cursor, con["start"] + end
        need(
            review.target.program_image[a:b]
            == review.cal.program_image[a:b]
            == bytes(end - cursor),
            "deferred reservation is not observed zero",
        )
        need(
            not relative_fixups(review.target, a, b - a),
            "relocation inside deferred reservation",
        )
        gaps.append(
            dict(
                offset=cursor,
                size=end - cursor,
                original_start=a,
                original_end=b,
                original_and_calibration_zero=True,
                ordered_MZ_fixups=[],
            )
        )
        cursor = end
    return dict(
        member=mod["name"],
        start=con["start"],
        end=con["start"] + con["size"],
        size=con["size"],
        member_program_sha256=mod["program_sha256"],
        linked_CODE_sha256=sha(
            review.target.program_image[con["start"] : con["start"] + con["size"]]
        ),
        CODE_LEDATA=ledata,
        LIDATA=lidata,
        unwritten_SEGDEF_ranges=gaps,
        decision="deferred-no-exclusion; no implicit zero-fill ownership exemption",
    )


def review_inputs(root: Path = ROOT) -> dict:
    library = root / ".analysis/toolchain/installed/tc40j/LIB/CL.LIB"
    base = root / ".analysis/builds/main-calibration-b/source"
    inputs = {
        "library_sha256": library.read_bytes(),
        "calibration_map_sha256": (base / "obj/th05/main.map").read_bytes(),
        "calibration_exe_sha256": (base / "bin/th05/main.exe").read_bytes(),
    }
    need(
        sha((root / "config/toolchain.toml").read_bytes())
        == PINS["toolchain_manifest_sha256"],
        "toolchain manifest pin mismatch",
    )
    for key, raw in inputs.items():
        need(sha(raw) == PINS[key], "private input pin mismatch: " + key)
    context = UnitContext(root, "main")
    artifact, target, _ = load_unit_target(context, context.config())
    need(
        artifact["sha256"] == PINS["target_sha256"]
        and sha(target.program_image) == PINS["target_payload_sha256"],
        "original target pin mismatch",
    )
    candidate = parse_mz(inputs["calibration_exe_sha256"])
    need(candidate.valid, "invalid retained calibration MZ")
    review = VendorReview(
        inputs["library_sha256"], inputs["calibration_map_sha256"], candidate, target
    )
    nominated = []
    for con in review.contribs:
        if (
            con["cl"] != "CODE"
            or not con["size"]
            or con["module"].casefold() not in review.mods
        ):
            continue
        a, size = con["start"], con["size"]
        if candidate.program_image[a : a + size] == target.program_image[
            a : a + size
        ] and relative_fixups(candidate, a, size) == relative_fixups(target, a, size):
            nominated.append(con)
    need(
        len(nominated) == 33 and sum(x["size"] for x in nominated) == 4949,
        "nominated inventory drift",
    )
    rows, deferred = [], []
    for con in nominated:
        mod = review.mods[con["module"].casefold()]
        if mod["name"] in ("farheap", "exec"):
            deferred.append(deferred_reservations(review, mod, con))
        else:
            rows.append(review.verify(mod, con))
    result = dict(
        schema_version=1,
        kind="pinned-vendor-ownership-evidence",
        artifact="th05-main",
        compiler_invocations=0,
        authored_credit=0,
        denominator_changed=False,
        **PINS,
        library="CL.LIB",
        library_member_count=len(review.mods),
        library_parser_sha256=sha(
            (root / "scripts/lib/borland_library.py").read_bytes()
        ),
        upstream_library_parser_sha256=UPSTREAM_PARSER_SHA256,
        verifier_sha256=sha((root / "scripts/review_vendor.py").read_bytes()),
        proposed_contribution_count=len(rows),
        proposed_bytes=sum(x["size"] for x in rows),
        classification="third-party compiler/runtime library contribution; CODE is OMF class, not instruction-only",
        contributions=rows,
        deferred=deferred,
    )
    validate_metadata(result)
    return result


def validate_metadata(meta: dict, *, root: Path = ROOT) -> dict:
    """Public structure only. Byte proof requires the private --check replay."""
    need(
        meta.get("schema_version") == 1
        and meta.get("kind") == "pinned-vendor-ownership-evidence"
        and meta.get("artifact") == "th05-main",
        "metadata schema/artifact",
    )
    for key, value in PINS.items():
        need(meta.get(key) == value, "metadata pin mismatch: " + key)
    need(
        meta.get("compiler_invocations") == 0
        and meta.get("authored_credit") == 0
        and meta.get("denominator_changed") is False,
        "metadata cannot grant authored credit or alter denominator",
    )
    need(
        meta.get("library_member_count") == 893 and meta.get("library") == "CL.LIB",
        "library identity/count",
    )

    def integer(value, low, high):
        need(
            type(value) is int and low <= value <= high,
            "integer outside metadata bounds",
        )
        return value

    def hash_value(value):
        need(
            isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value),
            "malformed evidence hash",
        )

    for key in (
        "library_parser_sha256",
        "upstream_library_parser_sha256",
        "verifier_sha256",
    ):
        hash_value(meta.get(key))
    need(
        meta["upstream_library_parser_sha256"] == UPSTREAM_PARSER_SHA256,
        "upstream parser provenance",
    )
    for key, relative in (
        ("library_parser_sha256", "scripts/lib/borland_library.py"),
        ("verifier_sha256", "scripts/review_vendor.py"),
        ("toolchain_manifest_sha256", "config/toolchain.toml"),
    ):
        need(
            sha((root / relative).read_bytes()) == meta[key],
            "public verifier/parser/toolchain source drift: " + relative,
        )
    rows, deferred = meta.get("contributions", []), meta.get("deferred", [])
    need(
        len(rows) == meta.get("proposed_contribution_count") == 31
        and sum(x["size"] for x in rows) == meta.get("proposed_bytes") == 2901,
        "complete contribution totals",
    )
    seen, extents = set(), []
    for row in rows + deferred:
        name = row.get("member")
        need(
            isinstance(name, str)
            and re.fullmatch("[a-zA-Z0-9_@$]{1,8}", name)
            and name not in seen,
            "duplicate/unsafe member",
        )
        seen.add(name)
        a, size = (
            integer(row.get("start"), 0, 145957),
            integer(row.get("size"), 1, 65535),
        )
        need(row.get("end") == a + size <= 145958, "contribution end outside original")
        extents.append((a, a + size))
        hash_value(row.get("member_program_sha256"))
        hash_value(row.get("linked_CODE_sha256"))
    for (_, end), (start, _) in zip(sorted(extents), sorted(extents)[1:]):
        need(end <= start, "overlapping vendor extents")
    for row in rows:
        size = row["size"]
        need(
            row.get("status") == "proven-complete-vendor-CODE-proposal"
            and row.get("segment") == "_TEXT"
            and row.get("class_name") == "CODE",
            "unsupported contribution class/status",
        )
        need(
            row.get("complete_gapless_CODE_LEDATA") is True
            and row.get("unique_original_occurrence") is True,
            "missing complete byte/boundary proof",
        )
        seg = row.get("SEGDEF", {})
        need(
            seg == dict(name="_TEXT", cl="CODE", size=size, acbp=0x28),
            "complete SEGDEF disagrees",
        )
        hash_value(row.get("original_unlinked_CODE_sha256"))
        covered = set()
        for block in row.get("CODE_LEDATA", []):
            a, n = (
                integer(block.get("offset"), 0, size - 1),
                integer(block.get("size"), 1, size),
            )
            need(
                a + n <= size and not covered.intersection(range(a, a + n)),
                "LEDATA overlap/bounds",
            )
            covered.update(range(a, a + n))
            hash_value(block.get("sha256"))
            integer(block.get("record_offset"), 0, 1048576)
        need(len(covered) == size, "LEDATA full extent missing")
        writes, expected_mz = set(), []
        for action in row.get("fixup_actions", []):
            site = integer(action.get("site"), 0, size - 1)
            kind = action.get("kind")
            need(type(kind) is int and kind in (1, 2, 3), "unsupported FIXUPP location")
            need(
                action.get("frame_method") in (0, 1, 5)
                and action.get("target_method") in (0, 2),
                "unsupported FIXUPP method",
            )
            integer(action.get("target_index"), 1, 65535)
            integer(action.get("segment"), 1, 65535)
            integer(action.get("displacement"), 0, 65535)
            for key in ("resolved_target_frame", "resolved_frame"):
                integer(action.get(key), 0, 0xFFFF0)
            integer(action.get("resolved_target_offset"), 0, 65535)
            need(
                action["resolved_target_frame"] % 16
                == action["resolved_frame"] % 16
                == 0,
                "unaligned resolved frame",
            )
            binding = action.get("binding")
            need(
                isinstance(binding, str)
                and (binding.startswith("segment:") or binding.startswith("external:"))
                and "/" not in binding
                and "\\" not in binding,
                "unsafe/unresolved binding",
            )
            start, n = action.get("write_start"), action.get("write_size")
            smart = (
                action.get("operation") == "TLINK same-segment far-call NOP/PUSHCS/CALL"
            )
            need(
                (start, n) == (site - 1, 5)
                if smart
                else (start, n) == (site, {1: 2, 2: 2, 3: 4}[kind]),
                "FIXUPP write width/site disagrees",
            )
            need(not smart or kind == 3, "smart CALL needs real far-pointer fixup")
            need(
                0 <= start < start + n <= size
                and not writes.intersection(range(start, start + n)),
                "FIXUPP write overlap/bounds",
            )
            writes.update(range(start, start + n))
            hash_value(action.get("expected_bytes_sha256"))
            if kind == 2:
                expected_mz.append(site)
            elif kind == 3 and not smart:
                expected_mz.append(site + 2)
        need(
            row.get("ordered_MZ_fixups") == expected_mz,
            "ordered MZ relocation metadata differs from FIXUPP actions",
        )
    need(
        {x["member"] for x in deferred} == {"farheap", "exec"} and len(deferred) == 2,
        "deferred members changed",
    )
    expected_gaps = {"farheap": [(6, 6)], "exec": [(356, 2)]}
    for row in deferred:
        need(
            row.get("decision")
            == "deferred-no-exclusion; no implicit zero-fill ownership exemption",
            "deferred policy changed",
        )
        gaps = row.get("unwritten_SEGDEF_ranges", [])
        need(
            [(x["offset"], x["size"]) for x in gaps] == expected_gaps[row["member"]],
            "unwritten reservation boundaries changed",
        )
        for gap in gaps:
            need(
                gap.get("original_start") == row["start"] + gap["offset"]
                and gap.get("original_end") == gap["original_start"] + gap["size"]
                and gap.get("original_and_calibration_zero") is True
                and gap.get("ordered_MZ_fixups") == [],
                "deferred reservation evidence",
            )

    # The generated metadata contains hashes/identities, never raw CODE or local paths.
    def public_only(value):
        if isinstance(value, dict):
            for key, item in value.items():
                need(
                    key
                    not in (
                        "data",
                        "raw",
                        "program_records",
                        "path",
                        "library_parser_path",
                    ),
                    "private/raw evidence is not public metadata",
                )
                public_only(item)
        elif isinstance(value, list):
            for item in value:
                public_only(item)
        elif isinstance(value, str):
            need(
                not value.startswith(("/home/", "/mnt/", "C:\\", "D:\\")),
                "private absolute path",
            )

    public_only(meta)
    return dict(
        kind="public-metadata-structure-only",
        contributions=31,
        proposed_bytes=2901,
        deferred_members=2,
        byte_proof_replayed=False,
        authored_credit=0,
        denominator_changed=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument(
        "--check",
        action="store_true",
        help="replay private inputs and compare public metadata",
    )
    modes.add_argument(
        "--write",
        action="store_true",
        help="replay private inputs and write evidence metadata only",
    )
    modes.add_argument(
        "--structural-check",
        action="store_true",
        help="check public metadata without proprietary/private inputs",
    )
    args = parser.parse_args()
    path = ROOT / "config/vendor_ownership.json"
    if args.structural_check:
        print(json.dumps(validate_metadata(json.loads(path.read_text())), indent=2))
        return 0
    result = review_inputs()
    if args.write:
        path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        need(
            json.loads(path.read_text()) == result,
            "saved vendor metadata differs from replayed private evidence",
        )
    print(
        json.dumps(
            dict(
                kind="native-private-vendor-byte-review",
                contributions=31,
                proposed_bytes=2901,
                deferred_members=2,
                compiler_invocations=0,
                metadata_written=args.write,
                denominator_changed=False,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

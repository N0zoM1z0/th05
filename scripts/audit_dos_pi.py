#!/usr/bin/env python3
"""Relink the DOS product executables with moved CODE and DGROUP contributions.

Position independence (PI) means every memory reference is symbolic, so code
and data can move. This audit takes the objects of a `scripts/build.py`
product build, relinks them unchanged (the control must reproduce the EXE and
MAP byte for byte), then inserts padding contributions after the first
definition of every public CODE segment and every DGROUP DATA/BSS segment and
relinks again. Each original contribution keeps its size and must move. The
check then maps every MZ relocation site, immediate far CALL/JMP target, far
data pointer and direct 16-bit CS/DS displacement back to its MAP owner and
requires the same owner-relative target in the shifted image.

Direct displacements that do not follow their owner are written to
`direct-offset-review.json` for source review; they are candidates, not
failures, because a constant can look like an address. The method follows
TH04's `audit_th04_dos_pi.py`.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import defaultdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import NamedTuple

from lib.omf import parse_omf
from lib.pc98 import MZImage, parse_mz
from lib.unit_oracle import map_publics

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = (ROOT / ".analysis").resolve()
EXES = {"main": "MAIN.EXE", "op": "OP.EXE", "maine": "MAINE.EXE"}
MSDOS = ROOT / "_reference/ReC98/bin/msdos.exe"
PREFIX = ROOT / ".analysis/toolchain/wineprefix"
MAP_ROW = re.compile(
    r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
    r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=([0-9A-F]{2})")
ALIGNMENTS = {1: "byte", 2: "word", 3: "para", 4: "page", 5: "dword"}


class Contribution(NamedTuple):
    frame: int
    offset: int
    size: int
    kind: str
    name: str
    group: str
    module: str
    acbp: int

    @property
    def start(self) -> int:
        return self.frame * 16 + self.offset

    @property
    def owner(self) -> tuple[str, str, str, str]:
        return self.kind, self.name, self.group.lower(), self.module.lower()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def map_rows(path: Path) -> list[Contribution]:
    rows = []
    for line in path.read_text(encoding="cp437").splitlines():
        match = MAP_ROW.fullmatch(line.rstrip())
        if match:
            frame, offset, size, kind, name, group, module, acbp = match.groups()
            rows.append(Contribution(int(frame, 16), int(offset, 16), int(size, 16),
                                     kind, name, group, module, int(acbp, 16)))
    if not rows:
        raise ValueError(f"no detailed TLINK contributions in {path}")
    return rows


def run(work: Path, log: str, *args: str) -> None:
    env = dict(os.environ, WINEPREFIX=str(PREFIX), WINEDEBUG="-all", MSDOS_PATH=r"C:\TC4\BIN")
    process = subprocess.run(["wine", *args], cwd=work, env=env, capture_output=True, timeout=300)
    (work / log).write_bytes(json.dumps(args).encode() + b"\n" + process.stdout + process.stderr)
    if process.returncode or re.search(rb"(?m)^(?:\*\*(?:Error|Fatal)\*\*|Error:|Fatal:|Error [A-Z])", process.stdout + process.stderr):
        raise ValueError(f"tool failed with status {process.returncode}, see {work / log}")


def tlink(work: Path, response: str, log: str) -> None:
    run(work, log, str(MSDOS), "-e", "-x", "tlink", "@" + response.replace("/", "\\"))


def omf_module(data: bytes) -> str:
    name = parse_omf(data)[0].data
    return name[1:1 + name[0]].decode("cp437").lower()


def read_response(path: Path) -> tuple[list[str], str]:
    text = path.read_bytes().decode("ascii").replace("+\r\n", " ").strip()
    objects_text, files_text = text.split(",", 1)
    return objects_text.split(), files_text


def write_response(path: Path, args: list[str], files_text: str) -> None:
    lines, line = [], []
    for arg in args:
        line.append(arg)
        if len(" ".join(line)) > 100:
            lines.append(" ".join(line))
            line = []
    if line:
        lines.append(" ".join(line))
    path.write_bytes(("+\r\n".join(lines) + "," + files_text + "\r\n").encode("ascii"))


def pad_objects(rows: list[Contribution], modules: list[str], work: Path,
                padding: dict[str, int]) -> dict[int, str]:
    """Insert padding after the first module defining each public segment."""
    definitions = defaultdict(list)
    for row in rows:
        if row.kind == "CODE" or (row.kind in {"DATA", "BSS"} and row.group.upper() == "DGROUP"):
            definitions[row.kind, row.name].append(row)
    contents = defaultdict(list)
    for (kind, name), found in definitions.items():
        if not any(row.size for row in found):
            continue
        known = [(modules.index(row.module.lower()), row.acbp)
                 for row in found if row.module.lower() in modules]
        if not known:
            continue
        index, acbp = min(known)
        if (acbp >> 2) & 7 != 2 or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            continue
        fill = {"CODE": "90h", "DATA": "0", "BSS": "?"}[kind]
        contents[index].extend([f"{name} segment {ALIGNMENTS[acbp >> 5]} public '{kind}' use16",
                                f"    db {padding[kind]} dup({fill})", f"{name} ends"])
    objects = {}
    for index, lines in sorted(contents.items()):
        stem = f"pi{index:05d}"
        (work / "obj/pi").mkdir(parents=True, exist_ok=True)
        (work / f"obj/pi/{stem}.asm").write_text("\n".join([".386", *lines, "end", ""]), encoding="ascii")
        run(work, f"obj/pi/{stem}.log", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx",
            f"obj\\pi\\{stem}.asm", f"obj\\pi\\{stem}.obj")
        parse_omf((work / f"obj/pi/{stem}.obj").read_bytes())
        objects[index] = f"obj\\pi\\{stem}.obj"
    if not objects:
        raise ValueError("no eligible CODE or DGROUP segments for padding")
    return objects


def owner_of(pairs, starts, linear):
    index = bisect_right(starts, linear) - 1
    if index < 0:
        return None
    old, new = pairs[index]
    return (old, new) if linear < old.start + old.size else None


def direct_offsets(before: bytes, after: bytes, pairs, starts, publics: list[int]) -> dict:
    """Screen direct CS/DS displacements whose owner moved.

    Decoding restarts at every MAP public so that embedded tables cannot
    desynchronize the rest of a contribution.
    """
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    from capstone.x86_const import X86_OP_MEM, X86_REG_CS, X86_REG_DS, X86_REG_INVALID

    dgroup = next((old.frame, new.frame) for old, new in pairs if old.group.upper() == "DGROUP")
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    decoder.skipdata = True
    candidates, screened, moved, seen = [], 0, 0, set()
    for old, new in pairs:
        if old.kind != "CODE":
            continue
        entries = [old.start] + [p for p in publics if old.start < p < old.start + old.size]
        instructions = []
        for begin, end in zip(entries, entries[1:] + [old.start + old.size]):
            for ins in decoder.disasm(before[begin:end], begin - old.start + old.offset):
                if (old.frame, ins.address) not in seen:
                    seen.add((old.frame, ins.address))
                    instructions.append(ins)
        for ins in instructions:
            if not ins.id or ins.disp_size != 2:
                continue
            for op in ins.operands:
                if op.type != X86_OP_MEM or op.mem.base or op.mem.index:
                    continue
                if op.mem.segment not in (X86_REG_CS, X86_REG_DS, X86_REG_INVALID):
                    continue
                cs = op.mem.segment == X86_REG_CS
                old_base, new_base = (old.frame, new.frame) if cs else dgroup
                offset = op.mem.disp & 0xFFFF
                hit = owner_of(pairs, starts, old_base * 16 + offset)
                if not hit or (cs and hit[0].kind != "CODE") or (not cs and hit[0].group.upper() != "DGROUP"):
                    continue
                old_target, new_target = hit
                expected = (new_target.start + old_base * 16 + offset - old_target.start - new_base * 16) & 0xFFFF
                at = new.start + ins.address - old.offset + ins.disp_offset
                actual = int.from_bytes(after[at:at + 2], "little")
                screened += 1
                if actual != expected:
                    candidates.append({"address": f"{old.frame:04X}:{ins.address:04X}", "module": old.module,
                                       "operand": f"{ins.mnemonic} {ins.op_str}",
                                       "target_module": old_target.module, "target_segment": old_target.name,
                                       "baseline": offset, "shifted": actual, "expected": expected})
                elif actual != offset:
                    moved += 1
    return {"screened": screened, "moved": moved, "candidates": candidates}


def switch_tables(before: bytes, after: bytes, pairs) -> tuple[int, int, list[tuple[int, int]]]:
    """Check compiler switch tables: `cmp bx, N` ... `jmp word ptr cs:[bx+T]`.

    Each of the N+1 near offsets must still name the same code inside its
    contribution. Returns tables, entries and the table extents.
    """
    tables = entries = 0
    extents = []
    for old, new in pairs:
        if old.kind != "CODE":
            continue
        blob = before[old.start:old.start + old.size]
        for match in re.finditer(rb"\x2e\xff[\xa4-\xa7]", blob):
            if match.end() + 2 > len(blob):
                continue
            window = blob[max(0, match.start() - 24):match.start()]
            bounds = list(re.finditer(rb"(?:\x83[\xf8-\xff](.)|\x3d(..)|\x81[\xf8-\xff](..))"
                                      rb"(?:[\x76\x77].|\x0f[\x86\x87]..)", window, re.S))
            if not bounds:
                continue
            raw = next(g for g in bounds[-1].groups() if g is not None)
            limit = int.from_bytes(raw, "little")
            # Without `add bx, bx` or `shl bx, 1` the compared value is already a byte offset.
            doubled = re.search(rb"\x03\xdb|\x01\xdb|\xd1\xe3", window[bounds[-1].end():])
            count = limit + 1 if doubled else limit // 2 + 1
            if count > 512:
                continue
            table = old.frame * 16 + int.from_bytes(blob[match.end():match.end() + 2], "little")
            if not (old.start <= table and table + 2 * count <= old.start + old.size):
                continue
            for k in range(count):
                site = table + 2 * k
                value = int.from_bytes(before[site:site + 2], "little")
                target = old.frame * 16 + value
                moved = new.start + site - old.start
                expected = (new.start + target - old.start - new.frame * 16) & 0xFFFF
                if not old.start <= target < old.start + old.size:
                    raise ValueError(f"switch table entry at {site:#x} leaves {old.module}")
                if int.from_bytes(after[moved:moved + 2], "little") != expected:
                    raise ValueError(f"switch table entry at {site:#x} ({old.module}) lost its case")
            tables += 1
            entries += count
            extents.append((table, table + 2 * count))
    return tables, entries, extents


def compare_layout(original: MZImage, shifted: MZImage, old_rows, new_rows, synthetic: set[str],
                   publics: list[int]):
    if not original.valid or not shifted.valid:
        raise ValueError("invalid MZ")
    new_by_owner = defaultdict(list)
    for row in new_rows:
        if row.size and row.module.lower() not in synthetic:
            new_by_owner[row.owner].append(row)
    moved, target_frames, pairs = defaultdict(int), defaultdict(set), []
    for old in old_rows:
        if not old.size:
            continue
        if not new_by_owner[old.owner]:
            raise ValueError(f"lost MAP contribution {old.owner}")
        new = new_by_owner[old.owner].pop(0)
        if old.size != new.size:
            raise ValueError(f"size changed for {old.owner}")
        pairs.append((old, new))
        target_frames[old.frame].add(new.frame)
        if old.start != new.start:
            moved[old.kind] += 1
    if any(new_by_owner.values()):
        raise ValueError("unexpected extra MAP contributions")
    if any(moved[kind] == 0 for kind in ("CODE", "DATA", "BSS")):
        raise ValueError(f"CODE, DATA and BSS must all move: {dict(moved)}")
    # A public segment can have a paragraph frame of its own inside a wider group.
    sections = []
    for rows in (old_rows, new_rows):
        first = {}
        for row in sorted(rows, key=lambda r: r.start):
            first.setdefault((row.kind, row.name), row.start)
        sections.append(first)
    for section, start in sections[0].items():
        if section in sections[1]:
            target_frames[start >> 4].add(sections[1][section] >> 4)
    pairs.sort(key=lambda pair: pair[0].start)
    starts = [old.start for old, _ in pairs]
    old_image, new_image = original.program_image, shifted.program_image
    expected, unmapped, far_transfers, far_pointers = [], set(), 0, 0
    for relocation in original.relocations:
        site = relocation.linear
        hit = owner_of(pairs, starts, site)
        if not hit or site + 2 > hit[0].start + hit[0].size:
            raise ValueError(f"unowned baseline relocation at {site:#x}")
        old, new = hit
        new_site = new.start + site - old.start
        expected.append(new_site)
        old_frame = int.from_bytes(old_image[site:site + 2], "little")
        new_frame = int.from_bytes(new_image[new_site:new_site + 2], "little")
        if new_frame not in target_frames[old_frame]:
            unmapped.add((old_frame, new_frame))
        if old.kind == "CODE" and site - 3 >= old.start and old_image[site - 3] in (0x9A, 0xEA):
            # Immediate far CALL/JMP: offset word, then the relocated segment.
            destination = old_frame * 16 + int.from_bytes(old_image[site - 2:site], "little")
            target = owner_of(pairs, starts, destination)
            if target and target[0].kind == "CODE":
                new_destination = new_frame * 16 + int.from_bytes(new_image[new_site - 2:new_site], "little")
                if (old_image[site - 3] != new_image[new_site - 3]
                        or new_destination != target[1].start + destination - target[0].start):
                    raise ValueError(f"far transfer at {site - 3:#x} ({old.module}) lost its code target")
                far_transfers += 1
        elif old.kind != "CODE" and site - 2 >= old.start:
            # Far pointer in initialized data: offset word, then the relocated segment.
            destination = old_frame * 16 + int.from_bytes(old_image[site - 2:site], "little")
            target = owner_of(pairs, starts, destination)
            if target:
                new_destination = new_frame * 16 + int.from_bytes(new_image[new_site - 2:new_site], "little")
                if new_destination != target[1].start + destination - target[0].start:
                    raise ValueError(f"far data pointer at {site - 2:#x} ({old.module}) lost its target")
                far_pointers += 1
    actual = [entry.linear for entry in shifted.relocations]
    if sorted(expected) != sorted(actual):
        raise ValueError("MZ relocations no longer cover the same bytes within their owners")
    if unmapped:
        raise ValueError("MZ relocation frames lack MAP ownership: " +
                         ", ".join(f"{a:04X}->{b:04X}" for a, b in sorted(unmapped)))
    tables, entries, extents = switch_tables(old_image, new_image, pairs)
    direct = direct_offsets(old_image, new_image, pairs, starts, publics)
    inside = [c for c in direct["candidates"] if any(
        lo - 6 <= int(c["address"][:4], 16) * 16 + int(c["address"][5:], 16) < hi for lo, hi in extents)]
    direct["candidates"] = [c for c in direct["candidates"] if c not in inside]
    direct["inside_switch_tables"] = len(inside)
    layout = {"moved_contributions_by_class": dict(moved), "checked_contributions": len(pairs),
              "relocations": len(actual), "ordered_owner_sites_identical": expected == actual,
              "relocated_far_transfers": far_transfers, "relocated_far_data_pointers": far_pointers,
              "switch_tables": tables, "switch_table_entries": entries,
              "direct_offsets_screened": direct["screened"], "direct_offsets_moved": direct["moved"],
              "direct_offsets_for_review": len(direct["candidates"])}
    return layout, direct


def relink(artifact: str, product: dict, output: Path, padding: dict[str, int]) -> tuple[dict, dict]:
    baseline_exe = (ROOT / product["build"]).resolve()
    source = baseline_exe.parents[2]
    if not source.is_relative_to(PRIVATE) or sha(baseline_exe.read_bytes()) != product["sha256"]:
        raise ValueError("baseline product identity drift")
    work = output / artifact / "source"
    shutil.copytree(source, work, symlinks=True)
    response = f"bin/th05/{artifact}.rsp"
    exe, map_path = work / f"bin/th05/{artifact}.exe", work / f"obj/th05/{artifact}.map"
    baseline_map = map_path.read_bytes()
    exe.unlink()
    map_path.unlink()
    tlink(work, response, "control-link.log")
    if exe.read_bytes() != baseline_exe.read_bytes() or map_path.read_bytes() != baseline_map:
        raise ValueError("unshifted relink does not reproduce the product EXE and MAP")
    old_rows = map_rows(map_path)
    publics = sorted({address for address, _ in map_publics(map_path)})
    args, files_text = read_response(work / response)
    if args[:4] != ["-c", "-s", "-E", "c0l.obj"]:
        raise ValueError("unexpected TLINK response")
    modules = [omf_module((PREFIX / "drive_c/TC4/LIB/C0L.OBJ").read_bytes())]
    for name in args[4:]:
        modules.append(omf_module((work / name.replace("\\", "/")).read_bytes()))
    pads = pad_objects(old_rows, modules, work, padding)
    shifted = list(args[:3])
    for index, name in enumerate(args[3:]):
        shifted.append(name)
        if index in pads:
            shifted.append(pads[index])
    write_response(work / response, shifted, files_text)
    tlink(work, response, "shifted-link.log")
    data = exe.read_bytes()
    synthetic = {name[:-4].lower() + ".asm" for name in pads.values()}
    layout, direct = compare_layout(parse_mz(baseline_exe.read_bytes()), parse_mz(data),
                                    old_rows, map_rows(map_path), synthetic, publics)
    report = json.dumps(direct, indent=2).encode() + b"\n"
    (output / artifact / "direct-offset-review.json").write_bytes(report)
    receipt = {"artifact": f"th05-{artifact}", "scope": "DOS product position independence layout perturbation",
               "baseline_sha256": product["sha256"], "shifted_sha256": sha(data), "padding_bytes": padding,
               "padding_objects": len(pads), "unshifted_control_byte_identical": True,
               "direct_offset_review_sha256": sha(report), **layout}
    (output / artifact / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    shutil.copyfile(exe, output / EXES[artifact])
    return {"file": EXES[artifact], "bytes": len(data), "sha256": sha(data),
            "build": str((exe).relative_to(ROOT)), "original_equal": False}, layout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=ROOT / ".analysis/build/th05")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", nargs="+", choices=EXES, default=list(EXES))
    parser.add_argument("--padding", type=int, nargs=3, default=(16, 32, 48),
                        metavar=("CODE", "DATA", "BSS"), help="bytes inserted per eligible segment")
    args = parser.parse_args()
    if any(size <= 0 for size in args.padding):
        parser.error("padding sizes must be positive")
    padding = dict(zip(("CODE", "DATA", "BSS"), args.padding))
    baseline, output = args.baseline.resolve(), args.output.resolve()
    if not output.is_relative_to(PRIVATE) or output.exists():
        parser.error("use a fresh output directory under .analysis/")
    manifest = json.loads((baseline / "build.json").read_text())
    products, layouts = {}, {}
    with (PRIVATE / "borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        output.mkdir(parents=True)
        for artifact in dict.fromkeys(args.only):
            products[artifact], layouts[artifact] = relink(artifact, manifest["products"][artifact],
                                                           output, padding)
    for artifact, row in manifest["products"].items():
        if artifact not in products:  # ZUN.COM and unselected products are reused unchanged
            shutil.copyfile(baseline / row["file"], output / row["file"])
            products[artifact] = row
    (output / "build.json").write_text(json.dumps(
        {"schema_version": 1, "built": "pi-relink", "padding": padding, "products": products}, indent=2) + "\n")
    print(json.dumps(layouts, indent=2))


if __name__ == "__main__":
    main()

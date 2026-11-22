#!/usr/bin/env python3
"""Check that accepted units reference memory only through fixups.

For every accepted C/C++ unit and reviewed-ASM family, this reads the compiled
OMF object that the retained producer linked, rebuilds its segment bytes and
the byte positions covered by FIXUPP records, and decodes the unit's own
extent. A 16-bit direct memory displacement (no base or index register) whose
bytes are not covered by a fixup is a literal address: the unit would keep
reading the same offset after its data moved. Those instructions are listed
for review; hardware and DOS addresses are expected among them. A 16-bit
immediate without a fixup whose value equals the offset of a DGROUP public in
the producer MAP (the binders place every foreign symbol at its original
address) is listed as a register-carried candidate.

This complements `audit_dos_pi.py`, which relinks the DOS product but only sees
the maintained translation units overlaid into it. It needs the private
`.analysis/` replay outputs and runs no tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from lib.omf_edit import object_segments, segment_names
from lib.unit_oracle import map_publics

ROOT = Path(__file__).resolve().parents[1]
LEDGERS = {"main": "config/accepted_units.json", "op": "config/accepted_units.op.json",
           "maine": "config/accepted_units.maine.json", "zun": "config/accepted_units.zun.json"}
MAP_ROW = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)")


def map_rows(path: Path) -> list[tuple[int, int, str, str]]:
    rows = []
    for line in path.read_text(encoding="cp437").splitlines():
        match = MAP_ROW.match(line)
        if match and int(match[3], 16):
            start = int(match[1], 16) * 16 + int(match[2], 16)
            if match[4] == "CODE":
                rows.append((start, int(match[3], 16), match[5], match[7]))
    return rows


def objects_by_module(source: Path) -> dict[str, bytes]:
    found = {}
    for path in source.glob("*.obj"):
        raw = path.read_bytes()
        found[raw[4:4 + raw[3]].decode("cp437").lower()] = raw
    return found


def dgroup_publics(path: Path) -> set[int]:
    text = path.read_text(encoding="cp437")
    frames = [int(m[1], 16) for m in re.finditer(
        r"^\s*([0-9A-F]{4}):[0-9A-F]{4}\s+[0-9A-F]{4}\s+C=(?:DATA|BSS)\s+S=\S+\s+G=DGROUP", text, re.M)]
    if not frames:
        return set()
    base = min(frames) * 16
    return {a - base for a, _ in map_publics(path) if base <= a < base + 0x10000 and a - base >= 0x40}


def literal_displacements(source: Path, start: int, size: int, decoder) -> tuple[int, list[dict]]:
    from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
    rows = map_rows(source / ("units.map"))
    symbols = dgroup_publics(source / "units.map")
    objects = objects_by_module(source)
    screened, literals = 0, []
    pieces = [r for r in rows if r[0] < start + size and start < r[0] + r[1]]
    for row_start, row_size, segment, module in pieces:
        if module.lower() in ("bindings.asm", "c0t.asm", "c0.asm"):
            continue  # foreign context: binders reserve space but supply no unit bytes
        raw = objects.get(module.lower())
        if raw is None:
            raise ValueError(f"no object for MAP module {module}")
        names = segment_names(raw)
        segs = object_segments(raw)
        indices = [i + 1 for i, name in enumerate(names) if name == segment and i + 1 in segs]
        if len(indices) != 1:
            raise ValueError(f"{module}: segment {segment} not unique in the object")
        image, covered = segs[indices[0]]
        lo, hi = max(start, row_start) - row_start, min(start + size, row_start + row_size) - row_start
        for ins in decoder.disasm(bytes(image[lo:hi]), lo):
            immediate = [op.imm & 0xFFFF for op in ins.operands if op.type == X86_OP_IMM]
            if ins.imm_size == 2 and immediate and immediate[0] in symbols and not set(
                    range(ins.address + ins.imm_offset, ins.address + ins.imm_offset + 2)) & covered:
                literals.append({"module": module, "offset": f"{segment}:{ins.address:04X}",
                                 "instruction": f"{ins.mnemonic} {ins.op_str}", "kind": "immediate"})
            if not ins.id or ins.disp_size != 2:
                continue
            for op in ins.operands:
                if op.type == X86_OP_MEM and not op.mem.base and not op.mem.index:
                    screened += 1
                    field = range(ins.address + ins.disp_offset, ins.address + ins.disp_offset + 2)
                    if not set(field) & covered:
                        literals.append({"module": module, "offset": f"{segment}:{ins.address:04X}",
                                         "instruction": f"{ins.mnemonic} {ins.op_str}",
                                         "kind": "displacement"})
    return screened, literals


def receipt_index() -> dict[str, Path]:
    found = {}
    for path in (ROOT / ".analysis").rglob("receipt.json"):
        found.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), path)
    return found


def main() -> int:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the full review list as JSON")
    args = parser.parse_args()
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    receipts = receipt_index()
    report, screened, units, skipped = [], 0, 0, []
    jobs = []
    for artifact, ledger_path in LEDGERS.items():
        for unit in json.loads((ROOT / ledger_path).read_text())["units"]:
            result = unit["result"]
            rnd = result["rounds"][0]
            if rnd["target_fixups"] is None:
                continue
            jobs.append((artifact, unit["id"], unit["replay_receipt_sha256"], result["producer_paths"][0],
                         rnd["candidate_start"], rnd["size"]))
    for uid, unit in json.loads((ROOT / "config/accepted_asm_families.json").read_text())["units"].items():
        comparison = unit["rounds"][0]["comparison"]
        jobs.append((unit["entry"]["artifact"], uid, unit["replay_receipt_sha256"], "a/source",
                     comparison["candidate_start"], comparison["size"]))
    for artifact, uid, digest, producer, start, size in jobs:
        receipt = receipts.get(digest)
        source = receipt.parent / producer if receipt else None
        if source is None or not (source / "units.map").exists():
            skipped.append(uid)
            continue
        if not (source / "units.exe").exists():
            start -= 0x100 if artifact == "zun" else 0  # COM images load at 100h
        count, literals = literal_displacements(source, start, size, decoder)
        screened += count
        units += 1
        for row in literals:
            report.append({"artifact": artifact, "unit": uid, **row})
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    for row in report:
        print(f"{row['artifact']:5} {row['unit']:48} {row['offset']:22} {row['instruction']}")
    print(f"{units} units, {screened} direct displacements, {len(report)} without a fixup; "
          f"skipped {len(skipped)}: {' '.join(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

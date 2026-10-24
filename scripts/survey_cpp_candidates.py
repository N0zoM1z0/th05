#!/usr/bin/env python3
"""Route reference C++ contributions by instruction shape; never grant credit.

All displacement/immediate fields are masked only for candidate discovery.
Every result is an inference requiring original boundary/operand review and
an independent cold raw-byte oracle before source acceptance.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

from lib.pc98 import digest_file, parse_mz
from lib.unit_context import UnitContext, load_unit_target

ROOT = Path(__file__).resolve().parents[1]


def shape(data: bytes, origin: int) -> tuple[bytes, int] | None:
    import capstone
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    decoder.detail = True
    mask = bytearray(len(data))
    decoded = 0
    for instruction in decoder.disasm(data, origin):
        offset = instruction.address - origin
        if offset != decoded:
            return None
        for start, size in ((instruction.disp_offset, instruction.disp_size),
                            (instruction.imm_offset, instruction.imm_size)):
            if start and size:
                mask[offset + start:offset + start + size] = bytes([1]) * size
        # Capstone exposes only the last encoded immediate of a far transfer.
        if instruction.bytes[0] in (0x9a, 0xea):
            mask[offset + 1:offset + instruction.size] = bytes([1]) * (instruction.size - 1)
        decoded += instruction.size
    if decoded != len(data):
        return None
    fixed = mask.count(0)
    if fixed < 8 or fixed * 5 < len(data):
        return None
    pattern = bytearray()
    index = 0
    while index < len(data):
        end = index + 1
        while end < len(data) and mask[end] == mask[index]:
            end += 1
        pattern.extend((b".{" + str(end - index).encode() + b"}") if mask[index]
                       else re.escape(data[index:end]))
        index = end
    return bytes(pattern), fixed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path, help="completed reference calibration directory")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--artifact", choices=("main", "op", "maine"), default="main")
    args = parser.parse_args()
    build = args.build.resolve()
    receipt = json.loads((build / "receipt.json").read_text())
    candidate_path = build / receipt["output"]
    if digest_file(candidate_path) != receipt["sha256"] or receipt["artifact"] != args.artifact:
        parser.error("candidate changed since the calibration build")
    context = UnitContext(ROOT, args.artifact)
    artifact, image, target_view = load_unit_target(context, context.config())
    target = image.program_image
    candidate = parse_mz(candidate_path.read_bytes()).program_image
    mapping = build / f"source/obj/th05/{args.artifact}.map"
    rows = []
    for line in mapping.read_text(encoding="cp437").splitlines():
        match = re.match(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=(\S+)\s+G=\S+\s+M=(\S+\.cpp)\s", line, re.I)
        if not match:
            continue
        start, size = int(match[1], 16) * 16 + int(match[2], 16), int(match[3], 16)
        if not size:
            continue
        discovered = shape(candidate[start:start + size], start)
        item = {"module": match[5], "segment": match[4], "candidate_start": start, "size": size,
                "status": "diagnostic-only-no-authored-credit"}
        if discovered is None:
            item["reason"] = "incomplete decode or insufficient fixed bytes"
        else:
            pattern, fixed = discovered
            positions = [m.start() for m in re.finditer(pattern, target, re.DOTALL)]
            item.update({"fixed_bytes": fixed, "match_count": len(positions), "target_candidates": positions[:8]})
        rows.append(item)
    result = {"kind": "masked-discovery-only", "target_sha256": artifact["sha256"],
              "candidate_sha256": receipt["sha256"], "map_sha256": digest_file(mapping), "contributions": rows,
              "limitations": ["All addresses/constants are masked for routing only.",
                              "Unique shape matching is neither source authorship nor exactness.",
                              "Boundary, operand, ABI and cold raw comparison remain mandatory."]}
    if target_view is not None:
        result["target_view"] = target_view
    default_name = "cpp-candidate-survey.json" if args.artifact == "main" else f"cpp-candidate-survey-{args.artifact}.json"
    output = (args.output or ROOT / ".analysis" / default_name).resolve()
    if not output.is_relative_to((ROOT / ".analysis").resolve()):
        parser.error("diagnostic evidence must remain in .analysis")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    unique = [r for r in rows if r.get("match_count") == 1]
    print(f"Diagnostic only: {len(rows)} C++ contributions, {len(unique)} unique shape candidates, "
          f"{sum(r['size'] for r in unique):,} candidate bytes; zero authored credit")
    for row in sorted(unique, key=lambda r: r["size"], reverse=True)[:12]:
        print(f"{row['module']:<25} {row['segment']:<20} load+{row['target_candidates'][0]:05x} {row['size']:5} bytes")
    print(f"Private discovery evidence: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

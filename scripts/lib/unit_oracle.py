"""Compare complete reviewed unit bytes and ordered relative MZ fixup sites."""
from __future__ import annotations
from pathlib import Path
import re

from .pc98 import MZImage, digest_bytes


def map_contribution(path: Path, module: str, segment: str) -> tuple[int, int]:
    found = []
    for line in path.read_text(encoding="cp437").splitlines():
        match = re.match(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=(\S+)\s+G=\S+\s+M=(\S+)", line, re.I)
        if match and match[4].lower() == segment.lower() and match[5].lower() == module.lower():
            start, size = int(match[1], 16) * 16 + int(match[2], 16), int(match[3], 16)
            if size:
                found.append((start, size))
    if len(found) != 1:
        raise ValueError(f"expected one complete CODE contribution for {module}/{segment}: {found}")
    return found[0]


def relative_fixups(image: MZImage, start: int, size: int) -> list[int]:
    result = []
    for fixup in image.relocations:
        if fixup.linear < start + size and fixup.linear + 2 > start:
            if fixup.linear < start or fixup.linear + 2 > start + size:
                raise ValueError("unit boundary splits a relocation word")
            result.append(fixup.linear - start)
    if len(result) != len(set(result)):
        raise ValueError("duplicate relocation sites in unit")
    return result


def compare_unit(target: MZImage, candidate: MZImage, target_start: int,
                 candidate_start: int, size: int) -> dict:
    if not target.valid or not candidate.valid:
        raise ValueError("invalid MZ input")
    if size <= 0 or min(target_start, candidate_start) < 0:
        raise ValueError("invalid extent")
    left = target.program_image[target_start:target_start + size]
    right = candidate.program_image[candidate_start:candidate_start + size]
    if len(left) != size or len(right) != size:
        raise ValueError("truncated unit extent")
    left_fixups = relative_fixups(target, target_start, size)
    right_fixups = relative_fixups(candidate, candidate_start, size)
    return {"target_start": target_start, "candidate_start": candidate_start, "size": size,
            "target_sha256": digest_bytes(left), "candidate_sha256": digest_bytes(right),
            "raw_exact": left == right, "target_fixups": left_fixups,
            "candidate_fixups": right_fixups, "fixups_exact": left_fixups == right_fixups,
            "exact": left == right and left_fixups == right_fixups}

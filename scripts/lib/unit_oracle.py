"""Compare complete reviewed unit bytes and ordered relative MZ fixup sites."""
from __future__ import annotations
from pathlib import Path
import re

from .pc98 import MZImage, digest_bytes
from .unit_extents import data_map_scope, unit_extent_kind


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


def function_scoped(entry: dict) -> bool:
    """Function scopes are opt-in; the historical whole-contribution default stays."""
    if unit_extent_kind(entry) == 'initialized-data':
        return False
    if "function_end_symbol" in entry and "function_symbol" not in entry:
        raise ValueError("function_end_symbol requires function_symbol")
    for key in ("function_symbol", "function_end_symbol"):
        if key in entry and (not isinstance(entry[key], str) or not entry[key].strip()):
            raise ValueError(f"{key} must be a nonempty MAP symbol")
    if "function_symbol" in entry and (type(entry.get("functions")) is not int or entry["functions"] != 1):
        raise ValueError("a complete function unit must declare exactly one function")
    return "function_symbol" in entry


def map_publics(path: Path) -> list[tuple[int, str]]:
    """Read only TLINK's value table, including idle functions, excluding Abs.

    TLINK repeats publics in its name table. Counting both tables can conceal
    duplicate symbols or manufacture ambiguous function boundaries.
    """
    rows = []
    active = False
    headers = 0
    for line in path.read_text(encoding="cp437").splitlines():
        if "Publics by Value" in line:
            active = True
            headers += 1
            continue
        if active and ("Program entry point" in line or "Publics by Name" in line):
            active = False
        if not active:
            continue
        match = re.fullmatch(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:(idle|Abs)\s+)?(.+?)\s*", line, re.I)
        if match and (match[3] or "").lower() != "abs":
            rows.append((int(match[1], 16) * 16 + int(match[2], 16), match[4]))
    if headers != 1 or not rows:
        raise ValueError("expected one nonempty TLINK Publics by Value table")
    if len(rows) != len(set(rows)):
        raise ValueError("duplicate MAP public symbol rows")
    return rows


def map_unit_scope(path: Path, entry: dict) -> dict:
    """Locate a whole contribution or one reviewed complete public function.

    Function scopes require demangled function publics (the normal TLINK MAP
    format). A data/ASM label is not evidence of a function boundary. The next
    distinct public inside the same contribution cannot be skipped, even if
    that function is unregistered, idle, or known to differ from the original.
    The final function ends at the complete real compiler contribution end.
    """
    if unit_extent_kind(entry) == 'initialized-data':
        return data_map_scope(path, entry)
    start, size = map_contribution(path, entry["module"], entry["segment"])
    if not function_scoped(entry):
        return {"kind": "complete-contribution", "start": start, "size": size}
    symbol = entry["function_symbol"]
    if not re.fullmatch(r".+\(.*\)", symbol):
        raise ValueError("function scope requires a demangled MAP function public")
    publics = map_publics(path)
    found = [address for address, name in publics if name == symbol]
    if len(found) != 1 or not start <= found[0] < start + size:
        raise ValueError("function symbol is missing, ambiguous or outside its CODE contribution")
    function_start = found[0]
    if len([name for address, name in publics if address == function_start]) != 1:
        raise ValueError("aliased MAP publics do not prove one complete function")
    following = [(address, name) for address, name in publics if function_start < address < start + size]
    end = min((address for address, _ in following), default=start + size)
    next_names = [name for address, name in following if address == end]
    if next_names and (len(next_names) != 1 or not re.fullmatch(r".+\(.*\)", next_names[0])):
        raise ValueError("next MAP public does not prove an unambiguous function boundary")
    configured_end = entry.get("function_end_symbol")
    if configured_end is not None and next_names != [configured_end]:
        raise ValueError("function_end_symbol must be the actual next function inside the contribution")
    return {"kind": "complete-function", "start": function_start, "size": end - function_start,
            "function_symbol": symbol, "contribution_start": start, "contribution_size": size,
            "boundary_kind": "next-function" if next_names else "contribution-end",
            "next_function_symbol": next_names[0] if next_names else None}


def map_unit(path: Path, entry: dict) -> tuple[int, int]:
    scope = map_unit_scope(path, entry)
    return scope["start"], scope["size"]


def compare_mapped_unit(target: MZImage, candidate: MZImage, path: Path, entry: dict) -> dict:
    scope = map_unit_scope(path, entry)
    if scope["size"] != entry["size"]:
        raise ValueError(f"{entry['id']}: {scope['kind']} size mismatch: {scope['size']}")
    comparison = compare_unit(target, candidate, entry["target_start"], scope["start"], scope["size"])
    if function_scoped(entry) or unit_extent_kind(entry) == 'initialized-data':
        comparison["map_scope"] = scope
    return comparison


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

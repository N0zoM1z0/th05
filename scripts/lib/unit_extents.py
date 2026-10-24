"""Opt-in initialized semantic DATA; historical units remain CODE by default.

These checks prove extent/producer structure, not semantic ownership by
themselves. The maintained initializer source and declared roles need review.
Assets and compiler-generated CODE tables are outside this DATA lane.
"""

from __future__ import annotations

from pathlib import Path
import re

from .omf import parse_omf
from .pc98 import digest_bytes


DATA_SEMANTICS = frozenset(
    {
        "state",
        "filenames",
        "ui-text",
        "function-pointers",
        "string-pointers",
        "semantic-tables",
    }
)


def unit_extent_kind(entry: dict) -> str:
    kind = entry.get("extent_kind", "code")
    if kind not in ("code", "initialized-data"):
        raise ValueError("only CODE or initialized semantic DATA extents are supported")
    if kind == "code":
        return kind
    if type(entry.get("size")) is not int or entry["size"] <= 0:
        raise ValueError("initialized DATA requires a positive complete extent size")
    if type(entry.get("functions")) is not int or entry["functions"] != 0:
        raise ValueError("initialized DATA must declare zero functions")
    if "function_symbol" in entry or "function_end_symbol" in entry:
        raise ValueError(
            "initialized DATA requires a whole contribution, never function scopes"
        )
    if any(
        not isinstance(entry.get(key, []), list) or entry.get(key, [])
        for key in ("alignment_offsets", "code_data_ranges")
    ):
        raise ValueError(
            "CODE alignment and switch tables cannot be reclassified as DATA"
        )
    roles = entry.get("data_semantics")
    if (
        not isinstance(roles, list)
        or not roles
        or any(
            not isinstance(role, str) or role not in DATA_SEMANTICS for role in roles
        )
        or len(set(roles)) != len(roles)
    ):
        raise ValueError(
            "DATA requires explicit reviewed semantic initializer roles; assets are unsupported"
        )
    if entry.get("origin") not in (
        "compiler-generated-cxx",
        "compiler-generated-cxx-semantic-data",
        "compiler-generated-cxx-dos-intrinsics",
        "compiler-generated-cxx-hardware-register-intrinsics",
    ):
        raise ValueError(
            "DATA must come from a maintained natural C++ initializer producer"
        )
    return kind


def classify_data_extent(entry: dict, *, target_bytes: bytes | None = None) -> dict:
    if unit_extent_kind(entry) != "initialized-data":
        raise ValueError("not an initialized DATA extent")
    size = entry.get("size")
    if type(size) is not int or size <= 0:
        raise ValueError("invalid complete initialized DATA size")
    values = entry.get("padding_bytes", [])
    if not isinstance(values, list):
        raise ValueError("DATA padding must be an explicit list")
    padding = {}
    for item in values:
        if not isinstance(item, dict) or set(item) != {"offset", "value"}:
            raise ValueError("DATA padding requires explicit offset/value")
        offset, value = item["offset"], item["value"]
        if (
            type(offset) is not int
            or not 0 <= offset < size
            or offset in padding
            or type(value) is not int
            or not 0 <= value <= 255
        ):
            raise ValueError("invalid or duplicate DATA padding")
        padding[offset] = value
    if len(padding) == size:
        raise ValueError("initialized DATA must retain semantic initializer bytes")
    if target_bytes is not None:
        if len(target_bytes) != size:
            raise ValueError("DATA verification requires the complete target extent")
        if any(target_bytes[offset] != value for offset, value in padding.items()):
            raise ValueError("DATA padding disagrees with the original target")
    authored = size - len(padding)
    return {
        "authored_code_bytes": 0,
        "code_data_bytes": 0,
        "instruction_bytes": 0,
        "padding_bytes": len(padding),
        "authored_data_bytes": authored,
        "authored_bytes": authored,
    }


def data_map_scope(path: Path, entry: dict) -> dict:
    if unit_extent_kind(entry) != "initialized-data":
        raise ValueError("DATA MAP lookup needs initialized-data opt-in")
    found = []
    pattern = re.compile(
        r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
        r"C=(\S+)\s+S=(\S+)\s+G=\S+\s+M=(\S+)",
        re.I,
    )
    for line in path.read_text(encoding="cp437").splitlines():
        match = pattern.match(line)
        if (
            match
            and match[5].casefold() == entry["segment"].casefold()
            and match[6].casefold() == entry["module"].casefold()
        ):
            size = int(match[3], 16)
            if size:
                found.append(
                    (match[4].upper(), int(match[1], 16) * 16 + int(match[2], 16), size)
                )
    if len(found) != 1 or found[0][0] != "DATA":
        raise ValueError(
            "expected one complete initialized C=DATA contribution; BSS/CODE are unsupported"
        )
    _, start, size = found[0]
    return {
        "kind": "complete-initialized-data-contribution",
        "map_class": "DATA",
        "start": start,
        "size": size,
        "module": entry["module"],
        "segment": entry["segment"],
    }


def validate_data_scope_evidence(
    entry: dict, comparison: dict, omf_scope: dict
) -> None:
    """Public receipt structure; accept must independently recompute both scopes."""
    if unit_extent_kind(entry) != "initialized-data":
        raise ValueError("not an initialized DATA evidence record")
    scope = comparison.get("map_scope", {})
    size = comparison.get("candidate_size", comparison["size"])
    if (
        type(size) is not int
        or size <= 0
        or type(comparison.get("candidate_start")) is not int
        or comparison["candidate_start"] < 0
        or not isinstance(scope, dict)
        or type(scope.get("start")) is not int
        or type(scope.get("size")) is not int
        or scope
        != {
            "kind": "complete-initialized-data-contribution",
            "map_class": "DATA",
            "start": comparison["candidate_start"],
            "size": size,
            "module": entry["module"],
            "segment": entry["segment"],
        }
    ):
        raise ValueError("complete DATA MAP evidence disagrees with actual extent")
    if (
        not isinstance(omf_scope, dict)
        or set(omf_scope)
        != {"kind", "segment", "class", "size", "segment_index", "ledata"}
        or omf_scope.get("kind") != "complete-compiler-initialized-data"
        or omf_scope.get("class") != "DATA"
        or not isinstance(omf_scope.get("segment"), str)
        or omf_scope.get("segment", "").casefold() != entry["segment"].casefold()
        or type(omf_scope.get("size")) is not int
        or omf_scope.get("size") != size
        or type(omf_scope.get("segment_index")) is not int
        or omf_scope["segment_index"] <= 0
        or not isinstance(omf_scope.get("ledata"), list)
    ):
        raise ValueError("complete initialized compiler DATA evidence disagrees")
    covered = set()
    for block in omf_scope["ledata"]:
        if not isinstance(block, dict) or set(block) != {"offset", "size", "sha256"}:
            raise ValueError("DATA LEDATA evidence fields disagree")
        start, length = block["offset"], block["size"]
        if (
            type(start) is not int
            or type(length) is not int
            or start < 0
            or length <= 0
            or start + length > size
            or covered.intersection(range(start, start + length))
            or not isinstance(block["sha256"], str)
            or not re.fullmatch("[0-9a-f]{64}", block["sha256"])
        ):
            raise ValueError("DATA LEDATA evidence bounds/hash disagree")
        covered.update(range(start, start + length))
    if len(covered) != size:
        raise ValueError("DATA LEDATA evidence is incomplete")


def _index(data: bytes, cursor: int) -> tuple[int, int]:
    if cursor >= len(data):
        raise ValueError("truncated initialized DATA OMF index")
    result = data[cursor]
    cursor += 1
    if result & 128:
        if cursor >= len(data):
            raise ValueError("truncated initialized DATA OMF long index")
        result = ((result & 127) << 8) | data[cursor]
        cursor += 1
    return result, cursor


def initialized_data_omf_scope(raw: bytes, entry: dict, *, require_size: bool = True) -> dict:
    """Prove all bytes come from one real compiler DATA SEGDEF's LEDATA.

    LIDATA/COMDAT/patch transforms are deliberately unsupported in this first
    lane. OMF FIXUPP bytes stay unchanged and the actual linked MZ must still
    pass its independent complete raw/ordered-fixup comparison.
    """
    if unit_extent_kind(entry) != "initialized-data":
        raise ValueError("DATA OMF lookup needs initialized-data opt-in")
    records = parse_omf(raw)
    names, segments = [""], [None]
    for record in records:
        data = record.data
        if record.name == "LNAMES":
            cursor = 0
            while cursor < len(data):
                length = data[cursor]
                cursor += 1
                if cursor + length > len(data):
                    raise ValueError("truncated DATA LNAMES")
                names.append(data[cursor : cursor + length].decode("cp437"))
                cursor += length
        elif record.name == "SEGDEF":
            if len(data) < 6 or not data[0] & 0xE0 or data[0] & 2:
                raise ValueError("unsupported DATA SEGDEF attributes")
            name, cursor = _index(data, 3)
            cl, cursor = _index(data, cursor)
            overlay, cursor = _index(data, cursor)
            if (
                cursor != len(data)
                or not 0 < name < len(names)
                or not 0 < cl < len(names)
                or not 0 <= overlay < len(names)
            ):
                raise ValueError("invalid DATA SEGDEF names")
            segments.append(
                {
                    "name": names[name],
                    "class": names[cl],
                    "size": int.from_bytes(data[1:3], "little"),
                }
            )
    matches = [
        (index, seg)
        for index, seg in enumerate(segments)
        if seg and seg["name"].casefold() == entry["segment"].casefold()
    ]
    if len(matches) != 1 or matches[0][1]["class"].upper() != "DATA":
        raise ValueError("expected one real compiler initialized DATA SEGDEF")
    index, segment = matches[0]
    if require_size and segment["size"] != entry["size"]:
        raise ValueError("complete compiler DATA SEGDEF size disagrees")
    covered = bytearray(segment["size"])
    chunks = []
    for record in records:
        if record.name in (
            "COMDAT",
            "COMDAT32",
            "BAKPAT",
            "BAKPAT32",
            "LIDATA",
            "LIDATA32",
            "LEDATA32",
            "FIXUPP32",
            "SEGDEF32",
        ):
            raise ValueError("unsupported initialized DATA producer transformation")
        if record.name != "LEDATA":
            continue
        si, cursor = _index(record.data, 0)
        if si != index:
            continue
        if cursor + 2 > len(record.data):
            raise ValueError("truncated initialized DATA LEDATA")
        start = int.from_bytes(record.data[cursor : cursor + 2], "little")
        payload = record.data[cursor + 2 :]
        end = start + len(payload)
        if not payload or end > len(covered) or any(covered[start:end]):
            raise ValueError("initialized DATA LEDATA overlaps or escapes SEGDEF")
        covered[start:end] = b"\1" * len(payload)
        chunks.append(
            {"offset": start, "size": len(payload), "sha256": digest_bytes(payload)}
        )
    if not covered or not all(covered):
        raise ValueError("initialized DATA SEGDEF contains unwritten bytes")
    return {
        "kind": "complete-compiler-initialized-data",
        "segment": segment["name"],
        "class": "DATA",
        "size": segment["size"],
        "segment_index": index,
        "ledata": chunks,
    }

"""Read OMF segments and fixup coverage; add public aliases and rename externs.

Edits only touch PUBDEF/EXTDEF records. Code, data and fixups stay unchanged.
"""
from __future__ import annotations

from .omf import parse_omf

FIXUP_WIDTH = {0: 1, 1: 2, 2: 2, 3: 4, 4: 1, 5: 2, 9: 2, 13: 2}


def index(data: bytes, at: int) -> tuple[int, int]:
    if data[at] & 0x80:
        return ((data[at] & 0x7F) << 8) | data[at + 1], at + 2
    return data[at], at + 1


def _encode_index(value: int) -> bytes:
    return bytes([value]) if value < 0x80 else bytes([0x80 | (value >> 8), value & 0xFF])


def object_segments(raw: bytes) -> dict[int, tuple[bytearray, set[int]]]:
    """Segment index -> (LEDATA image, fixup-covered offsets)."""
    images: dict[int, bytearray] = {}
    covered: dict[int, set[int]] = {}
    last = None
    for record in parse_omf(raw):
        data = record.data
        if record.record_type in (0xA0, 0xA1):
            segment, at = index(data, 0)
            width = 4 if record.record_type == 0xA1 else 2
            offset = int.from_bytes(data[at:at + width], "little")
            payload = data[at + width:]
            image = images.setdefault(segment, bytearray())
            if len(image) < offset + len(payload):
                image.extend(b"\0" * (offset + len(payload) - len(image)))
            image[offset:offset + len(payload)] = payload
            covered.setdefault(segment, set())
            last = (segment, offset)
        elif record.record_type in (0xA2, 0xA3):
            last = None
        elif record.record_type in (0x9C, 0x9D):
            at = 0
            while at < len(data):
                head = data[at]
                if not head & 0x80:  # THREAD subrecord
                    method = (head >> 2) & 7
                    at += 1
                    if method < 3:
                        _, at = index(data, at)
                    continue
                locat = (head << 8) | data[at + 1]
                kind, where, fixdat = (locat >> 10) & 0xF, locat & 0x3FF, data[at + 2]
                at += 3
                if not fixdat & 0x80 and ((fixdat >> 4) & 7) < 3:
                    _, at = index(data, at)
                if not fixdat & 0x08:
                    _, at = index(data, at)
                if not fixdat & 0x04:
                    at += 4 if record.record_type == 0x9D else 2
                if last is None:
                    raise ValueError("FIXUPP without LEDATA")
                segment, base = last
                covered[segment].update(range(base + where, base + where + FIXUP_WIDTH.get(kind, 2)))
    return {k: (images[k], covered[k]) for k in images}


def lnames_segments(raw: bytes) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, list[int]]]]:
    """(LNAMES, SEGDEF (name, class), GRPDEF (name, segment indices))."""
    names, segments, groups = [], [], []
    for record in parse_omf(raw):
        data = record.data
        if record.record_type in (0x96, 0xCA):
            at = 0
            while at < len(data):
                names.append(data[at + 1:at + 1 + data[at]].decode("cp437"))
                at += 1 + data[at]
        elif record.record_type in (0x98, 0x99):
            at = 1 + (3 if (data[0] >> 5) == 0 else 0) + (4 if record.record_type == 0x99 else 2)
            name, at = index(data, at)
            klass, at = index(data, at)
            segments.append((names[name - 1], names[klass - 1]))
        elif record.record_type == 0x9A:
            name, at = index(data, 0)
            members = []
            while at < len(data):
                if data[at] != 0xFF:
                    break
                segment, at = index(data, at + 1)
                members.append(segment)
            groups.append((names[name - 1], members))
    return names, segments, groups


def segment_names(raw: bytes) -> list[str]:
    return [name for name, _ in lnames_segments(raw)[1]]


def publics(raw: bytes) -> dict[str, tuple[int, int, int]]:
    """Public name -> (group index, segment index, offset)."""
    found = {}
    for record in parse_omf(raw):
        if record.record_type != 0x90:
            continue
        data = record.data
        group, at = index(data, 0)
        segment, at = index(data, at)
        if segment == 0:
            at += 2
        while at < len(data):
            name = data[at + 1:at + 1 + data[at]].decode("cp437")
            at += 1 + data[at]
            offset = int.from_bytes(data[at:at + 2], "little")
            _, at = index(data, at + 2)
            found[name] = (group, segment, offset)
    return found


def externs(raw: bytes) -> list[str]:
    found = []
    for record in parse_omf(raw):
        if record.record_type == 0x8C:
            data, at = record.data, 0
            while at < len(data):
                found.append(data[at + 1:at + 1 + data[at]].decode("cp437"))
                at += 1 + data[at]
                _, at = index(data, at)
    return found


def _record(kind: int, body: bytes) -> bytes:
    head = bytes([kind]) + (len(body) + 1).to_bytes(2, "little") + body
    return head + bytes([(-sum(head)) & 0xFF])


def segment_group(raw: bytes, segment: int) -> int:
    for number, (_, members) in enumerate(lnames_segments(raw)[2], 1):
        if segment in members:
            return number
    return 0


def add_aliases_at(raw: bytes, aliases: dict[str, tuple[int, int]]) -> bytes:
    """aliases: name -> (segment index, offset). Existing publics are kept."""
    known = publics(raw)
    records = []
    for alias, (segment, offset) in sorted(aliases.items()):
        if alias in known:
            if known[alias][1:] != (segment, offset):
                raise ValueError(f"{alias} already public at a different place")
            continue
        name = alias.encode("cp437")
        body = (_encode_index(segment_group(raw, segment)) + _encode_index(segment) + bytes([len(name)]) +
                name + (offset & 0xFFFF).to_bytes(2, "little") + b"\0")
        records.append(_record(0x90, body))
    last = parse_omf(raw)[-1]
    if last.record_type not in (0x8A, 0x8B):
        raise ValueError("object does not end with MODEND")
    return raw[:last.offset] + b"".join(records) + raw[last.offset:]


def rename_externs(raw: bytes, renames: dict[str, str]) -> bytes:
    if not renames:
        return raw
    out = bytearray()
    for record in parse_omf(raw):
        chunk = raw[record.offset:record.offset + record.length + 3]
        if record.record_type == 0x8C:
            data, at, body = record.data, 0, b""
            while at < len(data):
                name = data[at + 1:at + 1 + data[at]].decode("cp437")
                at += 1 + data[at]
                start = at
                _, at = index(data, at)
                new = renames.get(name, name).encode("cp437")
                body += bytes([len(new)]) + new + data[start:at]
            chunk = _record(0x8C, body)
        out += chunk
    parse_omf(bytes(out))
    return bytes(out)


def fixups(raw: bytes) -> list[dict]:
    """Every FIXUP with its LEDATA segment/offset, location kind and resolved target."""
    out, last = [], None
    frame_threads, target_threads = {}, {}
    for record in parse_omf(raw):
        data = record.data
        if record.record_type in (0xA0, 0xA1):
            segment, at = index(data, 0)
            last = (segment, int.from_bytes(data[at:at + (4 if record.record_type == 0xA1 else 2)], "little"))
        elif record.record_type in (0xA2, 0xA3):
            last = None
        elif record.record_type in (0x9C, 0x9D):
            at = 0
            while at < len(data):
                head = data[at]
                if not head & 0x80:
                    method, number = (head >> 2) & 7, head & 3
                    at += 1
                    value = None
                    if method < 3:
                        value, at = index(data, at)
                    (frame_threads if head & 0x40 else target_threads)[number] = (method, value)
                    continue
                locat = (head << 8) | data[at + 1]
                fixdat = data[at + 2]
                at += 3
                if fixdat & 0x80:
                    frame = frame_threads.get((fixdat >> 4) & 3)
                else:
                    method = (fixdat >> 4) & 7
                    value = None
                    if method < 3:
                        value, at = index(data, at)
                    frame = (method, value)
                if fixdat & 0x08:
                    method, value = target_threads[fixdat & 3]
                    method = (method & 3) | (fixdat & 0x04)
                else:
                    method = fixdat & 7
                    value, at = index(data, at)
                displacement = 0
                if not method & 4:
                    width = 4 if record.record_type == 0x9D else 2
                    displacement = int.from_bytes(data[at:at + width], "little")
                    at += width
                segment, base = last
                out.append({"segment": segment, "offset": base + (locat & 0x3FF), "kind": (locat >> 10) & 0xF,
                            "self_relative": not (locat & 0x4000), "target_method": method & 3,
                            "target_index": value, "displacement": displacement, "frame": frame})
    return out

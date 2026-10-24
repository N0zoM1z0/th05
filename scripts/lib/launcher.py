"""Read the TH05 COMCSTM/COMSET launcher without executing embedded programs.

The result is a physical partition and source observation, never an authorship
or reconstruction verdict. Whole-file SHA-256 pins payload and code contents;
the container has no independently observed per-member checksum field.
"""

from __future__ import annotations

import hashlib
import struct


PSP_SIZE = 0x100
MAX_PROCS = 32
DIRECTORY_SIZE = 2 + MAX_PROCS * 8 + (MAX_PROCS + 1) * 2 + 3
COPY_HELPER = bytes.fromhex("f3a458b8000150c3")
COPYRIGHT = b"comcstm (c)O.Morikawa 1996"


class LauncherError(ValueError):
    """A launcher carrier or one of its bounded directory records is invalid."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LauncherError(message)


def parse_launcher(data: bytes, *, expected_sha256: str | None = None) -> dict:
    """Validate the outer header and inner directory, then partition every byte.

    Runtime offsets inside the inner COM use its own PSP bias. Returned
    ``file_start``/``file_end`` always refer to the original outer ZUN.COM.
    """
    require(13 <= len(data) <= 0xff00, "invalid outer COM size")
    actual_sha256 = digest(data)
    if expected_sha256 is not None:
        require(actual_sha256 == expected_sha256, "outer SHA-256 mismatch")
    require(data[0] == 0xe9, "outer entry is not a near jump")
    usage_address, usage_size, inner_size, timestamp = struct.unpack_from("<HHHI", data, 3)
    header_size = usage_address - PSP_SIZE
    require(header_size == 13 + len(COPYRIGHT), "unsupported COMCSTM header extent")
    require(data[13:header_size] == COPYRIGHT, "unsupported COMCSTM signature")
    inner_start = header_size + usage_size
    inner_end = inner_start + inner_size
    require(usage_size > 0 and 0 < inner_start < inner_end < len(data),
            "outer usage/inner extents exceed the carrier")
    entry = (3 + struct.unpack_from("<h", data, 1)[0]) & 0xffff
    require(entry == inner_end, "outer jump does not reach its trailing stub")
    # The observed TH05 wrapper implements Pipeline/cstmstub.asm in 68 bytes.
    # Its complete bytes are bound by the caller's pinned carrier digest.
    require(len(data) - inner_end == 68, "unsupported outer wrapper extent")
    inner = data[inner_start:inner_end]
    require(len(inner) >= 2 and inner[0] == 0xeb, "inner entry is not a short jump")
    inner_entry = 2 + struct.unpack_from("<b", inner, 1)[0]
    require(0 <= inner_entry <= len(inner) - 5, "inner entry exceeds its carrier")
    require(inner[inner_entry:inner_entry + 3] == b"\xfc\x8b\x0e",
            "inner entry lacks CLD and the directory-count load")
    count_address = struct.unpack_from("<H", inner, inner_entry + 3)[0]
    stub_size = count_address - PSP_SIZE
    require(inner_entry + 5 <= stub_size and
            stub_size + DIRECTORY_SIZE + len(COPY_HELPER) <= len(inner),
            "inner directory extent is invalid")
    count = struct.unpack_from("<H", inner, stub_size)[0]
    require(1 <= count <= MAX_PROCS, "invalid inner procedure count")
    names_start = stub_size + 2
    names_raw = inner[names_start:names_start + MAX_PROCS * 8]
    used_names = [names_raw[index * 8:(index + 1) * 8] for index in range(count)]
    require(all(name.strip() and all(32 <= value < 127 for value in name)
                for name in used_names), "invalid procedure name")
    require(len(set(used_names)) == count, "duplicate procedure name")
    require(names_raw[count * 8:] == b" " * ((MAX_PROCS - count) * 8),
            "nonspace unused name slots")
    entries_start = names_start + MAX_PROCS * 8
    entries = struct.unpack_from("<33H", inner, entries_start)
    payload_start = stub_size + DIRECTORY_SIZE
    helper_start = len(inner) - len(COPY_HELPER)
    used_entries = entries[:count + 1]
    require(used_entries[0] == payload_start + PSP_SIZE and
            used_entries[-1] == helper_start + PSP_SIZE and
            all(start < end for start, end in zip(used_entries, used_entries[1:])),
            "invalid or overlapping procedure partition")
    require(not any(entries[count + 1:]), "nonzero unused entry slots")
    call_start = entries_start + 66
    require(inner[call_start] == 0xe8, "inner transfer is not a near call")
    displacement = struct.unpack_from("<h", inner, call_start + 1)[0]
    require((call_start + 3 + displacement) & 0xffff == helper_start,
            "inner call does not reach its trailing copy helper")
    require(inner[helper_start:] == COPY_HELPER, "unexpected inner copy helper")

    partition: list[dict] = []

    def extent(name: str, kind: str, start: int, end: int) -> dict:
        require(0 <= start < end <= len(data), "invalid physical partition extent")
        row = {"name": name, "kind": kind, "file_start": start,
               "file_end": end, "size": end - start,
               "sha256": digest(data[start:end]), "origin": "unreviewed"}
        partition.append(row)
        return row

    extent("comcstm-header", "container-metadata", 0, header_size)
    extent("usage", "text-data", header_size, inner_start)
    extent("inner-dispatcher", "code-candidate", inner_start, inner_start + stub_size)
    extent("inner-directory", "container-metadata", inner_start + stub_size,
           inner_start + payload_start)
    payloads = []
    for index, raw_name in enumerate(used_names):
        start = inner_start + used_entries[index] - PSP_SIZE
        end = inner_start + used_entries[index + 1] - PSP_SIZE
        row = extent(raw_name.decode("ascii").rstrip(), "embedded-com", start, end)
        row.update({"inner_file_start": start - inner_start,
                    "runtime_start": used_entries[index],
                    "md5": hashlib.md5(data[start:end]).hexdigest()})
        payloads.append(row.copy())
    extent("inner-copy-helper", "code-candidate", inner_start + helper_start, inner_end)
    extent("outer-wrapper", "code-candidate", inner_end, len(data))
    require(partition[0]["file_start"] == 0 and
            partition[-1]["file_end"] == len(data) and
            all(before["file_end"] == after["file_start"]
                for before, after in zip(partition, partition[1:])) and
            sum(row["size"] for row in partition) == len(data),
            "physical partition contains gaps or overlaps")
    return {
        "schema_version": 1,
        "format": "plain-com-comcstm-with-inner-comset",
        "claim": "target container observation; no authored or exact-source acceptance",
        "size": len(data), "sha256": actual_sha256,
        "header_size": header_size, "usage_size": usage_size,
        "timestamp_raw": timestamp, "outer_entry_file_offset": entry,
        "inner_file_start": inner_start, "inner_file_end": inner_end,
        "inner_size": inner_size, "inner_stub_size": stub_size,
        "directory_size": DIRECTORY_SIZE, "procedure_count": count,
        "member_checksum_field": "not observed; SHA-256 values are observer-computed",
        "checks": {"outer_extent": True, "outer_entry": True,
                   "inner_directory": True, "transfer_helper": True,
                   "complete_nonoverlapping_partition": True,
                   "pinned_sha256": expected_sha256 is not None},
        "payloads": payloads, "partition": partition,
    }

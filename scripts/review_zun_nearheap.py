#!/usr/bin/env python3
"""Verify the Borland CT.LIB nearheap member against the original ZUN -S child.

This is a bounded vendor-object ownership proof: the complete 631-byte CODE
segment differs from the pinned CT.LIB member only at its 26 two-byte OMF
relocation fields; the six initialized DATA bytes match verbatim. No compiler
replay, source-byte transcription, or authored-code credit is involved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import tomllib

from lib.borland_library import library_members
from lib.launcher import parse_launcher
from lib.omf import parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_nearheap.toml"
PUBLIC = ROOT / "config/zun_nearheap_acceptance.json"
CLAIM_ORIGIN = "reviewed-native-zun-com-reconstruction"


def _record(kind: int, data: bytes) -> bytes:
    header = bytes([kind]) + struct.pack("<H", len(data) + 1)
    return header + data + bytes([(-sum(header + data)) & 0xFF])


def _object_from_member(member) -> bytes:
    name = member.name.encode("ascii")
    return _record(0x80, bytes([len(name)]) + name) + member.program_records


def _index(data: bytes, position: int) -> tuple[int, int]:
    first = data[position]
    if first & 0x80:
        return (((first & 0x7F) << 8) | data[position + 1], position + 2)
    return first, position + 1


def _module(library_path: Path, config: dict) -> dict:
    library = library_path.read_bytes()
    if digest_bytes(library) != config["library_sha256"]:
        raise ValueError("pinned Borland CT.LIB changed")
    members = [m for m in library_members(library) if m.name.lower() == config["library_member"].lower()]
    if len(members) != 1:
        raise ValueError("nearheap library member is missing or ambiguous")
    member = members[0]
    obj = _object_from_member(member)
    if (digest_bytes(member.program_records) != config["module_program_records_sha256"] or
            digest_bytes(obj) != config["module_object_sha256"]):
        raise ValueError("nearheap member OMF identity changed")

    names: list[str] = []
    segments: dict[int, tuple[int, str, str]] = {}
    publics: dict[str, tuple[int, int]] = {}
    ledatas: dict[int, tuple[int, bytes]] = {}
    fixup_records: list[bytes] = []
    for record in parse_omf(obj):
        data = record.data
        if record.name == "LNAMES":
            position = 0
            while position < len(data):
                length = data[position]
                position += 1
                names.append(data[position:position + length].decode("ascii"))
                position += length
        elif record.name == "SEGDEF":
            position = 0
            attributes = data[position]
            position += 1
            if attributes & 1:
                length = int.from_bytes(data[position:position + 4], "little")
                position += 4
            else:
                length = int.from_bytes(data[position:position + 2], "little")
                position += 2
            name_index, position = _index(data, position)
            class_index, position = _index(data, position)
            _, position = _index(data, position)
            segment = len(segments) + 1
            segments[segment] = (length, names[name_index - 1], names[class_index - 1])
        elif record.name == "PUBDEF":
            position = 0
            _, position = _index(data, position)  # group
            segment, position = _index(data, position)
            if segment == 0:
                position += 2  # frame number
            while position < len(data):
                length = data[position]
                position += 1
                name = data[position:position + length].decode("ascii")
                position += length
                offset = int.from_bytes(data[position:position + 2], "little")
                position += 2
                _, position = _index(data, position)  # type index
                publics[name] = (segment, offset)
        elif record.name == "LEDATA":
            segment, position = _index(data, 0)
            offset = int.from_bytes(data[position:position + 2], "little")
            position += 2
            if segment in ledatas:
                raise ValueError("nearheap segment unexpectedly has split LEDATA")
            ledatas[segment] = (offset, data[position:])
        elif record.name == "FIXUPP":
            fixup_records.append(data)

    if segments != {1: (631, "_TEXT", "CODE"), 2: (6, "_DATA", "DATA")}:
        raise ValueError(f"nearheap OMF segments changed: {segments}")
    expected_publics = {
        "_free": (1, 0), "_malloc": (1, 207), "_realloc": (1, 550),
        "__first": (2, 0), "__last": (2, 2), "__rover": (2, 4),
    }
    if publics != expected_publics:
        raise ValueError(f"nearheap public function/data boundaries changed: {publics}")
    if (set(ledatas) != {1, 2} or ledatas[1][0] != 0 or ledatas[2][0] != 0 or
            len(ledatas[1][1]) != 631 or len(ledatas[2][1]) != 6):
        raise ValueError("nearheap CODE/DATA LEDATA extents changed")
    if (digest_bytes(ledatas[1][1]) != config["code_sha256"] or
            digest_bytes(ledatas[2][1]) != config["data_sha256"]):
        raise ValueError("nearheap CODE/DATA source LEDATA changed")
    if len(fixup_records) != 1 or len(fixup_records[0]) % 5:
        raise ValueError("nearheap FIXUPP structure changed")
    fixups = []
    raw_fixups = fixup_records[0]
    for position in range(0, len(raw_fixups), 5):
        locat = int.from_bytes(raw_fixups[position:position + 2], "big")
        if not (locat & 0x8000):
            raise ValueError("nearheap FIXUPP contains an unsupported thread record")
        location_type = (locat >> 10) & 0x0F
        offset = locat & 0x03FF
        if location_type != 1:
            raise ValueError("nearheap FIXUPP contains a non-16-bit relocation")
        fixups.append(offset)
    if fixups != config["fixup_offsets"] or len(fixups) != 26:
        raise ValueError("nearheap relocation field locations changed")
    return {
        "library_sha256": digest_bytes(library),
        "module_program_records_sha256": digest_bytes(member.program_records),
        "module_object_sha256": digest_bytes(obj),
        "code": ledatas[1][1],
        "data": ledatas[2][1],
        "fixups": fixups,
        "publics": publics,
        "fixup_records_sha256": digest_bytes(b"".join(fixup_records)),
    }


def _target(config: dict) -> tuple[bytes, bytes, bytes]:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    raw = read_verified_artifact(ROOT, artifact)
    if len(raw) != config["container_size"] or artifact["sha256"] != config["target_sha256"]:
        raise ValueError("ZUN container identity changed")
    rows = [row for row in parse_launcher(raw, expected_sha256=artifact["sha256"])["payloads"]
            if row["name"] == config["member"]]
    if len(rows) != 1:
        raise ValueError("original ZUN -S child is missing or ambiguous")
    member = rows[0]
    if (member["file_start"], member["size"], member["sha256"]) != (
            config["member_start"], config["member_size"], config["member_sha256"]):
        raise ValueError("original ZUN -S child identity changed")
    child = raw[member["file_start"]:member["file_end"]]
    code = child[config["code_start_com"] - 0x100:
                 config["code_start_com"] - 0x100 + config["code_size"]]
    data = child[config["data_start_com"] - 0x100:
                 config["data_start_com"] - 0x100 + config["data_size"]]
    if len(code) != config["code_size"] or len(data) != config["data_size"]:
        raise ValueError("nearheap target CODE/DATA slice is incomplete")
    return code, data, artifact["sha256"]


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("nearheap source origin or Borland toolchain identity changed")
    module = _module(ROOT / config["library_path"], config)
    target_code, target_data, target_artifact_sha256 = _target(config)
    code, data, fixups = module["code"], module["data"], module["fixups"]
    relocation_bytes = {offset + delta for offset in fixups for delta in range(config["fixup_width"])}
    mismatches = [i for i, (left, right) in enumerate(zip(code, target_code)) if left != right]
    if set(mismatches) != relocation_bytes or len(mismatches) != 52:
        raise ValueError("nearheap target differs outside its exact 26 two-byte OMF relocations")
    if digest_bytes(data) != digest_bytes(target_data) or target_data != bytes(6):
        raise ValueError("nearheap initialized DATA does not match the original six-byte target")
    resolved_words = [int.from_bytes(target_code[o:o + 2], "little") for o in fixups]
    for address in (0x1A6A, 0x1A6C, 0x1A6E):
        if address not in resolved_words:
            raise ValueError("nearheap target does not resolve its three DATA publics at the expected DS base")

    # A changed non-relocation instruction byte must fail the exact masked
    # comparison; the full target hash separately pins every resolved fixup.
    mutated = bytearray(target_code)
    nonreloc = next(i for i in range(len(mutated)) if i not in relocation_bytes)
    mutated[nonreloc] ^= 1
    negative_nonrelocation = {
        i for i, (left, right) in enumerate(zip(code, mutated)) if left != right
    } != relocation_bytes
    relocation_mutated = bytearray(target_code)
    relocation_mutated[fixups[0]] ^= 1
    negative_relocation = digest_bytes(relocation_mutated) != digest_bytes(target_code)
    if not negative_nonrelocation or not negative_relocation:
        raise ValueError("nearheap source/target negative control failed")

    code_file_start = config["member_start"] + config["code_start_com"] - 0x100
    data_file_start = config["member_start"] + config["data_start_com"] - 0x100
    if (code_file_start, data_file_start) != (config["code_file_start"], config["data_file_start"]):
        raise ValueError("nearheap outer-file offsets changed")
    return {
        "schema_version": 1,
        "kind": "bounded-zun-borland-ctlib-module-ownership-review",
        "manifest_sha256": digest_file(CONFIG),
        "toolchain_manifest_sha256": digest_file(ROOT / "config/toolchain.toml"),
        "target_artifact_sha256": target_artifact_sha256,
        "source_library_sha256": module["library_sha256"],
        "library_member": config["library_member"],
        "module_program_records_sha256": module["module_program_records_sha256"],
        "module_object_sha256": module["module_object_sha256"],
        "fixup_records_sha256": module["fixup_records_sha256"],
        "member_sha256": config["member_sha256"],
        "member_start": config["member_start"],
        "member_size": config["member_size"],
        "origin": config["origin"],
        "global_authored_credit": config["global_authored_credit"],
        "code": {
            "runtime_start": config["code_start_com"],
            "file_start": code_file_start,
            "size": len(code),
            "source_sha256": digest_bytes(code),
            "target_sha256": digest_bytes(target_code),
            "nonrelocation_bytes_exact": len(code) - len(relocation_bytes),
            "relocation_count": len(fixups),
            "relocation_field_bytes": len(relocation_bytes),
            "relocation_offsets": fixups,
            "mismatch_offsets": mismatches,
            "resolved_words": resolved_words,
            "raw_exact": False,
            "exact_after_omf_relocation": True,
        },
        "data": {
            "runtime_start": config["data_start_com"],
            "file_start": data_file_start,
            "size": len(data),
            "source_sha256": digest_bytes(data),
            "target_sha256": digest_bytes(target_data),
            "raw_exact": True,
        },
        "publics": {name: offset for name, (_, offset) in module["publics"].items()},
        "negative_control": {
            "nonrelocation_instruction_flip_rejected": negative_nonrelocation,
            "resolved_relocation_flip_rejected_by_target_hash": negative_relocation,
        },
        "size": len(code) + len(data),
        "code_bytes": len(code),
        "initialized_data_bytes": len(data),
        "authored_credit": 0,
    }


def check() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    expected = evidence(config)
    actual = json.loads(PUBLIC.read_text())
    if actual != expected:
        raise ValueError("nearheap acceptance is stale or its source/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("nearheap review is bound to the live repository root")
    config = tomllib.loads(CONFIG.read_text())
    record = check()
    if (view.get("size") != config["container_size"] or
            view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("nearheap ownership view identity changed")
    library = "Borland Turbo C++ 4.0 CT.LIB"
    claims = [
        {"start": record["code"]["file_start"],
         "end": record["code"]["file_start"] + record["code"]["size"],
         "kind": "verified-vendor-code", "unit": "borland-nearheap",
         "origin": CLAIM_ORIGIN, "source_origin": config["origin"],
         "instruction_bytes": record["code"]["size"],
         "library": library, "member": config["library_member"]},
        {"start": record["data"]["file_start"],
         "end": record["data"]["file_start"] + record["data"]["size"],
         "kind": "verified-vendor-initialized-data", "unit": "borland-nearheap",
         "origin": CLAIM_ORIGIN, "source_origin": config["origin"],
         "instruction_bytes": 0, "authored_credit": 0,
         "content_kind": "library-initialized-data",
         "library": library, "member": config["library_member"]},
    ]
    return claims, digest_file(PUBLIC)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        config = tomllib.loads(CONFIG.read_text())
        record = evidence(config)
        PUBLIC.write_text(json.dumps(record, indent=2) + "\n")
    record = check()
    print("PASS: Borland CT.LIB nearheap: 631 relocated CODE + 6 exact DATA; free/malloc/realloc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

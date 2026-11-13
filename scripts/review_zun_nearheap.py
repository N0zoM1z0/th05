#!/usr/bin/env python3
"""Verify Borland's original CT.LIB nearheap member in the ZUN -S child.

The complete 631-byte CODE segment is reconstructed from the pinned tiny-model
CT.LIB member by applying its real OMF FIXUPP semantics. All 579 nonrelocation
bytes match directly; all 52 relocation bytes resolve to the original DS or
near-Pascal external addresses. Its six initialized DATA bytes match verbatim.
No compiler replay, copied target bytes, or authored-code credit is involved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct
import tomllib

from lib.borland_library import library_members
from lib.launcher import parse_launcher
from lib.omf import parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.toolchain import attest_surface

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
    if position >= len(data):
        raise ValueError("truncated OMF index")
    first = data[position]
    if first & 0x80:
        if position + 2 > len(data):
            raise ValueError("truncated two-byte OMF index")
        return (((first & 0x7F) << 8) | data[position + 1], position + 2)
    return first, position + 1


def _pascal(data: bytes, position: int) -> tuple[str, int]:
    if position >= len(data):
        raise ValueError("truncated OMF Pascal string")
    length = data[position]
    end = position + 1 + length
    if end > len(data):
        raise ValueError("OMF Pascal string exceeds its record")
    return data[position + 1:end].decode("ascii"), end


def _module(library_path: Path, config: dict) -> dict:
    library = library_path.read_bytes()
    if digest_bytes(library) != config["library_sha256"]:
        raise ValueError("pinned Borland CT.LIB changed")
    members = [m for m in library_members(library)
               if m.name.casefold() == config["library_member"].casefold()]
    if len(members) != 1:
        raise ValueError("nearheap library member is missing or ambiguous")
    member = members[0]
    obj = _object_from_member(member)
    if (digest_bytes(member.program_records) != config["module_program_records_sha256"] or
            digest_bytes(obj) != config["module_object_sha256"]):
        raise ValueError("nearheap member OMF identity changed")

    names: list[str] = [""]
    segments: dict[int, tuple[int, str, str]] = {}
    groups: dict[int, tuple[str, list[int]]] = {}
    publics: dict[str, tuple[int, int]] = {}
    externals: list[str] = []
    ledatas: dict[int, tuple[int, bytes]] = {}
    fixup_records: list[bytes] = []
    fixups: list[dict] = []
    current: tuple[int, int] | None = None

    for record in parse_omf(obj):
        data = record.data
        if record.name == "LNAMES":
            position = 0
            while position < len(data):
                value, position = _pascal(data, position)
                names.append(value)
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
            if (not 0 < name_index < len(names) or
                    not 0 < class_index < len(names) or position != len(data)):
                raise ValueError("nearheap SEGDEF contains an invalid name or trailing data")
            segments[len(segments) + 1] = (
                length, names[name_index], names[class_index]
            )
        elif record.name == "GRPDEF":
            position = 0
            name_index, position = _index(data, position)
            if not 0 < name_index < len(names):
                raise ValueError("nearheap GRPDEF has an invalid group name")
            members_in_group = []
            while position < len(data):
                if data[position] != 0xFF:
                    raise ValueError("nearheap GRPDEF has an unsupported component")
                position += 1
                segment_index, position = _index(data, position)
                members_in_group.append(segment_index)
            groups[len(groups) + 1] = (names[name_index], members_in_group)
        elif record.name == "PUBDEF":
            position = 0
            _, position = _index(data, position)  # group index
            segment, position = _index(data, position)
            if segment == 0:
                position += 2  # absolute frame
            while position < len(data):
                name, position = _pascal(data, position)
                if position + 2 > len(data):
                    raise ValueError("nearheap PUBDEF is truncated")
                offset = int.from_bytes(data[position:position + 2], "little")
                position += 2
                _, position = _index(data, position)  # type index
                if name in publics:
                    raise ValueError("nearheap PUBDEF repeats a symbol")
                publics[name] = (segment, offset)
        elif record.name == "EXTDEF":
            position = 0
            while position < len(data):
                name, position = _pascal(data, position)
                _, position = _index(data, position)  # type index
                externals.append(name)
        elif record.name == "LEDATA":
            segment, position = _index(data, 0)
            if position + 2 > len(data):
                raise ValueError("nearheap LEDATA is truncated")
            offset = int.from_bytes(data[position:position + 2], "little")
            position += 2
            if segment in ledatas:
                raise ValueError("nearheap segment unexpectedly has split LEDATA")
            ledatas[segment] = (offset, data[position:])
            current = (segment, offset)
        elif record.name == "FIXUPP":
            if current is None:
                raise ValueError("nearheap FIXUPP has no preceding LEDATA")
            fixup_records.append(data)
            position = 0
            while position < len(data):
                if position + 3 > len(data):
                    raise ValueError("nearheap FIXUPP is truncated")
                locat, low, fixdat = data[position:position + 3]
                position += 3
                if not (locat & 0x80) or fixdat & 0x88:
                    raise ValueError("nearheap FIXUPP uses threaded/unsupported records")
                site = ((locat & 3) << 8) | low
                location_type = (locat >> 2) & 0x0F
                relative = not bool(locat & 0x40)
                frame_method = (fixdat >> 4) & 7
                target_method = fixdat & 3
                has_no_displacement = bool(fixdat & 4)
                frame_index = None
                if frame_method <= 2:
                    frame_index, position = _index(data, position)
                elif frame_method not in (4, 5, 6, 7):
                    raise ValueError("nearheap FIXUPP has an unsupported frame method")
                if target_method == 3:
                    raise ValueError("nearheap FIXUPP has an unsupported absolute target")
                target_index, position = _index(data, position)
                displacement = 0
                if not has_no_displacement:
                    if position + 2 > len(data):
                        raise ValueError("nearheap FIXUPP displacement is truncated")
                    displacement = int.from_bytes(data[position:position + 2], "little")
                    position += 2
                fixups.append({
                    "segment": current[0],
                    "site": current[1] + site,
                    "location_type": location_type,
                    "relative": relative,
                    "frame_method": frame_method,
                    "frame_index": frame_index,
                    "target_method": target_method,
                    "target_index": target_index,
                    "displacement": displacement,
                })

    if segments != {1: (631, "_TEXT", "CODE"), 2: (6, "_DATA", "DATA")}:
        raise ValueError(f"nearheap OMF segments changed: {segments}")
    if groups != {1: ("DGROUP", [2])}:
        raise ValueError(f"nearheap OMF group layout changed: {groups}")
    expected_publics = {
        "_free": (1, 0), "_malloc": (1, 207), "_realloc": (1, 550),
        "__first": (2, 0), "__last": (2, 2), "__rover": (2, 4),
    }
    if publics != expected_publics:
        raise ValueError(f"nearheap public function/data boundaries changed: {publics}")
    if externals != ["___brk", "___sbrk"]:
        raise ValueError(f"nearheap external symbol order changed: {externals}")
    if (set(ledatas) != {1, 2} or ledatas[1][0] != 0 or ledatas[2][0] != 0 or
            len(ledatas[1][1]) != 631 or len(ledatas[2][1]) != 6):
        raise ValueError("nearheap CODE/DATA LEDATA extents changed")
    if (digest_bytes(ledatas[1][1]) != config["code_sha256"] or
            digest_bytes(ledatas[2][1]) != config["data_sha256"]):
        raise ValueError("nearheap CODE/DATA source LEDATA changed")
    if (len(fixups) != 26 or
            [fixup["site"] for fixup in fixups] != config["fixup_offsets"] or
            any(fixup["segment"] != 1 or fixup["location_type"] != 1 or
                fixup["displacement"] != 0 for fixup in fixups)):
        raise ValueError("nearheap OMF FIXUPP locations/widths/order changed")

    segment_fixups = [f for f in fixups if f["target_method"] == 0]
    external_fixups = [f for f in fixups if f["target_method"] == 2]
    if (len(segment_fixups) != 20 or len(external_fixups) != 6 or
            any(f["relative"] or f["frame_method"] != 1 or f["frame_index"] != 1 or
                f["target_index"] != 2 for f in segment_fixups) or
            any(not f["relative"] or f["frame_method"] != 0 or f["frame_index"] != 1 or
                f["target_index"] not in (1, 2) for f in external_fixups)):
        raise ValueError("nearheap OMF FIXUPP frame/target semantics changed")

    return {
        "library_sha256": digest_bytes(library),
        "module_program_records_sha256": digest_bytes(member.program_records),
        "module_object_sha256": digest_bytes(obj),
        "code": ledatas[1][1],
        "data": ledatas[2][1],
        "fixups": fixups,
        "publics": publics,
        "externals": externals,
        "groups": groups,
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
    for symbol, address in config["external_targets"].items():
        signature = bytes.fromhex(config["external_target_signatures"][symbol])
        if child[address - 0x100:address - 0x100 + len(signature)] != signature:
            raise ValueError(f"nearheap external target {symbol} no longer starts at {address:04X}")
    return code, data, artifact["sha256"]


def _resolve_code(source: bytes, fixups: list[dict], config: dict,
                  external_names: list[str]) -> tuple[bytes, list[dict]]:
    expected = bytearray(source)
    resolved = []
    external_targets = config["external_targets"]
    for fixup in fixups:
        site = fixup["site"]
        if site < 0 or site + 2 > len(source):
            raise ValueError("nearheap OMF relocation extends beyond its CODE segment")
        source_word = int.from_bytes(source[site:site + 2], "little")
        if (fixup["target_method"] == 0 and not fixup["relative"] and
                fixup["frame_method"] == 1 and fixup["frame_index"] == 1 and
                fixup["target_index"] == 2):
            symbol = "_DATA"
            value = config["data_start_com"] + source_word + fixup["displacement"]
        elif (fixup["target_method"] == 2 and fixup["relative"] and
              fixup["frame_method"] == 0 and fixup["frame_index"] == 1 and
              1 <= fixup["target_index"] <= len(external_names)):
            symbol = external_names[fixup["target_index"] - 1]
            if symbol not in external_targets:
                raise ValueError("nearheap OMF external target lacks a pinned original address")
            next_ip = config["code_start_com"] + site + 2
            value = (external_targets[symbol] - next_ip + source_word +
                     fixup["displacement"])
        else:
            raise ValueError("nearheap OMF relocation does not match a reviewed target/frame")
        value &= 0xFFFF
        expected[site:site + 2] = value.to_bytes(2, "little")
        resolved.append({
            "site": site,
            "symbol": symbol,
            "source_addend": source_word,
            "resolved_word": value,
        })
    return bytes(expected), resolved


def _verify_target_code(source: bytes, target: bytes, fixups: list[dict],
                        config: dict, external_names: list[str]) -> tuple[list[int], list[dict]]:
    expected, resolved = _resolve_code(source, fixups, config, external_names)
    if expected != target:
        raise ValueError("nearheap target CODE is not the exact OMF-relocated CT.LIB module")
    relocation_bytes = {f["site"] + delta for f in fixups for delta in range(2)}
    mismatches = [i for i, (left, right) in enumerate(zip(source, target)) if left != right]
    if set(mismatches) != relocation_bytes or len(mismatches) != 52:
        raise ValueError("nearheap target differs outside its exact 26 two-byte OMF relocations")
    return mismatches, resolved


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or
            config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("nearheap source origin or Borland toolchain identity changed")
    toolchain = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surfaces = [row for row in toolchain["surfaces"] if row["id"] == "tc40j-lib"]
    if len(surfaces) != 1:
        raise ValueError("pinned TC4J library tree surface is missing or ambiguous")
    surface = attest_surface(ROOT, surfaces[0])
    if (not surface.get("pass") or
            surface.get("actual_sha256") != config["library_tree_sha256"] or
            surface.get("file_count") != config["library_tree_file_count"]):
        raise ValueError("complete pinned Borland library tree no longer verifies")

    module = _module(ROOT / config["library_path"], config)
    target_code, target_data, target_artifact_sha256 = _target(config)
    code, data, fixups = module["code"], module["data"], module["fixups"]
    mismatches, resolved = _verify_target_code(code, target_code, fixups, config, module["externals"])
    if (digest_bytes(data) != digest_bytes(target_data) or target_data != bytes(config["data_size"])):
        raise ValueError("nearheap initialized DATA does not match the original six-byte target")

    # Exercise the exact verifier, not a hash-only surrogate, with both a
    # nonrelocation instruction mutation and a changed linked relocation word.
    relocation_bytes = {f["site"] + delta for f in fixups for delta in range(2)}
    nonrelocation = next(i for i in range(len(target_code)) if i not in relocation_bytes)
    negative_instruction = bytearray(target_code)
    negative_instruction[nonrelocation] ^= 1
    try:
        _verify_target_code(code, bytes(negative_instruction), fixups, config, module["externals"])
        rejected_instruction = False
    except ValueError:
        rejected_instruction = True
    negative_relocation = bytearray(target_code)
    negative_relocation[fixups[0]["site"]] ^= 1
    try:
        _verify_target_code(code, bytes(negative_relocation), fixups, config, module["externals"])
        rejected_relocation = False
    except ValueError:
        rejected_relocation = True
    if not rejected_instruction or not rejected_relocation:
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
        "library_tree_sha256": surface["actual_sha256"],
        "library_tree_file_count": surface["file_count"],
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
            "relocated_sha256": digest_bytes(_resolve_code(code, fixups, config, module["externals"])[0]),
            "nonrelocation_bytes_exact": len(code) - len(relocation_bytes),
            "relocation_count": len(fixups),
            "relocation_field_bytes": len(relocation_bytes),
            "relocation_offsets": [f["site"] for f in fixups],
            "mismatch_offsets": mismatches,
            "resolved_relocations": resolved,
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
        "externals": module["externals"],
        "groups": {str(index): [name, members] for index, (name, members) in module["groups"].items()},
        "negative_control": {
            "nonrelocation_instruction_flip_rejected": rejected_instruction,
            "resolved_relocation_flip_rejected": rejected_relocation,
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
         "instruction_bytes": record["code"]["size"], "authored_credit": 0,
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
    check()
    print("PASS: Borland CT.LIB nearheap: 631 relocated CODE + 6 exact DATA; free/malloc/realloc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify the complete first Borland CT.LIB code partition in ZUN -S."""
from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from collections import OrderedDict
from pathlib import Path

from lib.borland_library import library_members
from lib.launcher import parse_launcher
from lib.omf import parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.tiny_com import TINY_CRT_SHA256
from lib.toolchain import attest_surface
from review_zun_nearheap import _index, _object_from_member, _pascal

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_early_ctlib.toml"
PUBLIC = ROOT / "config/zun_early_ctlib_acceptance.json"
CLAIM_ORIGIN = "original-borland-ct-library-object"
LIBRARY_NAME = "Borland Turbo C++ 4.0 CT.LIB"


def _parse_object(obj: bytes) -> dict:
    names = [""]
    segments: dict[int, tuple[int, str, str]] = {}
    groups: dict[int, tuple[str, list[int]]] = {}
    publics: OrderedDict[str, tuple[int, int]] = OrderedDict()
    externals: list[str] = []
    ledatas: list[dict] = []
    fixups: list[dict] = []
    fixup_records: list[bytes] = []
    current: tuple[int, int] | None = None
    record_counts: OrderedDict[str, int] = OrderedDict()

    for record in parse_omf(obj):
        record_counts[record.name] = record_counts.get(record.name, 0) + 1
        data = record.data
        if record.name == "LNAMES":
            position = 0
            while position < len(data):
                name, position = _pascal(data, position)
                names.append(name)
        elif record.name == "SEGDEF":
            position = 1
            attributes = data[0]
            if attributes & 1:
                length = int.from_bytes(data[position:position + 4], "little")
                position += 4
            else:
                length = int.from_bytes(data[position:position + 2], "little")
                position += 2
            name_index, position = _index(data, position)
            class_index, position = _index(data, position)
            _, position = _index(data, position)
            if name_index >= len(names) or class_index >= len(names):
                raise ValueError("CT.LIB SEGDEF refers to an absent LNAMES entry")
            segment_index = len(segments) + 1
            segments[segment_index] = (length, names[name_index], names[class_index])
        elif record.name == "GRPDEF":
            position = 0
            name_index, position = _index(data, position)
            if name_index >= len(names):
                raise ValueError("CT.LIB GRPDEF refers to an absent LNAMES entry")
            members = []
            while position < len(data):
                if data[position] != 0xFF:
                    raise ValueError("CT.LIB GRPDEF contains a non-segment component")
                position += 1
                segment_index, position = _index(data, position)
                members.append(segment_index)
            group_index = len(groups) + 1
            groups[group_index] = (names[name_index], members)
        elif record.name == "PUBDEF":
            position = 0
            _, position = _index(data, position)  # group index
            segment_index, position = _index(data, position)
            if segment_index == 0:
                position += 2  # absolute frame
            while position < len(data):
                name, position = _pascal(data, position)
                if position + 2 > len(data):
                    raise ValueError("CT.LIB PUBDEF is truncated")
                offset = int.from_bytes(data[position:position + 2], "little")
                position += 2
                _, position = _index(data, position)  # type index
                if name in publics:
                    raise ValueError("CT.LIB PUBDEF repeats a symbol")
                publics[name] = (segment_index, offset)
        elif record.name == "EXTDEF":
            position = 0
            while position < len(data):
                name, position = _pascal(data, position)
                _, position = _index(data, position)  # type index
                externals.append(name)
        elif record.name == "LEDATA":
            segment_index, position = _index(data, 0)
            if position + 2 > len(data):
                raise ValueError("CT.LIB LEDATA is truncated")
            offset = int.from_bytes(data[position:position + 2], "little")
            position += 2
            ledatas.append({"segment": segment_index, "offset": offset, "data": data[position:]})
            current = (segment_index, offset)
        elif record.name == "FIXUPP":
            if current is None:
                raise ValueError("CT.LIB FIXUPP has no preceding LEDATA")
            fixup_records.append(data)
            position = 0
            while position < len(data):
                if position + 3 > len(data):
                    raise ValueError("CT.LIB FIXUPP is truncated")
                locat, low, fixdat = data[position:position + 3]
                position += 3
                if not (locat & 0x80) or fixdat & 0x88:
                    raise ValueError("CT.LIB FIXUPP uses threaded or unsupported records")
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
                    raise ValueError("CT.LIB FIXUPP has an unsupported frame method")
                if target_method == 3:
                    raise ValueError("CT.LIB FIXUPP has an unsupported absolute target")
                target_index, position = _index(data, position)
                displacement = 0
                if not has_no_displacement:
                    if position + 2 > len(data):
                        raise ValueError("CT.LIB FIXUPP displacement is truncated")
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

    return {
        "segments": segments,
        "groups": groups,
        "publics": publics,
        "externals": externals,
        "ledatas": ledatas,
        "fixups": fixups,
        "fixup_records": fixup_records,
        "record_counts": record_counts,
        "object_sha256": digest_bytes(obj),
    }


def _format_module(module: dict) -> dict:
    return {
        "segments": [f"{index}|{length}|{name}|{class_name}"
                     for index, (length, name, class_name) in module["segments"].items()],
        "groups": [f"{index}|{name}|{','.join(str(x) for x in members)}"
                   for index, (name, members) in module["groups"].items()],
        "ledatas": [f"{row['segment']}|{row['offset']}|{len(row['data'])}"
                    for row in module["ledatas"]],
        "publics": [f"{name}|{segment}|{offset}"
                    for name, (segment, offset) in module["publics"].items()],
        "externals": module["externals"],
        "fixups_by_segment": _fixups_by_segment(module["fixups"]),
    }


def _fixups_by_segment(fixups: list[dict]) -> list[str]:
    grouped: OrderedDict[int, list[int]] = OrderedDict()
    for fixup in fixups:
        grouped.setdefault(fixup["segment"], []).append(fixup["site"])
    return [f"{segment}|{','.join(str(site) for site in sites)}"
            for segment, sites in grouped.items()]


def _parse_definition(value: str) -> tuple[str, int, int]:
    member, segment, offset = value.split("|")
    return member, int(segment), int(offset)


def _symbol_definition_address(symbol: str, definition: str, modules: dict,
                               config: dict, c0t: dict) -> dict:
    member_name, segment_index, offset = _parse_definition(definition)
    if member_name == "C0T.OBJ":
        module = c0t
        base_key = f"C0T.OBJ:{segment_index}"
        if base_key not in config["external_segment_bases"]:
            raise ValueError(f"C0T external segment base is missing for {symbol}")
        base = config["external_segment_bases"][base_key]
        spec = config["external_segment_specs"][base_key]
    else:
        module = modules.get(member_name)
        if module is None:
            raise ValueError(f"external CT.LIB member {member_name} is absent")
        base_key = f"{member_name}:{segment_index}"
        if member_name in {row["name"] for row in config["modules"]}:
            row = next(row for row in config["modules"] if row["name"] == member_name)
            if segment_index == 1:
                base = row["start_com"]
            else:
                key = f"{member_name}:{segment_index}"
                if key not in config["segment_bases"]:
                    raise ValueError(f"internal segment base is missing for {symbol}")
                base = config["segment_bases"][key]
            spec = None
        else:
            if base_key not in config["external_segment_bases"]:
                raise ValueError(f"external segment base is missing for {symbol}")
            base = config["external_segment_bases"][base_key]
            spec = config["external_segment_specs"][base_key]
    if symbol not in module["publics"]:
        raise ValueError(f"external symbol {symbol} is not public in {member_name}")
    actual_segment, actual_offset = module["publics"][symbol]
    if (actual_segment, actual_offset) != (segment_index, offset):
        raise ValueError(f"external public boundary changed for {symbol}")
    if segment_index not in module["segments"]:
        raise ValueError(f"external public {symbol} refers to a missing segment")
    length, name, class_name = module["segments"][segment_index]
    if offset > length and length != 0:
        raise ValueError(f"external public {symbol} lies outside its segment")
    if spec is not None and f"{length}:{name}:{class_name}" != spec:
        raise ValueError(f"external segment layout changed for {symbol}")
    return {
        "member": member_name,
        "segment": segment_index,
        "offset": offset,
        "segment_base": base,
        "address": (base + offset) & 0xFFFF,
        "segment_length": length,
        "segment_name": name,
        "segment_class": class_name,
    }


def _resolve_code(module_name: str, start_com: int, source: bytes,
                  fixups: list[dict], externals: list[str], config: dict) -> tuple[bytes, list[dict]]:
    expected = bytearray(source)
    resolved = []
    for fixup in fixups:
        if fixup["segment"] != 1:
            continue
        site = fixup["site"]
        if fixup["location_type"] != 1 or site < 0 or site + 2 > len(source):
            raise ValueError(f"{module_name} has a non-16-bit or out-of-range CODE relocation")
        source_word = int.from_bytes(source[site:site + 2], "little")
        if fixup["relative"]:
            if fixup["frame_method"] == 5:
                if fixup["frame_index"] is not None:
                    raise ValueError(f"{module_name} target-frame relocation has an explicit frame index")
            elif fixup["frame_method"] == 0:
                if fixup["frame_index"] != 1:
                    raise ValueError(f"{module_name} self-relative relocation is not framed by its CODE segment")
            else:
                raise ValueError(f"{module_name} relative relocation uses an unreviewed OMF frame method")
        elif fixup["frame_method"] != 1 or fixup["frame_index"] != 1:
            raise ValueError(f"{module_name} absolute relocation is not framed by DGROUP")
        if fixup["target_method"] == 2:
            if not (1 <= fixup["target_index"] <= len(externals)):
                raise ValueError(f"{module_name} CODE relocation has an invalid EXTDEF index")
            symbol = externals[fixup["target_index"] - 1]
            if symbol not in config["external_targets"]:
                raise ValueError(f"{module_name} external target {symbol} is not pinned")
            target_address = config["external_targets"][symbol]
        elif fixup["target_method"] == 0:
            symbol = f"{module_name}:SEG{fixup['target_index']}"
            key = f"{module_name}:{fixup['target_index']}"
            if key not in config["segment_bases"]:
                raise ValueError(f"{module_name} internal segment base {key} is not pinned")
            target_address = config["segment_bases"][key]
        else:
            raise ValueError(f"{module_name} CODE relocation uses an unsupported target method")
        if fixup["relative"]:
            value = (target_address - (start_com + site + 2) + source_word +
                     fixup["displacement"])
        else:
            value = target_address + source_word + fixup["displacement"]
        value &= 0xFFFF
        expected[site:site + 2] = value.to_bytes(2, "little")
        resolved.append({
            "site": site,
            "symbol": symbol,
            "relative": fixup["relative"],
            "frame_method": fixup["frame_method"],
            "frame_index": fixup["frame_index"],
            "target_method": fixup["target_method"],
            "target_index": fixup["target_index"],
            "displacement": fixup["displacement"],
            "source_addend": source_word,
            "target_address": target_address,
            "resolved_word": value,
        })
    return bytes(expected), resolved


def _verify_code(module_name: str, start_com: int, source: bytes, target: bytes,
                 fixups: list[dict], externals: list[str], config: dict) -> dict:
    expected, resolved = _resolve_code(module_name, start_com, source, fixups, externals, config)
    if expected != target:
        raise ValueError(f"{module_name} target CODE is not the exact OMF-relocated CT.LIB segment")
    relocation_bytes = {fixup["site"] + delta for fixup in fixups
                        if fixup["segment"] == 1 for delta in range(2)}
    mismatches = [index for index, (left, right) in enumerate(zip(source, target))
                  if left != right]
    if not set(mismatches).issubset(relocation_bytes):
        raise ValueError(f"{module_name} differs outside OMF FIXUPP relocation fields")
    return {
        "source_sha256": digest_bytes(source),
        "target_sha256": digest_bytes(target),
        "relocated_sha256": digest_bytes(expected),
        "nonrelocation_bytes_exact": len(source) - len(relocation_bytes),
        "relocation_count": sum(1 for fixup in fixups if fixup["segment"] == 1),
        "relocation_field_bytes": len(relocation_bytes),
        "relocation_offsets": [fixup["site"] for fixup in fixups if fixup["segment"] == 1],
        "mismatch_offsets": mismatches,
        "resolved_relocations": resolved,
        "raw_exact": source == target,
        "exact_after_omf_relocation": True,
    }


def _load_target(config: dict) -> tuple[dict, bytes, str]:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    raw = read_verified_artifact(ROOT, artifact)
    if len(raw) != config["container_size"] or artifact["sha256"] != config["target_sha256"]:
        raise ValueError("ZUN container identity changed")
    layout = parse_launcher(raw, expected_sha256=artifact["sha256"])
    rows = [row for row in layout["payloads"] if row["name"] == config["member"]]
    if len(rows) != 1:
        raise ValueError("original ZUN -S child is missing or ambiguous")
    row = rows[0]
    if (row["file_start"], row["size"], row["sha256"]) != (
            config["member_start"], config["member_size"], config["member_sha256"]):
        raise ValueError("original ZUN -S child identity changed")
    return row, raw[row["file_start"]:row["file_end"]], artifact["sha256"]


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or
            config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("ZUN early CT.LIB source origin/toolchain identity changed")
    toolchain = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surfaces = [row for row in toolchain["surfaces"] if row["id"] == "tc40j-lib"]
    if len(surfaces) != 1:
        raise ValueError("pinned TC4J library tree surface is missing or ambiguous")
    surface = attest_surface(ROOT, surfaces[0])
    if (not surface.get("pass") or
            surface.get("actual_sha256") != config["library_tree_sha256"] or
            surface.get("file_count") != config["library_tree_file_count"]):
        raise ValueError("complete pinned Borland library tree no longer verifies")

    library_path = ROOT / config["library_path"]
    library = library_path.read_bytes()
    if digest_bytes(library) != config["library_sha256"]:
        raise ValueError("original CT.LIB archive identity changed")
    members = library_members(library)
    member_by_name = {member.name.lower(): member for member in members}
    if len(member_by_name) != len(members):
        raise ValueError("CT.LIB member names are no longer unique")

    parsed_modules = {}
    module_records = {}
    target_row, child, target_artifact_sha256 = _load_target(config)
    modules_evidence = []
    code_intervals = []
    external_symbols_referenced = set()

    for spec in config["modules"]:
        name = spec["name"]
        member = member_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"original CT.LIB member {name} is missing")
        obj = _object_from_member(member)
        parsed = _parse_object(obj)
        parsed_modules[name] = parsed
        module_records[name] = member
        formatted = _format_module(parsed)
        for key in ("segments", "groups", "ledatas", "publics", "externals", "fixups_by_segment"):
            if formatted[key] != spec[key]:
                raise ValueError(f"CT.LIB {name} {key} changed: {formatted[key]}")
        if parsed["segments"].get(1) != (spec["code_size"], "_TEXT", "CODE"):
            raise ValueError(f"CT.LIB {name} CODE SEGDEF changed")
        code_ledatas = [row for row in parsed["ledatas"] if row["segment"] == 1]
        if len(code_ledatas) != 1 or code_ledatas[0]["offset"] != 0 or len(code_ledatas[0]["data"]) != spec["code_size"]:
            raise ValueError(f"CT.LIB {name} CODE LEDATA is not a complete segment")
        source = code_ledatas[0]["data"]
        start = spec["start_com"]
        target = child[start - 0x100:start - 0x100 + spec["code_size"]]
        if len(target) != spec["code_size"]:
            raise ValueError(f"ZUN -S {name} target CODE slice is incomplete")
        code_fixups = [fixup for fixup in parsed["fixups"] if fixup["segment"] == 1]
        external_symbols_referenced.update(
            parsed["externals"][fixup["target_index"] - 1]
            for fixup in code_fixups if fixup["target_method"] == 2
        )
        code_result = _verify_code(name, start, source, target, code_fixups,
                                   parsed["externals"], config)
        code_file_start = config["member_start"] + start - 0x100
        code_intervals.append((start, start + spec["code_size"], name))
        modules_evidence.append({
            "name": name,
            "start_com": start,
            "end_com": start + spec["code_size"],
            "file_start": code_file_start,
            "code_size": spec["code_size"],
            "program_records_sha256": digest_bytes(member.program_records),
            "object_sha256": parsed["object_sha256"],
            "fixup_records_sha256": digest_bytes(b"".join(parsed["fixup_records"])),
            "record_counts": dict(parsed["record_counts"]),
            "segments": formatted["segments"],
            "groups": formatted["groups"],
            "ledatas": formatted["ledatas"],
            "publics": formatted["publics"],
            "externals": formatted["externals"],
            "fixups_by_segment": formatted["fixups_by_segment"],
            "code": code_result,
        })

    code_intervals.sort()
    cursor = config["region_start_com"]
    for start, end, name in code_intervals:
        if start != cursor or end <= start:
            raise ValueError(f"ZUN early CT.LIB code partition has a gap/overlap before {name}")
        cursor = end
    if cursor != config["region_end_com"]:
        raise ValueError("ZUN early CT.LIB code partition does not close the complete interval")
    code_bytes = sum(end - start for start, end, _ in code_intervals)
    if code_bytes != config["region_end_com"] - config["region_start_com"]:
        raise ValueError("ZUN early CT.LIB code byte total changed")

    c0t_path = ROOT / config["c0t_object_path"]
    c0t_raw = c0t_path.read_bytes()
    if digest_bytes(c0t_raw) != TINY_CRT_SHA256:
        raise ValueError("original pinned C0T.OBJ identity changed")
    c0t = _parse_object(c0t_raw)

    external_module_names = {
        member for member, _, _ in (_parse_definition(value)
                                    for value in config["external_definitions"].values())
        if member != "C0T.OBJ" and member not in parsed_modules
    }
    external_modules = {}
    for name in sorted(external_module_names):
        member = member_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"CT.LIB external-definition member {name} is missing")
        external_modules[name] = _parse_object(_object_from_member(member))

    symbol_definitions = {}
    for symbol, definition in config["external_definitions"].items():
        member_name, segment_index, offset = _parse_definition(definition)
        if member_name == "C0T.OBJ":
            module = c0t
        elif member_name in parsed_modules:
            module = parsed_modules[member_name]
        else:
            module = external_modules[member_name]
        if symbol not in module["publics"]:
            raise ValueError(f"external symbol {symbol} is not a public of {member_name}")
        actual_segment, actual_offset = module["publics"][symbol]
        if (actual_segment, actual_offset) != (segment_index, offset):
            raise ValueError(f"external public boundary changed for {symbol}")
        if segment_index not in module["segments"]:
            raise ValueError(f"external public {symbol} refers to a missing segment")
        length, segment_name, class_name = module["segments"][segment_index]
        if member_name in parsed_modules:
            spec = next(row for row in config["modules"] if row["name"] == member_name)
            base = (spec["start_com"] if segment_index == 1 else
                    config["segment_bases"][f"{member_name}:{segment_index}"])
        else:
            base_key = f"{member_name}:{segment_index}"
            if base_key not in config["external_segment_bases"]:
                raise ValueError(f"external segment base is missing for {symbol}")
            base = config["external_segment_bases"][base_key]
            expected_segment = config["external_segment_specs"][base_key]
            if f"{length}:{segment_name}:{class_name}" != expected_segment:
                raise ValueError(f"external segment layout changed for {symbol}")
        address = (base + offset) & 0xFFFF
        if address != config["external_targets"][symbol]:
            raise ValueError(f"external target {symbol} does not resolve to its original public")
        symbol_definitions[symbol] = {
            "member": member_name,
            "segment": segment_index,
            "offset": offset,
            "segment_base": base,
            "address": address,
            "segment_length": length,
            "segment_name": segment_name,
            "segment_class": class_name,
        }

    if external_symbols_referenced != set(config["external_targets"]):
        raise ValueError("early CT.LIB external target inventory changed")

    # Both a normal instruction mutation and a linked relocation mutation must
    # be rejected by the same OMF-aware verifier used for the live target.
    first = modules_evidence[0]
    first_spec = config["modules"][0]
    first_source = next(row["data"] for row in parsed_modules[first_spec["name"]]["ledatas"]
                        if row["segment"] == 1)
    first_target = child[first_spec["start_com"] - 0x100:
                         first_spec["start_com"] - 0x100 + first_spec["code_size"]]
    first_fixups = [f for f in parsed_modules[first_spec["name"]]["fixups"] if f["segment"] == 1]
    relocation_bytes = {f["site"] + delta for f in first_fixups for delta in range(2)}
    nonrelocation_offset = next(i for i in range(len(first_target)) if i not in relocation_bytes)
    negative_instruction = bytearray(first_target)
    negative_instruction[nonrelocation_offset] ^= 1
    try:
        _verify_code(first_spec["name"], first_spec["start_com"], first_source,
                     bytes(negative_instruction), first_fixups,
                     parsed_modules[first_spec["name"]]["externals"], config)
        rejected_instruction = False
    except ValueError:
        rejected_instruction = True
    setup_spec = next(row for row in config["modules"] if row["name"] == "setupio")
    setup_parsed = parsed_modules["setupio"]
    setup_source = next(row["data"] for row in setup_parsed["ledatas"] if row["segment"] == 1)
    setup_target = child[setup_spec["start_com"] - 0x100:
                         setup_spec["start_com"] - 0x100 + setup_spec["code_size"]]
    setup_fixups = [f for f in setup_parsed["fixups"] if f["segment"] == 1]
    negative_relocation = bytearray(setup_target)
    negative_relocation[setup_fixups[0]["site"]] ^= 1
    try:
        _verify_code("setupio", setup_spec["start_com"], setup_source,
                     bytes(negative_relocation), setup_fixups,
                     setup_parsed["externals"], config)
        rejected_relocation = False
    except ValueError:
        rejected_relocation = True
    if not rejected_instruction or not rejected_relocation:
        raise ValueError("ZUN early CT.LIB negative control failed")

    file_start = config["member_start"] + config["region_start_com"] - 0x100
    file_end = config["member_start"] + config["region_end_com"] - 0x100
    if (file_start, file_end) != (0x13BA, 0x1601):
        raise ValueError("ZUN early CT.LIB outer-file interval changed")

    return {
        "schema_version": 1,
        "kind": "bounded-zun-borland-ctlib-code-ownership-review",
        "manifest_sha256": digest_file(CONFIG),
        "toolchain_manifest_sha256": digest_file(ROOT / "config/toolchain.toml"),
        "library_sha256": digest_bytes(library),
        "library_tree_sha256": surface["actual_sha256"],
        "library_tree_file_count": surface["file_count"],
        "target_artifact_sha256": target_artifact_sha256,
        "member": config["member"],
        "member_start": target_row["file_start"],
        "member_size": target_row["size"],
        "member_sha256": target_row["sha256"],
        "c0t_object_sha256": digest_bytes(c0t_raw),
        "origin": config["origin"],
        "global_authored_credit": config["global_authored_credit"],
        "region": {
            "start_com": config["region_start_com"],
            "end_com": config["region_end_com"],
            "file_start": file_start,
            "file_end": file_end,
            "size": code_bytes,
            "fully_partitioned": True,
            "module_count": len(modules_evidence),
        },
        "modules": modules_evidence,
        "external_symbol_definitions": symbol_definitions,
        "internal_segment_bases": config["segment_bases"],
        "negative_control": {
            "nonrelocation_instruction_flip_rejected": rejected_instruction,
            "resolved_relocation_flip_rejected": rejected_relocation,
        },
        "authored_credit": 0,
        "instruction_bytes": code_bytes,
    }


def check() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    expected = evidence(config)
    actual = json.loads(PUBLIC.read_text())
    if actual != expected:
        raise ValueError("ZUN early CT.LIB acceptance is stale or its source/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("ZUN early CT.LIB review is bound to the live repository root")
    config = tomllib.loads(CONFIG.read_text())
    record = check()
    if (view.get("size") != config["container_size"] or
            view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("ZUN early CT.LIB ownership view identity changed")
    claims = []
    for module in record["modules"]:
        claims.append({
            "start": module["file_start"],
            "end": module["file_start"] + module["code_size"],
            "kind": "verified-vendor-code",
            "unit": f"borland-ctlib-{module['name']}",
            "origin": CLAIM_ORIGIN,
            "source_origin": config["origin"],
            "instruction_bytes": module["code_size"],
            "authored_credit": 0,
            "content_kind": "original-OMF-CODE-LEDATA",
            "library": LIBRARY_NAME,
            "member": module["name"],
        })
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
    print(f"PASS: ZUN -S early CT.LIB: {record['instruction_bytes']} relocated CODE bytes, "
          f"{record['region']['module_count']} complete OMF members, no authored credit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

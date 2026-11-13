#!/usr/bin/env python3
"""Verify the complete resident stdio/path CT.LIB CODE partition in ZUN -S."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib

from lib.borland_library import library_members
from lib.launcher import parse_launcher
from lib.omf import parse_omf
from lib.pc98 import digest_bytes, digest_file
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.tiny_com import TINY_CRT_SHA256
from lib.toolchain import attest_surface
from review_zun_early_ctlib import _format_module, _object_from_member, _parse_object

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_stdio_ctlib.toml"
PUBLIC = ROOT / "config/zun_stdio_ctlib_acceptance.json"
CLAIM_ORIGIN = "reviewed-native-zun-com-reconstruction"
LIBRARY_NAME = "Borland Turbo C++ 4.0 CT.LIB"


def _definition(value: str) -> tuple[str, int, int]:
    member, segment, offset = value.split("|")
    return member, int(segment), int(offset)


def _target(config: dict) -> tuple[dict, bytes, str]:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    raw = read_verified_artifact(ROOT, artifact)
    if len(raw) != config["container_size"] or artifact["sha256"] != config["target_sha256"]:
        raise ValueError("ZUN container identity changed")
    rows = [row for row in parse_launcher(raw, expected_sha256=artifact["sha256"])["payloads"]
            if row["name"] == config["member"]]
    if len(rows) != 1:
        raise ValueError("original ZUN -S child is missing or ambiguous")
    row = rows[0]
    if (row["file_start"], row["size"], row["sha256"]) != (
            config["member_start"], config["member_size"], config["member_sha256"]):
        raise ValueError("original ZUN -S child identity changed")
    return row, raw[row["file_start"]:row["file_end"]], artifact["sha256"]


def _verify_segment(name: str, spec: dict, parsed: dict, config: dict,
                    source: bytes, target: bytes) -> dict:
    led_offset = spec["code_ledata_offset"]
    start_com = spec["start_com"]
    expected = bytearray(source)
    resolved = []
    relocation_bytes = set()
    derived_segment_bases = {}
    used_externals = set()
    for fixup in parsed["fixups"]:
        if fixup["segment"] != 1:
            continue
        site = fixup["site"]
        index = site - led_offset
        if (fixup["location_type"] != 1 or index < 0 or index + 2 > len(source)):
            raise ValueError(f"{name} has a non-16-bit or out-of-range CODE relocation")
        relocation_bytes.update((index, index + 1))
        source_word = int.from_bytes(source[index:index + 2], "little")
        target_word = int.from_bytes(target[index:index + 2], "little")
        if fixup["target_method"] == 2:
            if not (1 <= fixup["target_index"] <= len(parsed["externals"])):
                raise ValueError(f"{name} CODE relocation has an invalid EXTDEF index")
            symbol = parsed["externals"][fixup["target_index"] - 1]
            if symbol not in config["external_targets"]:
                raise ValueError(f"{name} external target {symbol} is not pinned")
            target_address = config["external_targets"][symbol]
            used_externals.add(symbol)
        elif fixup["target_method"] == 0:
            symbol = f"{name}:SEG{fixup['target_index']}"
            key = f"{name}:{fixup['target_index']}"
            if key not in config["segment_bases"]:
                raise ValueError(f"{name} internal segment base {key} is not pinned")
            target_address = config["segment_bases"][key]
            derived_segment_bases.setdefault(key, set()).add(target_address)
        else:
            raise ValueError(f"{name} CODE relocation uses an unsupported target method")

        if fixup["relative"]:
            if not ((fixup["frame_method"] == 5 and fixup["frame_index"] is None) or
                    (fixup["frame_method"] == 0 and fixup["frame_index"] == 1)):
                raise ValueError(f"{name} relative relocation uses an unreviewed OMF frame")
            next_ip = start_com + site + 2
            value = (target_address - next_ip + source_word + fixup["displacement"])
            observed_address = (next_ip + (((target_word - source_word -
                               fixup["displacement"] + 0x8000) & 0xFFFF) - 0x8000)) & 0xFFFF
        else:
            if not ((fixup["frame_method"] == 1 and fixup["frame_index"] == 1) or
                    (fixup["frame_method"] == 5 and fixup["frame_index"] is None)):
                raise ValueError(f"{name} absolute relocation uses an unreviewed OMF frame")
            value = target_address + source_word + fixup["displacement"]
            observed_address = (target_word - source_word - fixup["displacement"]) & 0xFFFF
        if observed_address != target_address:
            raise ValueError(f"{name} OMF field resolves to {observed_address:04X}, expected {target_address:04X}")
        value &= 0xFFFF
        expected[index:index + 2] = value.to_bytes(2, "little")
        resolved.append({
            "site": site,
            "led_data_offset": led_offset,
            "symbol": symbol,
            "relative": fixup["relative"],
            "frame_method": fixup["frame_method"],
            "frame_index": fixup["frame_index"],
            "target_method": fixup["target_method"],
            "target_index": fixup["target_index"],
            "displacement": fixup["displacement"],
            "source_addend": source_word,
            "target_address": target_address,
            "observed_target_address": observed_address,
            "resolved_word": value,
        })
    if expected != target:
        raise ValueError(f"{name} target CODE LEDATA is not exact after OMF relocation")
    mismatches = [i for i, (left, right) in enumerate(zip(source, target)) if left != right]
    if not set(mismatches).issubset(relocation_bytes):
        raise ValueError(f"{name} differs outside original OMF FIXUPP fields")
    for key, values in derived_segment_bases.items():
        if values != {config["segment_bases"][key]}:
            raise ValueError(f"{name} internal segment base does not resolve consistently")
    return {
        "source_sha256": digest_bytes(source),
        "target_sha256": digest_bytes(target),
        "relocated_sha256": digest_bytes(bytes(expected)),
        "led_data_offset": led_offset,
        "code_bytes": len(source),
        "segment_bytes": spec["code_segment_size"],
        "nonrelocation_bytes_exact": len(source) - len(relocation_bytes),
        "relocation_count": len(relocation_bytes) // 2,
        "relocation_field_bytes": len(relocation_bytes),
        "relocation_offsets": [f["site"] for f in parsed["fixups"] if f["segment"] == 1],
        "mismatch_offsets": mismatches,
        "resolved_relocations": resolved,
        "external_symbols_referenced": sorted(used_externals),
        "internal_segment_bases": {key: sorted(values) for key, values in derived_segment_bases.items()},
        "raw_exact": source == target,
        "exact_after_omf_relocation": True,
    }


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or
            config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("ZUN stdio CT.LIB source origin/toolchain identity changed")
    toolchain = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surfaces = [row for row in toolchain["surfaces"] if row["id"] == "tc40j-lib"]
    if len(surfaces) != 1:
        raise ValueError("pinned TC4J library tree surface is missing or ambiguous")
    surface = attest_surface(ROOT, surfaces[0])
    if (not surface.get("pass") or surface.get("actual_sha256") != config["library_tree_sha256"] or
            surface.get("file_count") != config["library_tree_file_count"]):
        raise ValueError("complete pinned Borland library tree no longer verifies")

    library = (ROOT / config["library_path"]).read_bytes()
    if digest_bytes(library) != config["library_sha256"]:
        raise ValueError("original CT.LIB archive identity changed")
    members = library_members(library)
    member_by_name = {member.name.lower(): member for member in members}
    if len(member_by_name) != len(members):
        raise ValueError("CT.LIB member names are no longer unique")

    target_row, child, target_artifact_sha256 = _target(config)
    parsed_modules = {}
    module_evidence = []
    external_symbols_referenced = set()
    code_intervals = []
    for spec in config["modules"]:
        name = spec["name"]
        member = member_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"original CT.LIB member {name} is missing")
        parsed = _parse_object(_object_from_member(member))
        parsed_modules[name] = parsed
        formatted = _format_module(parsed)
        for key in ("segments", "groups", "ledatas", "publics", "externals", "fixups_by_segment"):
            if formatted[key] != spec[key]:
                raise ValueError(f"CT.LIB {name} {key} changed: {formatted[key]}")
        if parsed["segments"].get(1) != (spec["code_segment_size"], "_TEXT", "CODE"):
            raise ValueError(f"CT.LIB {name} CODE SEGDEF changed")
        code_ledatas = [row for row in parsed["ledatas"] if row["segment"] == 1]
        if (len(code_ledatas) != 1 or code_ledatas[0]["offset"] != spec["code_ledata_offset"] or
                len(code_ledatas[0]["data"]) != spec["code_size"]):
            raise ValueError(f"CT.LIB {name} CODE LEDATA extent changed")
        source = code_ledatas[0]["data"]
        start = spec["start_com"]
        led_offset = spec["code_ledata_offset"]
        target_start = start + led_offset
        target = child[target_start - 0x100:target_start - 0x100 + len(source)]
        if len(target) != len(source):
            raise ValueError(f"ZUN -S {name} target CODE LEDATA slice is incomplete")
        result = _verify_segment(name, spec, parsed, config, source, target)
        external_symbols_referenced.update(result["external_symbols_referenced"])
        segment_start = start
        segment_end = start + spec["code_segment_size"]
        code_start = target_start
        code_end = target_start + len(source)
        code_file_start = config["member_start"] + target_start - 0x100
        code_intervals.append((code_start, code_end, name))
        module_evidence.append({
            "name": name,
            "segment_start_com": segment_start,
            "segment_end_com": segment_end,
            "code_start_com": code_start,
            "code_end_com": code_end,
            "file_start": code_file_start,
            "code_size": len(source),
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
            "code": result,
        })

    code_intervals.sort()
    expected = [
        (0x0F13, 0x0FD8), (0x0FD8, 0x1069), (0x1069, 0x10AB),
        (0x10AB, 0x1251), (0x1251, 0x1336), (0x1336, 0x1352),
        (0x1352, 0x1477), (0x1477, 0x14CC), (0x14CC, 0x1501),
        (0x1503, 0x1642),
    ]
    actual = [(start, end) for start, end, _ in code_intervals]
    if actual != expected:
        raise ValueError(f"ZUN stdio CT.LIB code intervals changed: {actual}")
    code_bytes = sum(end - start for start, end, _ in code_intervals)
    if code_bytes != config["expected_code_bytes"]:
        raise ValueError("ZUN stdio CT.LIB source-written CODE byte total changed")

    # The leading two bytes of setargv's 321-byte SEGDEF have no LEDATA;
    # the trailing 14 bytes before C0T DATA are also outside this CODE scope.
    gaps = []
    cursor = config["region_start_com"]
    for start, end, _ in code_intervals:
        if cursor < start:
            gaps.append((cursor, start))
        elif cursor > start:
            raise ValueError("ZUN stdio CT.LIB CODE LEDATAs overlap")
        cursor = end
    if cursor < config["region_end_com"]:
        gaps.append((cursor, config["region_end_com"]))
    actual_gaps = [f"0x{start:04X}|0x{end:04X}" for start, end in gaps]
    if actual_gaps != config["expected_unknown_gaps"]:
        raise ValueError(f"ZUN stdio CT.LIB unclaimed holes changed: {actual_gaps}")

    # Resolve every external against its original public boundary. These
    # address anchors validate relocations but do not claim DATA/INITDATA.
    c0t_raw = (ROOT / config["c0t_object_path"]).read_bytes()
    if digest_bytes(c0t_raw) != TINY_CRT_SHA256 or digest_bytes(c0t_raw) != config["c0t_object_sha256"]:
        raise ValueError("original pinned C0T.OBJ identity changed")
    c0t = _parse_object(c0t_raw)
    external_member_names = {
        member for member, _, _ in (_definition(value) for value in config["external_definitions"].values())
        if member != "C0T.OBJ" and member not in parsed_modules
    }
    external_modules = {}
    for name in sorted(external_member_names):
        member = member_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"external CT.LIB member {name} is missing")
        external_modules[name] = _parse_object(_object_from_member(member))

    symbol_definitions = {}
    for symbol, definition in config["external_definitions"].items():
        member_name, segment_index, offset = _definition(definition)
        module = (c0t if member_name == "C0T.OBJ" else
                  parsed_modules.get(member_name, external_modules.get(member_name)))
        if module is None or symbol not in module["publics"]:
            raise ValueError(f"external symbol {symbol} is not public in {member_name}")
        actual_segment, actual_offset = module["publics"][symbol]
        if (actual_segment, actual_offset) != (segment_index, offset):
            raise ValueError(f"external public boundary changed for {symbol}")
        if segment_index not in module["segments"]:
            raise ValueError(f"external public {symbol} refers to a missing segment")
        length, segment_name, class_name = module["segments"][segment_index]
        if member_name in parsed_modules:
            owner_spec = next(row for row in config["modules"] if row["name"] == member_name)
            base = (owner_spec["start_com"] if segment_index == 1 else
                    config["segment_bases"][f"{member_name}:{segment_index}"])
        else:
            key = f"{member_name}:{segment_index}"
            if key not in config["external_segment_bases"] or key not in config["external_segment_specs"]:
                raise ValueError(f"external segment base/spec is missing for {symbol}")
            base = config["external_segment_bases"][key]
            if f"{length}:{segment_name}:{class_name}" != config["external_segment_specs"][key]:
                raise ValueError(f"external segment layout changed for {symbol}")
        address = (base + offset) & 0xFFFF
        if address != config["external_targets"][symbol]:
            raise ValueError(f"external target {symbol} does not resolve to its original public")
        symbol_definitions[symbol] = {
            "member": member_name, "segment": segment_index, "offset": offset,
            "segment_base": base, "address": address,
            "segment_length": length, "segment_name": segment_name,
            "segment_class": class_name,
        }
    if external_symbols_referenced != set(config["external_targets"]):
        raise ValueError("ZUN stdio CT.LIB external-symbol inventory changed")

    # Reject both an instruction mutation and a linked relocation mutation.
    first_spec = config["modules"][0]
    first_parsed = parsed_modules[first_spec["name"]]
    first_source = next(row["data"] for row in first_parsed["ledatas"] if row["segment"] == 1)
    first_target = child[first_spec["start_com"] - 0x100:
                         first_spec["start_com"] - 0x100 + len(first_source)]
    first_fixups = [f for f in first_parsed["fixups"] if f["segment"] == 1]
    first_relocation_bytes = {f["site"] + d for f in first_fixups for d in range(2)}
    nonrel = next(i for i in range(len(first_target)) if i not in first_relocation_bytes)
    negative_instruction = bytearray(first_target)
    negative_instruction[nonrel] ^= 1
    try:
        _verify_segment(first_spec["name"], first_spec, first_parsed, config,
                        first_source, bytes(negative_instruction))
        rejected_instruction = False
    except ValueError:
        rejected_instruction = True
    setargv_spec = next(row for row in config["modules"] if row["name"] == "setargv")
    setargv_parsed = parsed_modules["setargv"]
    setargv_source = next(row["data"] for row in setargv_parsed["ledatas"] if row["segment"] == 1)
    setargv_target_start = setargv_spec["start_com"] + setargv_spec["code_ledata_offset"]
    setargv_target = child[setargv_target_start - 0x100:
                           setargv_target_start - 0x100 + len(setargv_source)]
    setargv_fixups = [f for f in setargv_parsed["fixups"] if f["segment"] == 1]
    negative_relocation = bytearray(setargv_target)
    negative_relocation[setargv_fixups[0]["site"] - setargv_spec["code_ledata_offset"]] ^= 1
    try:
        _verify_segment("setargv", setargv_spec, setargv_parsed, config,
                        setargv_source, bytes(negative_relocation))
        rejected_relocation = False
    except ValueError:
        rejected_relocation = True
    if not rejected_instruction or not rejected_relocation:
        raise ValueError("ZUN stdio CT.LIB negative control failed")

    file_start = config["member_start"] + config["region_start_com"] - 0x100
    file_end = config["member_start"] + config["region_end_com"] - 0x100
    if (file_start, file_end) != (0x18F7, 0x2034):
        raise ValueError("ZUN stdio CT.LIB outer-file interval changed")
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
            "size": config["region_end_com"] - config["region_start_com"],
            "source_written_code_bytes": code_bytes,
            "unknown_gaps": actual_gaps,
            "module_count": len(module_evidence),
        },
        "modules": module_evidence,
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
        raise ValueError("ZUN stdio CT.LIB acceptance is stale or its source/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("ZUN stdio CT.LIB review is bound to the live repository root")
    config = tomllib.loads(CONFIG.read_text())
    record = check()
    if (view.get("size") != config["container_size"] or
            view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("ZUN stdio CT.LIB ownership view identity changed")
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
    print(f"PASS: ZUN -S stdio/path CT.LIB: {record['instruction_bytes']} relocated CODE bytes, "
          f"{record['region']['module_count']} complete OMF members, no authored credit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

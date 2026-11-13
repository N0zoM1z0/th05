#!/usr/bin/env python3
"""Verify ZUN -S resident CT.LIB DATA and the embedded Master 0.23 header string."""
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
from lib.toolchain import attest_surface
from review_zun_early_ctlib import _format_module, _object_from_member, _parse_object

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_resident_data.toml"
PUBLIC = ROOT / "config/zun_resident_data_acceptance.json"
CLAIM_ORIGIN = "reviewed-native-zun-com-reconstruction"
BORLAND_LIBRARY = "Borland Turbo C++ 4.0 CT.LIB"
MASTER_LIBRARY = "Master 0.23"


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


def _verify_data_segment(name: str, spec: dict, parsed: dict, config: dict,
                         source: bytes, target: bytes) -> dict:
    led_offset = spec["data_ledata_offset"]
    start_com = spec["start_com"]
    expected = bytearray(source)
    relocation_bytes = set()
    resolved = []
    for fixup in parsed["fixups"]:
        if fixup["segment"] != 2:
            continue
        site = fixup["site"]
        index = site - led_offset
        if (fixup["location_type"] != 1 or index < 0 or index + 2 > len(source)):
            raise ValueError(f"{name} DATA relocation is not a bounded 16-bit offset")
        if fixup["relative"]:
            raise ValueError(f"{name} DATA relocation unexpectedly uses self-relative addressing")
        if fixup["target_method"] != 0:
            raise ValueError(f"{name} DATA relocation uses an unreviewed target method")
        key = f"{name}:{fixup['target_index']}"
        if key not in config["segment_bases"]:
            raise ValueError(f"{name} DATA relocation target segment {key} is not pinned")
        if not ((fixup["frame_method"] == 1 and fixup["frame_index"] == 1) or
                (fixup["frame_method"] == 5 and fixup["frame_index"] is None)):
            raise ValueError(f"{name} DATA relocation uses an unreviewed OMF frame")
        target_address = config["segment_bases"][key]
        source_word = int.from_bytes(source[index:index + 2], "little")
        target_word = int.from_bytes(target[index:index + 2], "little")
        observed_address = (target_word - source_word - fixup["displacement"]) & 0xFFFF
        if observed_address != target_address:
            raise ValueError(f"{name} DATA relocation resolves to {observed_address:04X}, expected {target_address:04X}")
        value = (target_address + source_word + fixup["displacement"]) & 0xFFFF
        expected[index:index + 2] = value.to_bytes(2, "little")
        relocation_bytes.update((index, index + 1))
        resolved.append({
            "site": site,
            "symbol": key,
            "frame_method": fixup["frame_method"],
            "frame_index": fixup["frame_index"],
            "target_method": fixup["target_method"],
            "target_index": fixup["target_index"],
            "source_addend": source_word,
            "target_address": target_address,
            "observed_target_address": observed_address,
            "resolved_word": value,
        })
    if expected != target:
        raise ValueError(f"{name} DATA LEDATA is not exact after OMF relocation")
    mismatches = [i for i, (left, right) in enumerate(zip(source, target)) if left != right]
    if not set(mismatches).issubset(relocation_bytes):
        raise ValueError(f"{name} DATA differs outside original OMF FIXUPP fields")
    return {
        "source_sha256": digest_bytes(source),
        "target_sha256": digest_bytes(target),
        "relocated_sha256": digest_bytes(bytes(expected)),
        "led_data_offset": led_offset,
        "data_bytes": len(source),
        "segment_bytes": spec["data_segment_size"],
        "nonrelocation_bytes_exact": len(source) - len(relocation_bytes),
        "relocation_count": len(relocation_bytes) // 2,
        "relocation_field_bytes": len(relocation_bytes),
        "relocation_offsets": [f["site"] for f in parsed["fixups"] if f["segment"] == 2],
        "mismatch_offsets": mismatches,
        "resolved_relocations": resolved,
        "raw_exact": source == target,
        "exact_after_omf_relocation": True,
    }


def evidence(config: dict) -> dict:
    if (config.get("schema_version") != 1 or
            config.get("origin") != "pinned-borland-ct-library-original-object" or
            config.get("global_authored_credit") != "vendor-zero" or
            config.get("toolchain_manifest_sha256") != digest_file(ROOT / "config/toolchain.toml")):
        raise ValueError("ZUN resident DATA source origin/toolchain identity changed")
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
    # Reuse the already reviewed code closures as the provenance for original
    # DATA segment addresses; no new address is inferred from a target word.
    import review_zun_early_ctlib as early
    import review_zun_stdio_ctlib as stdio
    early_record = early.check()
    stdio_record = stdio.check()
    anchor_addresses = {
        "_abort:2": 0x1878,
        "atexit:2": early_record["external_symbol_definitions"]["__atexitcnt"]["address"],
        "exit:1": 0x0A32,
        "exit:2": 0x189A,
        "files:2": stdio_record["external_symbol_definitions"]["__streams"]["address"],
        "files2:2": stdio_record["external_symbol_definitions"]["__nfile"]["address"],
        "ioerror:2": 0x1A0C,
    }
    if anchor_addresses != config["segment_bases"]:
        raise ValueError("resident DATA segment anchors disagree with reviewed CODE relocation closures")

    modules = []
    intervals = []
    for spec in config["modules"]:
        name = spec["name"]
        member = member_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"original CT.LIB member {name} is missing")
        parsed = _parse_object(_object_from_member(member))
        formatted = _format_module(parsed)
        for key in ("segments", "groups", "ledatas", "publics", "externals", "fixups_by_segment"):
            if formatted[key] != spec[key]:
                raise ValueError(f"CT.LIB {name} {key} changed: {formatted[key]}")
        if parsed["segments"].get(2) != (spec["data_segment_size"], "_DATA", "DATA"):
            raise ValueError(f"CT.LIB {name} DATA SEGDEF changed")
        ledatas = [row for row in parsed["ledatas"] if row["segment"] == 2]
        if (len(ledatas) != 1 or ledatas[0]["offset"] != spec["data_ledata_offset"] or
                len(ledatas[0]["data"]) != spec["data_size"]):
            raise ValueError(f"CT.LIB {name} DATA LEDATA extent changed")
        source = ledatas[0]["data"]
        start = spec["start_com"]
        target = child[start + spec["data_ledata_offset"] - 0x100:
                       start + spec["data_ledata_offset"] - 0x100 + len(source)]
        if len(target) != len(source):
            raise ValueError(f"ZUN -S {name} DATA slice is incomplete")
        result = _verify_data_segment(name, spec, parsed, config, source, target)
        file_start = config["member_start"] + start + spec["data_ledata_offset"] - 0x100
        intervals.append((start + spec["data_ledata_offset"],
                           start + spec["data_ledata_offset"] + len(source), name))
        modules.append({
            "name": name,
            "start_com": start,
            "end_com": start + spec["data_segment_size"],
            "file_start": file_start,
            "data_size": len(source),
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
            "data": result,
        })

    # The Master 0.23 archive contains four complete DATA members in this
    # resident region. The 93-byte archive-header string is a byte-identical
    # cross-check of the actual `version` OMF DATA member, not a second claim.
    master_path = ROOT / config["master_library_path"]
    master = master_path.read_bytes()
    if (digest_bytes(master) != config["master_library_sha256"] or
            len(master) != config["master_library_size"]):
        raise ValueError("pinned original Master 0.23 library identity changed")
    master_members = library_members(master)
    if len(master_members) != config["master_library_member_count"]:
        raise ValueError("pinned original Master 0.23 member inventory changed")
    master_by_name = {member.name.lower(): member for member in master_members}
    if len(master_by_name) != len(master_members):
        raise ValueError("Master 0.23 member names are no longer unique")

    master_modules = []
    master_parsed = {}
    for spec in config["master_modules"]:
        name = spec["name"]
        member = master_by_name.get(name.lower())
        if member is None:
            raise ValueError(f"original Master 0.23 member {name} is missing")
        parsed = _parse_object(_object_from_member(member))
        master_parsed[name] = parsed
        formatted = _format_module(parsed)
        for key in ("segments", "groups", "ledatas", "publics", "externals", "fixups_by_segment"):
            if formatted[key] != spec[key]:
                raise ValueError(f"Master 0.23 {name} {key} changed: {formatted[key]}")
        if parsed["segments"].get(2) != (spec["data_segment_size"], "_DATA", "DATA"):
            raise ValueError(f"Master 0.23 {name} DATA SEGDEF changed")
        ledatas = [row for row in parsed["ledatas"] if row["segment"] == 2]
        if (len(ledatas) != 1 or ledatas[0]["offset"] != spec["data_ledata_offset"] or
                len(ledatas[0]["data"]) != spec["data_size"]):
            raise ValueError(f"Master 0.23 {name} DATA LEDATA extent changed")
        source = ledatas[0]["data"]
        start = spec["start_com"]
        target = child[start + spec["data_ledata_offset"] - 0x100:
                       start + spec["data_ledata_offset"] - 0x100 + len(source)]
        if len(target) != len(source):
            raise ValueError(f"ZUN -S {name} Master DATA slice is incomplete")
        result = _verify_data_segment(name, spec, parsed, config, source, target)
        file_start = config["member_start"] + start + spec["data_ledata_offset"] - 0x100
        intervals.append((start + spec["data_ledata_offset"],
                           start + spec["data_ledata_offset"] + len(source), name))
        master_modules.append({
            "name": name,
            "start_com": start,
            "end_com": start + spec["data_segment_size"],
            "file_start": file_start,
            "data_size": len(source),
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
            "data": result,
        })

    # The grp object carries an EXTDEF for the version member's public; keep
    # that original cross-member identity in the evidence even though the DATA
    # itself has no FIXUPP relocation.
    version_public = master_parsed["version"]["publics"].get("_Master_Version")
    if version_public != (2, 20) or "_Master_Version" not in master_parsed["grp"]["externals"]:
        raise ValueError("Master grp/version public-symbol relationship changed")
    master_symbol_address = (config["master_modules"][0]["start_com"] + version_public[1]) & 0xFFFF

    master_source = master[config["master_header_offset"]:
                          config["master_header_offset"] + config["master_header_size"]]
    master_start = config["master_header_com_start"]
    master_target = child[master_start - 0x100:master_start - 0x100 + len(master_source)]
    version_data = next(row["data"] for row in master_parsed["version"]["ledatas"]
                        if row["segment"] == 2)
    if (len(master_source) != 93 or master_source != master_target or
            master_source != version_data or master_source[-1:] != b"\0" or
            not master_source.startswith(config["master_header_text"].encode("ascii"))):
        raise ValueError("Master 0.23 header string and version OMF DATA member are not exact")
    master_file_start = config["member_start"] + master_start - 0x100

    intervals.sort()
    if len(intervals) != 10:
        raise ValueError("unexpected CT.LIB/Master resident DATA interval count")
    expected = [
        (0x17FE, 0x185B), (0x185C, 0x1867), (0x1868, 0x1872),
        (0x1872, 0x1876), (0x1878, 0x1897), (0x1898, 0x189A),
        (0x189A, 0x18A0), (0x18A0, 0x19E0), (0x19E0, 0x1A0A),
        (0x1A0C, 0x1A67),
    ]
    if [(a, b) for a, b, _ in intervals] != expected:
        raise ValueError(f"resident DATA source intervals changed: {intervals}")
    total = sum(b - a for a, b, _ in intervals)
    if total != config["expected_total_data_bytes"]:
        raise ValueError("resident DATA source-written byte total changed")
    gaps = []
    cursor = config["resident_data_start_com"]
    for start, end, _ in intervals:
        if cursor < start:
            gaps.append((cursor, start))
        elif cursor > start:
            raise ValueError("resident DATA source intervals overlap")
        cursor = end
    if cursor < config["resident_data_end_com"]:
        gaps.append((cursor, config["resident_data_end_com"]))
    gap_strings = [f"0x{a:04X}|0x{b:04X}" for a, b in gaps]
    if gap_strings != config["expected_unknown_gaps"]:
        raise ValueError(f"resident DATA unclaimed gaps changed: {gap_strings}")

    # Reject a plain initialized-byte mutation and a relocated-pointer mutation.
    first_spec = config["modules"][0]
    first_module = next(row for row in modules if row["name"] == first_spec["name"])
    first_parsed = _parse_object(_object_from_member(member_by_name[first_spec["name"]]))
    first_source = next(row["data"] for row in first_parsed["ledatas"] if row["segment"] == 2)
    first_target = child[first_spec["start_com"] - 0x100:
                          first_spec["start_com"] - 0x100 + len(first_source)]
    negative_data = bytearray(first_target)
    negative_data[0] ^= 1
    try:
        _verify_data_segment(first_spec["name"], first_spec, first_parsed, config,
                             first_source, bytes(negative_data))
        rejected_data = False
    except ValueError:
        rejected_data = True
    files_spec = next(row for row in config["modules"] if row["name"] == "files")
    files_parsed = _parse_object(_object_from_member(member_by_name["files"]))
    files_source = next(row["data"] for row in files_parsed["ledatas"] if row["segment"] == 2)
    files_target = child[files_spec["start_com"] - 0x100:
                         files_spec["start_com"] - 0x100 + len(files_source)]
    files_fixup = next(row for row in files_parsed["fixups"] if row["segment"] == 2)
    negative_relocation = bytearray(files_target)
    negative_relocation[files_fixup["site"] - files_spec["data_ledata_offset"]] ^= 1
    try:
        _verify_data_segment("files", files_spec, files_parsed, config,
                             files_source, bytes(negative_relocation))
        rejected_relocation = False
    except ValueError:
        rejected_relocation = True
    if not rejected_data or not rejected_relocation:
        raise ValueError("resident DATA negative control failed")

    return {
        "schema_version": 1,
        "kind": "bounded-zun-resident-vendor-initialized-data-review",
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
        "origin": config["origin"],
        "master_source_origin": "pinned-master-library-original-binary",
        "master_library_sha256": digest_bytes(master),
        "master_library_size": len(master),
        "master_library_member_count": len(master_members),
        "master_header": {
            "file_start": master_file_start,
            "com_start": master_start,
            "source_offset": config["master_header_offset"],
            "size": len(master_source),
            "source_sha256": digest_bytes(master_source),
            "target_sha256": digest_bytes(master_target),
            "raw_exact": True,
            "origin": "pinned-master-library-original-binary",
        },
        "ctlib_modules": modules,
        "master_modules": master_modules,
        "master_external_symbol_definitions": {
            "_Master_Version": {"member": "version", "segment": 2, "offset": version_public[1],
                                "address": master_symbol_address},
        },
        "segment_bases": config["segment_bases"],
        "resident_data": {
            "start_com": config["resident_data_start_com"],
            "end_com": config["resident_data_end_com"],
            "size": config["resident_data_end_com"] - config["resident_data_start_com"],
            "source_written_bytes": total,
            "ctlib_data_bytes": sum(row["data_size"] for row in modules),
            "master_data_bytes": sum(row["data_size"] for row in master_modules),
            "master_header_crosscheck_bytes": len(master_source),
            "unknown_gaps": gap_strings,
        },
        "negative_control": {
            "nonrelocation_data_flip_rejected": rejected_data,
            "resolved_relocation_flip_rejected": rejected_relocation,
        },
        "authored_credit": 0,
        "instruction_bytes": 0,
    }


def check() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    expected = evidence(config)
    actual = json.loads(PUBLIC.read_text())
    if actual != expected:
        raise ValueError("resident DATA acceptance is stale or its source/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    root = root.resolve()
    if root != ROOT.resolve():
        raise ValueError("resident DATA review is bound to the live repository root")
    config = tomllib.loads(CONFIG.read_text())
    record = check()
    if (view.get("size") != config["container_size"] or
            view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("resident DATA ownership view identity changed")
    claims = []
    for module in record["ctlib_modules"]:
        claims.append({
            "start": module["file_start"],
            "end": module["file_start"] + module["data_size"],
            "kind": "verified-vendor-initialized-data",
            "unit": f"borland-ctlib-{module['name']}-data",
            "origin": CLAIM_ORIGIN,
            "source_origin": config["origin"],
            "instruction_bytes": 0,
            "authored_credit": 0,
            "content_kind": "library-initialized-data",
            "library": BORLAND_LIBRARY,
            "member": module["name"],
        })
    for module in record["master_modules"]:
        claims.append({
            "start": module["file_start"],
            "end": module["file_start"] + module["data_size"],
            "kind": "verified-vendor-initialized-data",
            "unit": f"master-023-{module['name']}-data",
            "origin": CLAIM_ORIGIN,
            "source_origin": record["master_source_origin"],
            "instruction_bytes": 0,
            "authored_credit": 0,
            "content_kind": "library-initialized-data",
            "library": MASTER_LIBRARY,
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
        PUBLIC.write_text(json.dumps(evidence(config), indent=2) + "\n")
    record = check()
    print(f"PASS: ZUN -S resident DATA: {record['resident_data']['source_written_bytes']} vendor DATA bytes "
          f"across {len(record['ctlib_modules'])} CT.LIB + {len(record['master_modules'])} Master OMF segments; zero authored credit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

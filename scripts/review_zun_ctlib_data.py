#!/usr/bin/env python3
"""Verify file-backed CT.LIB DATA/INITDATA segments in the remaining ZUN -S gap."""
from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

from lib.borland_library import library_members
from lib.pc98 import digest_bytes, digest_file
from review_zun_early_ctlib import (
    CLAIM_ORIGIN,
    LIBRARY_NAME,
    ROOT,
    _load_target,
    _object_from_member,
    _parse_object,
    check as check_early,
)
from review_zun_stdio_ctlib import check as check_stdio

CONFIG = ROOT / "config/zun_ctlib_data.toml"
PUBLIC = ROOT / "config/zun_ctlib_data_acceptance.json"
DATA_CLASSES = {"DATA", "INITDATA", "CONST", "FAR_DATA", "FAR_CONST"}


def _segment_bytes(parsed: dict, segment_index: int) -> tuple[bytes, list[tuple[int, int]]]:
    """Materialize the OMF segment image and retain exact LEDATA-written spans."""
    length = parsed["segments"][segment_index][0]
    data = bytearray(length)
    written = bytearray(length)
    for row in parsed["ledatas"]:
        if row["segment"] != segment_index:
            continue
        start, end = row["offset"], row["offset"] + len(row["data"])
        if start < 0 or end > length or end < start:
            raise ValueError("CT.LIB DATA LEDATA escapes its SEGDEF")
        if any(written[start:end]):
            raise ValueError("CT.LIB DATA LEDATA records overlap")
        data[start:end] = row["data"]
        written[start:end] = b"\x01" * (end - start)
    spans = []
    cursor = 0
    while cursor < length:
        if not written[cursor]:
            cursor += 1
            continue
        end = cursor + 1
        while end < length and written[end]:
            end += 1
        spans.append((cursor, end))
        cursor = end
    return bytes(data), spans


def _complement(spans: list[tuple[int, int]], size: int) -> list[tuple[int, int]]:
    output = []
    cursor = 0
    for start, end in sorted(spans):
        start, end = max(0, start), min(size, end)
        if start > cursor:
            output.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < size:
        output.append((cursor, size))
    return output


def _observed_target(base: int, source: bytes, target: bytes, fixup: dict) -> int:
    site = fixup["site"]
    if fixup["location_type"] != 1 or site < 0 or site + 2 > len(source):
        raise ValueError("CT.LIB data segment contains a non-16-bit/out-of-range relocation")
    source_word = int.from_bytes(source[site:site + 2], "little")
    target_word = int.from_bytes(target[site:site + 2], "little")
    raw_delta = target_word - source_word - fixup["displacement"]
    if fixup["relative"]:
        signed_delta = ((raw_delta + 0x8000) & 0xFFFF) - 0x8000
        return (base + site + 2 + signed_delta) & 0xFFFF
    return raw_delta & 0xFFFF


def _verify_segment(member_name: str, segment_index: int, base: int,
                    source: bytes, target: bytes, initialized_spans: list[tuple[int, int]],
                    fixups: list[dict], externals: list[str],
                    known_symbols: dict, known_bases: dict) -> dict:
    if len(source) < len(target):
        raise ValueError(f"{member_name} DATA source image is shorter than the file-backed target")
    source = source[:len(target)]
    initialized_spans = [(a, min(b, len(target))) for a, b in initialized_spans
                         if a < len(target) and min(b, len(target)) > a]
    uninitialized_spans = _complement(initialized_spans, len(target))
    for start, end in uninitialized_spans:
        if any(target[start:end]):
            raise ValueError(f"{member_name} uninitialized DATA tail is not zero-filled in ZUN -S")

    external_targets = {}
    internal_bases = {}
    relocation_bytes = set()
    for fixup in fixups:
        site = fixup["site"]
        if fixup["location_type"] != 1 or site < 0 or site + 2 > len(target):
            raise ValueError(f"{member_name} DATA relocation escapes the file-backed segment")
        if not any(start <= site and site + 2 <= end for start, end in initialized_spans):
            raise ValueError(f"{member_name} DATA relocation is outside source LEDATA")
        if fixup["relative"]:
            if not ((fixup["frame_method"] == 5 and fixup["frame_index"] is None) or
                    (fixup["frame_method"] == 0 and fixup["frame_index"] == 1)):
                raise ValueError(f"{member_name} relative DATA relocation uses an unreviewed OMF frame")
        elif not ((fixup["frame_method"] == 1 and fixup["frame_index"] == 1) or
                  (fixup["frame_method"] == 5 and fixup["frame_index"] is None)):
            raise ValueError(f"{member_name} absolute DATA relocation uses an unreviewed OMF frame")
        observed = _observed_target(base, source, target, fixup)
        if fixup["target_method"] == 2:
            if not (1 <= fixup["target_index"] <= len(externals)):
                raise ValueError(f"{member_name} DATA has an invalid EXTDEF index")
            symbol = externals[fixup["target_index"] - 1]
            if symbol not in known_symbols:
                raise ValueError(f"{member_name} DATA external {symbol} has no independently accepted public")
            target_address = known_symbols[symbol]
            external_targets[symbol] = observed
        elif fixup["target_method"] == 0:
            symbol = f"{member_name}:SEG{fixup['target_index']}"
            key = f"{member_name.lower()}:{fixup['target_index']}"
            if key not in known_bases:
                raise ValueError(f"{member_name} DATA internal target {key} has no accepted CODE/DATA anchor")
            target_address = known_bases[key]
            internal_bases[key] = observed
        else:
            raise ValueError(f"{member_name} DATA uses an unsupported OMF target method")
        if observed != target_address:
            raise ValueError(f"{member_name} DATA relocation resolves to {observed:04X}, expected {target_address:04X}")
        relocation_bytes.update((site, site + 1))

    expected = bytearray(source)
    resolved = []
    for fixup in fixups:
        site = fixup["site"]
        source_word = int.from_bytes(source[site:site + 2], "little")
        if fixup["target_method"] == 2:
            symbol = externals[fixup["target_index"] - 1]
            target_address = known_symbols[symbol]
        else:
            symbol = f"{member_name}:SEG{fixup['target_index']}"
            target_address = known_bases[f"{member_name.lower()}:{fixup['target_index']}"]
        if fixup["relative"]:
            value = target_address - (base + site + 2) + source_word + fixup["displacement"]
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
            "observed_target_address": target_address,
            "resolved_word": value,
        })
    if bytes(expected) != target:
        raise ValueError(f"{member_name} DATA segment {segment_index} is not exact after OMF relocation")
    mismatches = [index for index, (left, right) in enumerate(zip(source, target)) if left != right]
    if not set(mismatches).issubset(relocation_bytes):
        raise ValueError(f"{member_name} DATA differs outside OMF FIXUPP fields")
    return {
        "source_sha256": digest_bytes(source),
        "target_sha256": digest_bytes(target),
        "relocated_sha256": digest_bytes(bytes(expected)),
        "file_backed_bytes": len(target),
        "initialized_spans": [[a, b] for a, b in initialized_spans],
        "uninitialized_spans": [[a, b] for a, b in uninitialized_spans],
        "initialized_bytes": sum(b - a for a, b in initialized_spans),
        "uninitialized_bytes": sum(b - a for a, b in uninitialized_spans),
        "nonrelocation_bytes_exact": len(target) - len(relocation_bytes),
        "relocation_count": len(fixups),
        "relocation_offsets": [fixup["site"] for fixup in fixups],
        "mismatch_offsets": mismatches,
        "resolved_relocations": resolved,
        "exact_after_omf_relocation": True,
    }


def _known_maps(early: dict, early_config: dict, stdio: dict) -> tuple[dict, dict]:
    symbols = {}
    bases = {}
    for record in (early, stdio):
        for symbol, details in record["external_symbol_definitions"].items():
            address = details["address"]
            if symbol in symbols and symbols[symbol] != address:
                raise ValueError(f"accepted code reviewers disagree on {symbol}")
            symbols[symbol] = address
            bases[f"{details['member'].lower()}:{details['segment']}"] = details["segment_base"]
        for key, base in record.get("internal_segment_bases", {}).items():
            bases[key.lower()] = base
        for key, base in record.get("inferred_segment_bases", {}).items():
            bases[key.lower()] = base
        for module in record["modules"]:
            code_base = module.get("start_com", module.get("segment_start_com"))
            if code_base is not None:
                bases[f"{module['name'].lower()}:1"] = code_base
    for key, base in early_config["segment_bases"].items():
        bases[key.lower()] = base
    for key, base in early_config["external_segment_bases"].items():
        bases[key.lower()] = base
    return symbols, bases


def _match_segment(member_name: str, segment_index: int, length: int,
                   source: bytes, initialized_spans: list[tuple[int, int]],
                   fixups: list[dict], intervals: list[list[int]], child: bytes,
                   known_base: int | None, symbol_anchor: int | None,
                   known_symbols: dict, known_bases: dict,
                   externals: list[str]) -> tuple[int | None, int, list[int]]:
    file_end_com = 0x100 + len(child)
    anchored_fixup = False
    for fixup in fixups:
        if fixup["target_method"] == 0:
            key = f"{member_name.lower()}:{fixup['target_index']}"
            anchored_fixup |= key in known_bases
        elif fixup["target_method"] == 2 and 1 <= fixup["target_index"] <= len(externals):
            anchored_fixup |= externals[fixup["target_index"] - 1] in known_symbols
    if known_base is None and symbol_anchor is None and not anchored_fixup:
        return None, 0, []
    positions = [known_base if known_base is not None else symbol_anchor] if (
        known_base is not None or symbol_anchor is not None) else [
            base for low, high in intervals for base in range(low, high)
        ]
    matches = []
    match_sizes = {}
    for base in positions:
        interval = next(((low, high) for low, high in intervals if low <= base < high), None)
        if interval is None:
            continue
        available = min(length, file_end_com - base, interval[1] - base)
        if available <= 0 or any(end > available for _, end in initialized_spans):
            continue
        if any(fixup["site"] + 2 > available for fixup in fixups):
            continue
        target = child[base - 0x100:base - 0x100 + available]
        if len(target) != available:
            continue
        source_available = source[:available]
        uninitialized = _complement(initialized_spans, available)
        if any(any(target[start:end]) for start, end in uninitialized):
            continue
        relocation_bytes = {fixup["site"] + delta for fixup in fixups for delta in range(2)}
        mismatches = {index for index, (left, right) in enumerate(zip(source_available, target))
                      if left != right}
        if mismatches.issubset(relocation_bytes):
            matches.append(base)
            match_sizes[base] = available
    if len(matches) == 1:
        return matches[0], match_sizes[matches[0]], matches
    return None, 0, matches


def evidence(config: dict) -> dict:
    early = check_early()
    stdio = check_stdio()
    early_config = tomllib.loads((ROOT / "config/zun_early_ctlib.toml").read_text())
    if config.get("schema_version") != 1:
        raise ValueError("unsupported ZUN CT.LIB data-review schema")
    target_row, child, target_sha256 = _load_target(early_config)
    library_path = ROOT / early_config["library_path"]
    library = library_path.read_bytes()
    if digest_bytes(library) != early["library_sha256"]:
        raise ValueError("CT.LIB archive changed since the accepted code reviews")
    members = library_members(library)
    known_symbols, known_bases = _known_maps(early, early_config, stdio)

    full_modules = {}
    for member in members:
        try:
            parsed = _parse_object(_object_from_member(member))
        except ValueError:
            continue
        if any(class_name in DATA_CLASSES and length > 0
               for length, _seg_name, class_name in parsed["segments"].values()):
            full_modules[member.name] = parsed

    candidates = []
    ambiguous = []
    for member_name, parsed in full_modules.items():
        for segment_index, segment in parsed["segments"].items():
            length, segment_name, class_name = segment
            if class_name not in DATA_CLASSES or length <= 0:
                continue
            rows = [row for row in parsed["ledatas"] if row["segment"] == segment_index]
            if not rows:
                continue
            source, initialized_spans = _segment_bytes(parsed, segment_index)
            fixups = [fixup for fixup in parsed["fixups"] if fixup["segment"] == segment_index]
            if any(fixup["location_type"] != 1 for fixup in fixups):
                continue
            key = f"{member_name.lower()}:{segment_index}"
            known_base = known_bases.get(key)
            anchors = []
            for symbol, (public_segment, offset) in parsed["publics"].items():
                if public_segment == segment_index and symbol in known_symbols:
                    anchors.append((known_symbols[symbol] - offset) & 0xFFFF)
            if anchors and len(set(anchors)) != 1:
                raise ValueError(f"{member_name} DATA public symbols disagree on segment base")
            symbol_anchor = anchors[0] if anchors else None
            if known_base is not None and symbol_anchor is not None and known_base != symbol_anchor:
                raise ValueError(f"{member_name} DATA known segment base disagrees with PUBLIC anchor")
            if known_base is not None and not any(low <= known_base < high for low, high in config["intervals"]):
                continue
            if symbol_anchor is not None and not any(low <= symbol_anchor < high for low, high in config["intervals"]):
                continue
            base, available, matches = _match_segment(
                member_name, segment_index, length, source, initialized_spans,
                fixups, config["intervals"], child, known_base, symbol_anchor,
                known_symbols, known_bases, parsed["externals"])
            if base is None:
                if len(matches) > 1:
                    ambiguous.append({"member": member_name, "segment": segment_index,
                                      "length": length, "candidate_bases": matches[:64]})
                elif known_base is not None or symbol_anchor is not None:
                    raise ValueError(f"pinned {member_name}:{segment_index} DATA does not match target")
                continue
            target = child[base - 0x100:base - 0x100 + available]
            file_fixups = [fixup for fixup in fixups if fixup["site"] + 2 <= available]
            result = _verify_segment(member_name, segment_index, base, source, target,
                                     initialized_spans, file_fixups, parsed["externals"],
                                     known_symbols, known_bases)
            for symbol, (public_segment, offset) in parsed["publics"].items():
                if public_segment == segment_index and symbol in known_symbols:
                    if ((base + offset) & 0xFFFF) != known_symbols[symbol]:
                        raise ValueError(f"{member_name} DATA PUBLIC {symbol} has the wrong address")
            candidates.append({
                "member": member_name,
                "segment": segment_index,
                "segment_length": length,
                "segment_name": segment_name,
                "segment_class": class_name,
                "base_com": base,
                "segment_end_com": base + length,
                "end_com": base + available,
                "file_start": early_config["member_start"] + base - 0x100,
                "file_backed_bytes": available,
                "program_records_sha256": digest_bytes(next(m.program_records for m in members if m.name == member_name)),
                "object_sha256": parsed["object_sha256"],
                "fixup_records_sha256": digest_bytes(b"".join(parsed["fixup_records"])),
                "segments": [f"{index}|{seg_length}|{seg_name}|{seg_class}"
                             for index, (seg_length, seg_name, seg_class) in parsed["segments"].items()],
                "groups": [f"{index}|{group_name}|{','.join(str(x) for x in group_members)}"
                           for index, (group_name, group_members) in parsed["groups"].items()],
                "ledatas": [f"{row['segment']}|{row['offset']}|{len(row['data'])}"
                            for row in parsed["ledatas"]],
                "publics": [f"{symbol}|{seg}|{offset}"
                            for symbol, (seg, offset) in parsed["publics"].items()],
                "externals": parsed["externals"],
                "fixups_by_segment": [
                    f"{seg}|{','.join(str(f['site']) for f in parsed['fixups'] if f['segment'] == seg)}"
                    for seg in dict.fromkeys(f["segment"] for f in parsed["fixups"])
                ],
                "verification": result,
            })

    candidates.sort(key=lambda row: (row["base_com"], row["end_com"], row["member"], row["segment"]))
    for previous, current in zip(candidates, candidates[1:]):
        if current["base_com"] < previous["end_com"]:
            raise ValueError("CT.LIB initialized/uninitialized DATA segments overlap in the target")
    identities = {(row["member"], row["segment"]) for row in candidates}
    if len(identities) != len(candidates):
        raise ValueError("CT.LIB DATA segment was matched more than once")

    covered = {index: [] for index in range(len(config["intervals"]))}
    for row in candidates:
        for index, (low, high) in enumerate(config["intervals"]):
            if low <= row["base_com"] and row["end_com"] <= high:
                covered[index].append((row["base_com"], row["end_com"]))
                break
    gaps = []
    for index, (low, high) in enumerate(config["intervals"]):
        cursor = low
        for start, end in sorted(covered[index]):
            if start > cursor:
                gaps.append([cursor, start])
            cursor = max(cursor, end)
        if cursor < high:
            gaps.append([cursor, high])

    first = candidates[0] if candidates else None
    if first is None:
        raise ValueError("no original CT.LIB initialized-data segments matched the configured interval")
    first_module = full_modules[first["member"]]
    first_source, first_spans = _segment_bytes(first_module, first["segment"])
    first_target = child[first["base_com"] - 0x100:first["end_com"] - 0x100]
    first_fixups = [f for f in first_module["fixups"]
                    if f["segment"] == first["segment"] and f["site"] + 2 <= len(first_target)]
    relocation_bytes = {fixup["site"] + delta for fixup in first_fixups for delta in range(2)}
    nonrelocation = next((index for index in range(len(first_target)) if index not in relocation_bytes), None)
    rejected_data = False
    if nonrelocation is not None:
        bad = bytearray(first_target)
        bad[nonrelocation] ^= 1
        try:
            _verify_segment(first["member"], first["segment"], first["base_com"],
                            first_source, bytes(bad), first_spans, first_fixups,
                            first_module["externals"], known_symbols, known_bases)
        except ValueError:
            rejected_data = True
    relocation_row = next(((row, fixup) for row in candidates
                           for fixup in full_modules[row["member"]]["fixups"]
                           if fixup["segment"] == row["segment"] and fixup["site"] + 2 <= row["file_backed_bytes"]), None)
    rejected_relocation = False
    if relocation_row is not None:
        row, fixup = relocation_row
        module = full_modules[row["member"]]
        data_source, data_spans = _segment_bytes(module, row["segment"])
        data_target = child[row["base_com"] - 0x100:row["end_com"] - 0x100]
        data_fixups = [item for item in module["fixups"]
                       if item["segment"] == row["segment"] and item["site"] + 2 <= len(data_target)]
        bad = bytearray(data_target)
        bad[fixup["site"]] ^= 1
        try:
            _verify_segment(row["member"], row["segment"], row["base_com"],
                            data_source, bytes(bad), data_spans, data_fixups,
                            module["externals"], known_symbols, known_bases)
        except ValueError:
            rejected_relocation = True
    if not rejected_data:
        raise ValueError("CT.LIB data non-relocation mutation was not rejected")
    if relocation_row is not None and not rejected_relocation:
        raise ValueError("CT.LIB data relocation mutation was not rejected")

    return {
        "schema_version": 1,
        "kind": "bounded-zun-borland-ctlib-initialized-data-ownership-review",
        "manifest_sha256": digest_file(CONFIG),
        "early_acceptance_sha256": digest_file(ROOT / "config/zun_early_ctlib_acceptance.json"),
        "stdio_acceptance_sha256": digest_file(ROOT / "config/zun_stdio_ctlib_acceptance.json"),
        "library_sha256": early["library_sha256"],
        "library_tree_sha256": early["library_tree_sha256"],
        "target_artifact_sha256": target_sha256,
        "member": early["member"],
        "member_start": target_row["file_start"],
        "member_size": target_row["size"],
        "member_sha256": target_row["sha256"],
        "intervals": config["intervals"],
        "segments": candidates,
        "verified_data_bytes": sum(row["file_backed_bytes"] for row in candidates),
        "initialized_data_bytes": sum(row["verification"]["initialized_bytes"] for row in candidates),
        "uninitialized_storage_bytes": sum(row["verification"]["uninitialized_bytes"] for row in candidates),
        "unclassified_bytes": sum(end - start for start, end in gaps),
        "unclassified_intervals": gaps,
        "ambiguous_candidates": ambiguous,
        "negative_control": {
            "nonrelocation_data_flip_rejected": rejected_data,
            "relocation_word_flip_rejected": rejected_relocation if relocation_row else None,
        },
        "authored_credit": 0,
    }


def check() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    expected = evidence(config)
    actual = json.loads(PUBLIC.read_text())
    if actual != expected:
        raise ValueError("ZUN CT.LIB data acceptance is stale or its OMF/target proof changed")
    return expected


def reviewed_claims(root: Path, view: dict, *, verify_targets: bool = False):
    if root.resolve() != ROOT.resolve():
        raise ValueError("ZUN CT.LIB data review is bound to the live repository root")
    record = check()
    if (view.get("size") != 18116 or view.get("sha256") != record["target_artifact_sha256"]):
        raise ValueError("ZUN CT.LIB data ownership view identity changed")
    claims = []
    for segment in record["segments"]:
        for start, end in segment["verification"]["initialized_spans"]:
            claims.append({
                "start": segment["file_start"] + start,
                "end": segment["file_start"] + end,
                "kind": "verified-vendor-initialized-data",
                "unit": f"borland-ctlib-data-{segment['member']}-seg{segment['segment']}",
                "origin": CLAIM_ORIGIN,
                "source_origin": "pinned-borland-ct-library-original-object",
                "instruction_bytes": 0,
                "authored_credit": 0,
                "content_kind": "library-initialized-data",
                "library": LIBRARY_NAME,
                "member": segment["member"],
                "segment": segment["segment"],
                "segment_name": segment["segment_name"],
                "segment_class": segment["segment_class"],
            })
        for start, end in segment["verification"]["uninitialized_spans"]:
            claims.append({
                "start": segment["file_start"] + start,
                "end": segment["file_start"] + end,
                "kind": "reviewed-uninitialized-vendor-storage",
                "unit": f"borland-ctlib-storage-{segment['member']}-seg{segment['segment']}",
                "origin": CLAIM_ORIGIN,
                "source_origin": "pinned-borland-ct-library-original-object",
                "instruction_bytes": 0,
                "authored_credit": 0,
                "content_kind": "original-OMF-uninitialized-segment",
                "library": LIBRARY_NAME,
                "member": segment["member"],
                "segment": segment["segment"],
                "segment_name": segment["segment_name"],
                "segment_class": segment["segment_class"],
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
    print(f"PASS: ZUN CT.LIB initialized data: {record['verified_data_bytes']} file-backed bytes "
          f"({record['initialized_data_bytes']} initialized, {record['uninitialized_storage_bytes']} reserved) "
          f"across {len(record['segments'])} exact OMF segments; {record['unclassified_bytes']} bytes remain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

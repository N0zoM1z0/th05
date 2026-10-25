#!/usr/bin/env python3
"""Replay symbolic text-renderer ASM DATA separately from C/C++ acceptance."""
from __future__ import annotations

import argparse
import fcntl
import json
from pathlib import Path
import re
import shutil
import tomllib

from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_bytes, digest_file, parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain, static_toolchain, validate_full_toolchain
from lib.unit_context import UnitContext, freeze_target_view, load_unit_target, validate_public_target_view
from lib.unit_oracle import compare_unit, map_publics, relative_fixups

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/text_fx_data.toml"
PUBLIC = ROOT / "config/text_fx_data_acceptance.json"
ORIGIN = "inferred-original-handwritten-assembly"
SCOPES = (("dispatch", "_DATA", 28), ("state", "TEXT_FX_STATE_DATA", 4))
MUTATIONS = {
    "dispatch": ("dw glyph_weight_normal - (grppsafx_glyph_func_1 + 2)",
                 "dw glyph_weight_heavy - (grppsafx_glyph_func_1 + 2)"),
    "state": ("_graph_putsa_fx_spacing dw 16", "_graph_putsa_fx_spacing dw 17"),
}
ASSEMBLER = ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t"]
LINK_RESPONSE = b"-c -s -E bindings.obj tfxdata.obj, units.exe, units.map,\r\n"
PROOF_INPUTS = (
    "scripts/replay_text_fx_data.py", "scripts/lib/omf.py", "scripts/lib/pc98.py",
    "scripts/lib/reference_build.py", "scripts/lib/replay_toolchain.py",
    "scripts/lib/unit_context.py", "scripts/lib/unit_oracle.py",
    "scripts/lib/unit_extents.py", "config/targets.toml", "config/toolchain.toml",
)


def inputs(config: dict) -> list[dict]:
    paths = {str(CONFIG.relative_to(ROOT)), config["source"], *PROOF_INPUTS}
    for profile in config["profiles"].values():
        paths.update((profile["bindings"], profile["symbols"]))
    return [{"path": path, "sha256": digest_file(ROOT / path)} for path in sorted(paths)]


def mutate(source: bytes, scope: str | None) -> bytes:
    if scope is None:
        return source
    before, after = (value.encode("ascii") for value in MUTATIONS[scope])
    if source.count(before) != 1:
        raise ValueError("ASM mutation must have one exact semantic anchor")
    return source.replace(before, after)


def index(data: bytes, cursor: int) -> tuple[int, int]:
    if cursor >= len(data):
        raise ValueError("truncated OMF index")
    first = data[cursor]
    cursor += 1
    if first & 0x80:
        if cursor >= len(data):
            raise ValueError("truncated long OMF index")
        return ((first & 0x7F) << 8) | data[cursor], cursor + 1
    return first, cursor


def asm_scopes(raw: bytes) -> dict:
    """Require complete real DATA SEGDEFs, with no other initialized payload."""
    description = describe_omf(raw)
    if description["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("expected pinned TASM producer, never a C/C++ producer")
    names, segments = [""], [None]
    records = parse_omf(raw)
    forbidden = {"LIDATA", "LIDATA32", "COMDAT", "COMDAT32", "BAKPAT", "BAKPAT32",
                 "LEDATA32", "SEGDEF32", "FIXUPP", "FIXUPP32"}
    for record in records:
        if record.name in forbidden:
            raise ValueError("unsupported ASM DATA transform or unresolved fixup")
        data = record.data
        if record.name == "LNAMES":
            cursor = 0
            while cursor < len(data):
                length = data[cursor]
                cursor += 1
                if cursor + length > len(data):
                    raise ValueError("truncated LNAMES")
                names.append(data[cursor:cursor + length].decode("cp437"))
                cursor += length
        elif record.name == "SEGDEF":
            if len(data) < 6 or not data[0] & 0xE0 or data[0] & 2:
                raise ValueError("unsupported ASM DATA SEGDEF")
            name, cursor = index(data, 3)
            cl, cursor = index(data, cursor)
            overlay, cursor = index(data, cursor)
            if (cursor != len(data) or not 0 < name < len(names)
                    or not 0 < cl < len(names) or not 0 <= overlay < len(names)):
                raise ValueError("invalid SEGDEF names")
            segments.append((names[name], names[cl], int.from_bytes(data[1:3], "little")))
    result, owners = {}, {}
    for scope, name, size in SCOPES:
        matches = [(i, seg) for i, seg in enumerate(segments) if seg and seg[0] == name]
        if len(matches) != 1 or matches[0][1][1:] != ("DATA", size):
            raise ValueError("ASM must supply one complete reviewed DATA SEGDEF per scope")
        si = matches[0][0]
        owners[si] = scope
        result[scope] = {"segment": name, "size": size, "chunks": [], "covered": bytearray(size)}
    for si, seg in enumerate(segments):
        if seg and seg[2] and si not in owners:
            raise ValueError("unreviewed initialized or reserved contribution in ASM source")
    for record in records:
        if record.name != "LEDATA":
            continue
        si, cursor = index(record.data, 0)
        if si not in owners or cursor + 2 > len(record.data):
            raise ValueError("LEDATA outside reviewed ASM scope")
        scope = result[owners[si]]
        start = int.from_bytes(record.data[cursor:cursor + 2], "little")
        payload = record.data[cursor + 2:]
        end = start + len(payload)
        if not payload or end > scope["size"] or any(scope["covered"][start:end]):
            raise ValueError("ASM DATA overlaps or escapes complete SEGDEF")
        scope["covered"][start:end] = b"\1" * len(payload)
        scope["chunks"].append({"offset": start, "size": len(payload), "sha256": digest_bytes(payload)})
    for scope in result.values():
        if not all(scope.pop("covered")):
            raise ValueError("unwritten ASM DATA byte")
    return result


def map_scope(path: Path, segment: str, ds_frame: int) -> tuple[int, int]:
    pattern = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
                         r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)", re.I)
    found = []
    for line in path.read_text(encoding="cp437").splitlines():
        match = pattern.match(line)
        if match and match[5].upper() == segment.upper() and match[7].lower() == "tfxdata.asm":
            if (match[4].upper() != "DATA" or match[6].upper() != "DGROUP"
                    or int(match[1], 16) != ds_frame):
                raise ValueError("ASM contribution is not DATA in the reviewed DGROUP frame")
            found.append((int(match[1], 16) * 16 + int(match[2], 16), int(match[3], 16)))
    if len(found) != 1:
        raise ValueError("expected one complete assembler MAP contribution")
    return found[0]


def command_records(builder: Builder) -> list[dict]:
    return [{**record, "log_sha256": digest_file(builder.root.parent / record["log"])}
            for record in builder.records]


def observe(work: Path, config: dict, name: str, target, negative: str | None = None) -> dict:
    source = work / "source"
    profile = config["profiles"][name]
    expected = {"tfxdata.asm": mutate((ROOT / config["source"]).read_bytes(), negative),
                "symbols.inc": (ROOT / profile["symbols"]).read_bytes(),
                "bindings.asm": (ROOT / profile["bindings"]).read_bytes(),
                "build_dumb.bat": b"", "link.rsp": LINK_RESPONSE}
    for path, data in expected.items():
        if (source / path).read_bytes() != data:
            raise ValueError("saved actual assembler/linker inputs differ from maintained source")
    commands = json.loads((work / "commands.json").read_text())
    expected_commands = [ASSEMBLER + ["bindings.asm", "bindings.obj"],
                         ASSEMBLER + ["tfxdata.asm", "tfxdata.obj"],
                         ["wine", str(ROOT / "_reference/ReC98/bin/msdos.exe"),
                          "-e", "-x", "tlink", "@link.rsp"]]
    if len(commands) != 3:
        raise ValueError("missing actual producer commands")
    for record, command in zip(commands, expected_commands):
        if (record["command"] != command or record["returncode"] != 0
                or record["log_sha256"] != digest_file(work / record["log"])):
            raise ValueError("actual producer argv or successful logs changed")
    obj_raw = (source / "tfxdata.obj").read_bytes()
    omf = describe_omf(obj_raw)
    scopes = asm_scopes(obj_raw)
    binding = describe_omf((source / "bindings.obj").read_bytes())
    if binding["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("binding is not a valid pinned assembler object")
    candidate = parse_mz((source / "units.exe").read_bytes())
    comparisons = {}
    for scope, segment, size in SCOPES:
        start, actual_size = map_scope(source / "units.map", segment, profile["ds_frame"])
        if size != actual_size or start != profile[scope + "_start"]:
            raise ValueError("complete actual MAP extent changed")
        comparisons[scope] = compare_unit(target, candidate, profile[scope + "_start"], start, size)
    # Publics must agree with whole-contribution boundaries and table strides.
    base, state = (comparisons[s]["candidate_start"] for s in ("dispatch", "state"))
    expected_publics = {"_grppsafx_func_offsets_1": base, "_grppsafx_func_offsets_2": base + 10,
                        "_grppsafx_mask_ptrs": base + 20, "_graph_putsa_fx_func": state,
                        "_graph_putsa_fx_spacing": state + 2}
    actual_publics = map_publics(source / "units.map")
    for symbol, address in expected_publics.items():
        values = {value for value, label in actual_publics if label.lower() == symbol}
        if values != {address}:
            raise ValueError("assembler public disagrees with reviewed data boundary")
    return {"comparisons": comparisons, "omf_scopes": scopes,
            "object_sha256": omf["sha256"],
            "object_normalized_sha256": omf["dependency_timestamp_normalized_sha256"],
            "bindings_sha256": binding["sha256"],
            "bindings_normalized_sha256": binding["dependency_timestamp_normalized_sha256"],
            "map_sha256": digest_file(source / "units.map"),
            "mz_sha256": digest_file(source / "units.exe"),
            "commands_sha256": digest_file(work / "commands.json")}


def cold_round(work: Path, config: dict, name: str, target, negative: str | None = None) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    profile = config["profiles"][name]
    (source / "tfxdata.asm").write_bytes(mutate((ROOT / config["source"]).read_bytes(), negative))
    shutil.copyfile(ROOT / profile["symbols"], source / "symbols.inc")
    shutil.copyfile(ROOT / profile["bindings"], source / "bindings.asm")
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    builder.execute("bindings", ASSEMBLER + ["bindings.asm", "bindings.obj"])
    builder.execute("assemble", ASSEMBLER + ["tfxdata.asm", "tfxdata.obj"])
    (source / "link.rsp").write_bytes(LINK_RESPONSE)
    builder.execute("link", ["wine", str(builder.msdos), "-e", "-x", "tlink", "@link.rsp"])
    (work / "commands.json").write_text(json.dumps(command_records(builder), indent=2) + "\n")
    return observe(work, config, name, target, negative)


def native_review(path: Path, config: dict, targets: dict) -> None:
    if digest_file(path) != config["native_review_sha256"]:
        raise ValueError("native boundary review changed")
    review = json.loads(path.read_text())
    if review["CODE_credit"] != 0 or review["raster_mask_credit"] != 0:
        raise ValueError("native CODE or resource bytes must not receive credit")
    for name, profile in config["profiles"].items():
        artifact, target, proof = targets[name]
        entry = review["profiles"][name]
        if (entry["target_sha256"] != artifact["sha256"] or entry["target_view"] != proof
                or entry["CODE_extent"] != [profile["code_start"], profile["code_end"]]
                or entry["DS_frame"] != profile["ds_frame"]
                or entry["instruction_nops"] != profile["instruction_nops"]
                or entry["dispatch_data"] != [profile["dispatch_start"], profile["mask_start"]]
                or entry["excluded_raster_masks"] != [profile["mask_start"], profile["state_start"]]
                or entry["state_data"] != [profile["state_start"], profile["state_start"] + 4]):
            raise ValueError("native ownership geometry or target proof disagrees")
        instructions = entry["CODE_instructions"]
        cursor = profile["code_start"]
        for ins in instructions:
            data = bytes.fromhex(ins["bytes"])
            if (ins["address"] != cursor or not data
                    or target.program_image[cursor:cursor + len(data)] != data):
                raise ValueError("native complete instruction boundary review disagrees")
            cursor += len(data)
        if cursor != profile["code_end"]:
            raise ValueError("native CODE review is incomplete")
        writes = [i for i in instructions if i["mnemonic"] == "mov" and i["operands"].startswith("word ptr cs:")]
        if (writes != entry["actual_CS_writes"] or len(writes) != 5
                or [i["address"] for i in instructions if i["mnemonic"] == "nop"] != profile["instruction_nops"]):
            raise ValueError("native self-modification or NOP review changed")
        for scope, _, size in SCOPES:
            if relative_fixups(target, profile[scope + "_start"], size) != entry["ordered_DATA_fixups"]:
                raise ValueError("native ordered DATA relocation review disagrees")
        symbols = {}
        for line in (ROOT / profile["symbols"]).read_text().splitlines():
            match = re.fullmatch(r"(\w+) equ 0([0-9a-f]+)h", line)
            if match:
                symbols[match[1]] = int(match[2], 16)
        for i in (1, 2):
            call = profile["cs_base"] + symbols[f"grppsafx_glyph_func_{i}"] - 1
            displacement = int.from_bytes(target.program_image[call + 1:call + 3], "little", signed=True)
            if (target.program_image[call] != 0xE8
                    or call + 3 + displacement != profile["cs_base"] + symbols["glyph_weight_bold"]):
                raise ValueError("bound CALL operand does not invoke the native default helper")
        for i in range(1, 5):
            if symbols[f"_grppsafx_mask_{i}"] != profile["mask_start"] - profile["ds_frame"] * 16 + (i - 1) * 8:
                raise ValueError("bound raster resource address disagrees")


def check_public(record: dict, config: dict) -> None:
    if (config["origin"] != ORIGIN or config["global_authored_credit"] != "unreviewed"
            or record["origin"] != ORIGIN or record["global_authored_credit"] != "unreviewed"
            or record["inputs"] != inputs(config) or record["asm_data_bytes_exact"] != 64
            or record["cxx_authored_credit"] != 0 or record["complete_executable_exact"] is not False
            or set(record["profiles"]) != {"op", "maine"}):
        raise ValueError("ASM identity, origin or separate credit policy changed")
    for name, result in record["profiles"].items():
        context = UnitContext(ROOT, name)
        validate_public_target_view(context, context.config(), result["target_view"], result["target_sha256"])
        rounds = result["rounds"]
        if len(rounds) != 2:
            raise ValueError("two independent fresh ASM producers required")
        for field in ("object_normalized_sha256", "bindings_normalized_sha256", "mz_sha256", "map_sha256"):
            if rounds[0][field] != rounds[1][field]:
                raise ValueError("ASM producers are not deterministic")
        for scope, _, size in SCOPES:
            for positive in rounds:
                comparison = positive["comparisons"][scope]
                if (comparison["size"] != size or comparison["exact"] is not True
                        or comparison["target_start"] != config["profiles"][name][scope + "_start"]
                        or comparison["candidate_start"] != comparison["target_start"]
                        or comparison["raw_exact"] is not True or comparison["fixups_exact"] is not True
                        or comparison["target_fixups"] != [] or comparison["candidate_fixups"] != []
                        or comparison["target_sha256"] != comparison["candidate_sha256"]):
                    raise ValueError("incomplete raw/ordered-fixup ASM comparison")
            negative = result["negative_controls"][scope]["comparisons"]
            if (negative[scope]["raw_exact"] is not False or negative[scope]["exact"] is not False
                    or negative[scope]["size"] != size or negative[scope]["fixups_exact"] is not True
                    or negative[scope]["target_fixups"] != [] or negative[scope]["candidate_fixups"] != []):
                raise ValueError("own assembled negative mutation was not rejected")
            if any(negative[other]["exact"] is not True for other, _, _ in SCOPES if other != scope):
                raise ValueError("negative mutation escaped its declared DATA scope")


def targets_for(config: dict, work: Path | None = None) -> dict:
    targets = {}
    for name in config["profiles"]:
        context = UnitContext(ROOT, name)
        targets[name] = load_unit_target(context, context.config(),
                                         cache=work / name / "target-view" if work else None)
    return targets


def accept(path: Path, config: dict) -> None:
    record = json.loads(path.read_text())
    check_public(record, config)
    work = path.parent
    for entry in record["inputs"]:
        if digest_file(work / "inputs" / entry["path"]) != entry["sha256"]:
            raise ValueError("frozen ASM source or verifier snapshot changed")
    targets = targets_for(config, work)
    native_review(work / "native-review.json", config, targets)
    tool_path = work / "toolchain-attestation.json"
    tool = json.loads(tool_path.read_text())
    manifest, surfaces = static_toolchain(ROOT)
    validate_full_toolchain(tool, manifest, surfaces)
    proof_path = work / "toolchain-reuse-proof.json"
    proof = json.loads(proof_path.read_text())
    if (digest_file(tool_path) != record["toolchain_receipt_sha256"]
            or digest_file(proof_path) != record["toolchain_reuse_proof_sha256"]
            or proof["original_full_receipt_sha256"] != record["toolchain_receipt_sha256"]
            or proof["manifest_sha256"] != manifest or proof["reused"] != record["toolchain_reused"]):
        raise ValueError("frozen executable toolchain proof changed")
    for name, result in record["profiles"].items():
        artifact, target, target_view = targets[name]
        if artifact["sha256"] != result["target_sha256"] or target_view != result["target_view"]:
            raise ValueError("saved decoded target proof changed")
        for i, label in enumerate(("a", "b")):
            if observe(work / name / label, config, name, target) != result["rounds"][i]:
                raise ValueError("saved complete positive ASM producer disagrees")
        for scope, _, _ in SCOPES:
            if observe(work / name / ("negative-" + scope), config, name, target, scope) != result["negative_controls"][scope]:
                raise ValueError("saved own negative ASM producer disagrees")
    PUBLIC.write_text(json.dumps({**record, "replay_receipt_sha256": digest_file(path)}, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--accept", type=Path)
    group.add_argument("--check", action="store_true")
    parser.add_argument("--native-review", type=Path)
    args = parser.parse_args()
    config = tomllib.loads(CONFIG.read_text())
    if args.check:
        check_public(json.loads(PUBLIC.read_text()), config)
        print("PASS: 64 symbolic ASM DATA bytes source-current; zero C/C++ or global authored credit")
        return 0
    if args.accept:
        accept(args.accept.resolve(), config)
        print("PASS: both complete ASM DATA scopes revalidated in both artifacts; origin remains inferred")
        return 0
    if args.native_review is None:
        parser.error("--output requires the reviewed private --native-review")
    work = args.output.resolve()
    if work.exists():
        parser.error("replay requires a fresh output directory")
    targets = targets_for(config)
    native_review(args.native_review, config, targets)
    work.mkdir(parents=True)
    snapshot = inputs(config)
    for entry in snapshot:
        destination = work / "inputs" / entry["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / entry["path"], destination)
    shutil.copyfile(args.native_review, work / "native-review.json")
    result = {}
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        for name, (artifact, target, proof) in targets.items():
            (work / name).mkdir()
            freeze_target_view(UnitContext(ROOT, name), work / name / "target-view")
            rounds = []
            for label in ("a", "b"):
                observed = cold_round(work / name / label, config, name, target)
                rounds.append(observed)
                if any(not c["exact"] for c in observed["comparisons"].values()):
                    raise ValueError("positive ASM raw/fixup mismatch; stopped before further builds")
            negatives = {scope: cold_round(work / name / ("negative-" + scope), config, name, target, scope)
                         for scope, _, _ in SCOPES}
            result[name] = {"target_sha256": artifact["sha256"], "target_view": proof,
                            "rounds": rounds, "negative_controls": negatives}
    record = {"schema_version": 1, "kind": "bounded-symbolic-asm-data-replay", "inputs": snapshot,
              "origin": ORIGIN, "global_authored_credit": "unreviewed", "asm_data_bytes_exact": 64,
              "cxx_authored_credit": 0, "complete_executable_exact": False, "profiles": result,
              "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
              "toolchain_reused": tool["reused"], "toolchain_reuse_proof_sha256": tool["proof_sha256"]}
    check_public(record, config)
    (work / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: two fresh ASM producers and own negative per scope/artifact: {work / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

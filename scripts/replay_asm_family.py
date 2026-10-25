#!/usr/bin/env python3
"""Incremental bounded original-assembly CODE families, with explicit adoption."""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import re
import shutil
import tomllib

from lib.omf import describe_omf, parse_omf
from lib.pc98 import digest_file, digest_bytes, parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain, static_toolchain, validate_full_toolchain, relative_path
from lib.unit_context import UnitContext, load_unit_target, freeze_target_view, validate_public_target_view
from lib.unit_oracle import compare_unit, map_publics, relative_fixups
from lib.unit_extents import _index as index

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/asm_families.toml"
PUBLIC = ROOT / "config/accepted_asm_families.json"
DECISION = ROOT / "config/reviewed_asm_families.json"
ORIGIN = "reviewed-native-handwritten-assembly-reconstruction"
ASSEMBLER = ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t"]
RESPONSE = b"-c -s -E bindings.obj unit.obj, units.exe, units.map,\r\n"
KINDS = {"alignment", "inert-branch", "runtime-placeholder"}


def digest_object(value: dict) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def configuration() -> dict:
    config = tomllib.loads(CONFIG.read_text())
    rows = config["units"]
    if config["schema_version"] != 1 or not rows or len({r["id"] for r in rows}) != len(rows):
        raise ValueError("invalid ASM family manifest")
    for entry in rows:
        if entry["artifact"] not in ("main", "op", "maine") or not entry["publics"]:
            raise ValueError("ASM family requires a pinned artifact and real public boundaries")
        for key in ("source", "types", "bindings", "symbols", "notes"):
            relative_path(entry[key])
        if not entry["source"].endswith(".asm"):
            raise ValueError("compiler-generated owners cannot use the ASM lane")
        layout(entry)
    return {r["id"]: r for r in rows}


def producer_inputs(entry: dict) -> list[dict]:
    paths = {entry[k] for k in ("source", "types", "bindings", "symbols")}
    paths.update(entry["semantic_inputs"])
    paths.update(("config/targets.toml", "config/toolchain.toml"))
    return [{"path": p, "sha256": digest_file(ROOT / relative_path(p))} for p in sorted(paths)]


def verifier_inputs() -> list[dict]:
    paths = ["scripts/replay_asm_family.py", "scripts/lib/omf.py", "scripts/lib/pc98.py",
             "scripts/lib/reference_build.py", "scripts/lib/replay_toolchain.py", "scripts/lib/unit_context.py",
             "scripts/lib/unit_oracle.py", "scripts/lib/unit_extents.py"]
    return [{"path": p, "sha256": digest_file(ROOT / p)} for p in paths]


def layout(entry: dict) -> list[dict]:
    size = entry["size"]
    if type(size) is not int or size <= 0:
        raise ValueError("ASM scope needs a positive complete size")
    special = []
    for table in entry.get("tables", []):
        if table["size"] <= 0 or table["size"] % 2:
            raise ValueError("ASM near-handler table needs complete words")
        special.append({**table, "kind": "dispatch-table"})
    for row in entry.get("uncredited", []):
        if row["kind"] not in KINDS:
            raise ValueError("unreviewed zero-credit ASM kind")
        special.append(dict(row))
    output, cursor = [], 0
    for row in sorted(special, key=lambda r: r["offset"]):
        left, right = row["offset"], row["offset"] + row["size"]
        if (type(left) is not int or type(row["size"]) is not int or row["size"] <= 0
                or left < cursor or right > size):
            raise ValueError("ASM classification overlaps or escapes complete scope")
        if cursor < left:
            output.append({"offset": cursor, "size": left - cursor, "kind": "instructions"})
        output.append(row)
        cursor = right
    if cursor < size:
        output.append({"offset": cursor, "size": size - cursor, "kind": "instructions"})
    return output


def counts(entry: dict) -> dict:
    result = {k: 0 for k in ("instructions", "dispatch-table", *sorted(KINDS))}
    for row in layout(entry):
        result[row["kind"]] += row["size"]
    return result


def source_bytes(entry: dict, negative: bool) -> bytes:
    source = (ROOT / entry["source"]).read_bytes()
    if negative:
        before, after = (entry["negative"][k].encode("utf8") for k in ("find", "replace"))
        if not before or source.count(before) != 1 or before == after:
            raise ValueError("ASM semantic negative needs one real mutation anchor")
        source = source.replace(before, after)
    return source


def native_review(path: Path, entry: dict, artifact: dict, target) -> None:
    if digest_file(path) != entry["native_review_sha256"]:
        raise ValueError("native ASM origin/boundary review digest changed")
    proof = json.loads(path.read_text())
    start, size = entry["target_start"], entry["size"]
    if (proof["target_sha256"] != artifact["sha256"] or (proof["start"], proof["size"]) != (start, size)
            or proof["cs_base"] != entry["cs_base"] or proof["sha256"] != entry["target_scope_sha256"]
            or digest_bytes(target.program_image[start:start + size]) != entry["target_scope_sha256"]
            or relative_fixups(target, start, size) != entry["fixups"] or proof["ordered_fixups"] != entry["fixups"]):
        raise ValueError("complete native ASM target/bounds/ordered fixups disagree")
    covered, starts, nops = bytearray(size), set(), []
    for ins in proof["instructions"]:
        offset = ins["address"] - start
        raw = bytes.fromhex(ins["bytes"])
        end = offset + len(raw)
        if (not raw or offset < 0 or end > size or any(covered[offset:end])
                or target.program_image[start + offset:start + end] != raw):
            raise ValueError("native instruction review overlaps or differs")
        covered[offset:end] = b"\1" * len(raw)
        starts.add(ins["address"])
        if ins["mnemonic"] == "nop":
            nops.append(offset)
    if [{"offset": r["offset"], "size": r["size"]} for r in proof["tables"]] != entry.get("tables", []):
        raise ValueError("native CODE table extent changed")
    for table in proof["tables"]:
        left, right = table["offset"], table["offset"] + table["size"]
        if left < 0 or right > size or any(covered[left:right]):
            raise ValueError("native ASM table overlaps instructions")
        actual = [int.from_bytes(target.program_image[i:i + 2], "little") + entry["cs_base"]
                  for i in range(start + left, start + right, 2)]
        if actual != table["targets"] or any(h not in starts for h in actual):
            raise ValueError("native ASM table escapes real handler boundaries")
        covered[left:right] = b"\1" * (right - left)
    if not all(covered):
        raise ValueError("native complete ASM review leaves unknown bytes")
    alignment = [i for r in entry.get("uncredited", []) if r["kind"] == "alignment"
                 for i in range(r["offset"], r["offset"] + r["size"])]
    if sorted(nops) != sorted(alignment + entry["instruction_nops"]):
        raise ValueError("native instruction/alignment NOP review is incomplete")
    if any(target.program_image[start + i] != 0x90 for i in alignment):
        raise ValueError("native EVEN padding bytes differ")


def omf_scope(raw: bytes, config: dict) -> dict:
    """Only one complete ordinary CODE contribution; no initialized DATA."""
    description = describe_omf(raw)
    if description["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("ASM family requires a genuine pinned assembler producer")
    names, segments = [""], [None]
    records = parse_omf(raw)
    for record in records:
        if record.name in {"LIDATA", "LIDATA32", "COMDAT", "COMDAT32", "BAKPAT", "BAKPAT32",
                           "LEDATA32", "SEGDEF32", "FIXUPP32"}:
            raise ValueError("unsupported ASM CODE producer transform")
        body = record.data
        if record.name == "LNAMES":
            cursor = 0
            while cursor < len(body):
                length = body[cursor]
                cursor += 1
                if cursor + length > len(body):
                    raise ValueError("truncated ASM CODE names")
                names.append(body[cursor:cursor + length].decode("cp437"))
                cursor += length
        elif record.name == "SEGDEF":
            if len(body) < 6 or not body[0] & 0xE0 or body[0] & 2:
                raise ValueError("unsupported ASM CODE SEGDEF")
            name, cursor = index(body, 3)
            cl, cursor = index(body, cursor)
            overlay, cursor = index(body, cursor)
            if (cursor != len(body) or not 0 < name < len(names)
                    or not 0 < cl < len(names) or not 0 <= overlay < len(names)):
                raise ValueError("invalid ASM CODE segment names")
            segments.append((names[name], names[cl], int.from_bytes(body[1:3], "little")))
    matches = [(i, seg) for i, seg in enumerate(segments) if seg and seg[0] == config["segment"]]
    if len(matches) != 1 or matches[0][1][1:] != ("CODE", config["size"]):
        raise ValueError("expected complete reviewed ASM family CODE SEGDEF")
    si = matches[0][0]
    if any(seg and seg[2] and i != si for i, seg in enumerate(segments)):
        raise ValueError("unreviewed initialized/reserved source contribution")
    covered, chunks = bytearray(config["size"]), []
    for record in records:
        if record.name != "LEDATA":
            continue
        owner, cursor = index(record.data, 0)
        if owner != si or cursor + 2 > len(record.data):
            raise ValueError("LEDATA outside complete ASM family scope")
        start = int.from_bytes(record.data[cursor:cursor + 2], "little")
        payload = record.data[cursor + 2:]
        end = start + len(payload)
        if not payload or end > len(covered) or any(covered[start:end]):
            raise ValueError("ASM CODE overlap or out-of-bounds LEDATA")
        covered[start:end] = b"\1" * len(payload)
        chunks.append({"offset": start, "size": len(payload), "sha256": digest_bytes(payload)})
    if not all(covered):
        raise ValueError("incomplete ASM family LEDATA coverage")
    return {"kind": "complete-assembler-code", "segment": config["segment"], "size": len(covered), "ledata": chunks}




def map_scope(path: Path, entry: dict) -> int:
    regex = re.compile(r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+"
                       r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)", re.I)
    found = []
    for line in path.read_text(encoding="cp437").splitlines():
        m = regex.match(line)
        if m and m[5].casefold() == entry["segment"].casefold() and m[7].lower() == "unit.asm":
            if (m[4].upper() != "CODE" or m[6].casefold() != entry["group"].casefold()
                    or int(m[1], 16) * 16 != entry["cs_base"] or int(m[3], 16) != entry["size"]):
                raise ValueError("actual ASM CODE class/group/frame/size differs")
            found.append(int(m[1], 16) * 16 + int(m[2], 16))
    if found != [entry["target_start"]]:
        raise ValueError("expected one complete actual ASM contribution")
    return found[0]


def map_ds(path: Path, ds_base: int) -> None:
    rows = re.findall(r"^\s*([0-9A-F]{4}):[0-9A-F]{4}\s+[0-9A-F]{4}\s+"
                      r"C=DATA\s+S=_DATA\s+G=DGROUP\s+M=bindings\.asm\s", path.read_text(encoding="cp437"), re.I | re.M)
    if len(rows) != 1 or int(rows[0], 16) * 16 != ds_base:
        raise ValueError("actual symbol-only DATA frame differs from native DS context")


def observe(work: Path, entry: dict, target, negative: bool = False) -> dict:
    source = work / "source"
    expected = {"unit.asm": source_bytes(entry, negative), "types.inc": (ROOT / entry["types"]).read_bytes(),
                "symbols.inc": (ROOT / entry["symbols"]).read_bytes(),
                "bindings.asm": (ROOT / entry["bindings"]).read_bytes(),
                "link.rsp": RESPONSE, "build_dumb.bat": b""}
    for path, raw in expected.items():
        if (source / path).read_bytes() != raw:
            raise ValueError("actual saved ASM/linker aliases differ from maintained inputs")
    commands = json.loads((work / "commands.json").read_text())
    argv = [ASSEMBLER + ["bindings.asm", "bindings.obj"], ASSEMBLER + ["unit.asm", "unit.obj"],
            ["wine", str(ROOT / "_reference/ReC98/bin/msdos.exe"), "-e", "-x", "tlink", "@link.rsp"]]
    if len(commands) != len(argv):
        raise ValueError("missing actual successful ASM producer argv")
    for row, command in zip(commands, argv):
        if (row["command"] != command or row["returncode"] != 0
                or digest_file(work / row["log"]) != row["log_sha256"]):
            raise ValueError("successful ASM command/log identity differs")
    raw = (source / "unit.obj").read_bytes()
    scope, obj = omf_scope(raw, entry), describe_omf(raw)
    binder = describe_omf((source / "bindings.obj").read_bytes())
    if (binder["translator_comments"] != ["Turbo Assembler  Version 5.0"]
            or any(binder["record_counts"].get(k, 0) for k in ("LEDATA", "LIDATA", "COMDAT"))):
        raise ValueError("binding object is invalid or supplies initialized payload")
    candidate = parse_mz((source / "units.exe").read_bytes())
    # This readback is a verifier guard, not an assembler input. A stricter
    # verifier can recheck unchanged retained producers without cold rebuilding.
    native = json.loads((work.parent / "native-review.json").read_text())
    map_ds(source / "units.map", native["ds_base"])
    start = map_scope(source / "units.map", entry)
    publics = map_publics(source / "units.map")
    for label, offset in entry["publics"].items():
        if {value for value, name in publics if name.casefold() == label.casefold()} != {start + offset}:
            raise ValueError("actual ASM entry/table/patch public boundary differs")
    return {"comparison": compare_unit(target, candidate, entry["target_start"], start, entry["size"]),
            "omf_scope": scope, "object_sha256": obj["sha256"],
            "object_normalized_sha256": obj["dependency_timestamp_normalized_sha256"],
            "bindings_sha256": binder["sha256"], "bindings_normalized_sha256": binder["dependency_timestamp_normalized_sha256"],
            "map_sha256": digest_file(source / "units.map"), "mz_sha256": digest_file(source / "units.exe"),
            "commands_sha256": digest_file(work / "commands.json")}


def cold_round(work: Path, entry: dict, target, negative: bool = False) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    (source / "unit.asm").write_bytes(source_bytes(entry, negative))
    for key, alias in (("types", "types.inc"), ("symbols", "symbols.inc"), ("bindings", "bindings.asm")):
        shutil.copyfile(ROOT / entry[key], source / alias)
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    for module in ("bindings", "unit"):
        builder.execute(module, ASSEMBLER + [module + ".asm", module + ".obj"])
    (source / "link.rsp").write_bytes(RESPONSE)
    builder.execute("link", ["wine", str(builder.msdos), "-e", "-x", "tlink", "@link.rsp"])
    records = [{**row, "log_sha256": digest_file(work / row["log"])} for row in builder.records]
    (work / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
    return observe(work, entry, target, negative)


def check_record(record: dict, entry: dict) -> None:
    if (record["entry"] != entry or record["producer_inputs"] != producer_inputs(entry)
            or record["counts"] != counts(entry) or record["origin"] != ORIGIN
            or record["historical_source_recovered"] is not False or record["cxx_authored_credit"] != 0
            or record["complete_executable_exact"] is not False):
        raise ValueError("ASM source, complete scope, classification or origin changed")
    target = next(r for r in tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"]
                  if r["id"] == "th05-" + entry["artifact"])
    if record["target_sha256"] != target["sha256"]:
        raise ValueError("ASM target identity differs")
    if entry["artifact"] != "main":
        c = UnitContext(ROOT, entry["artifact"])
        validate_public_target_view(c, c.config(), record["target_view"], target["sha256"])
    rounds = record["rounds"]
    if len(rounds) != 2:
        raise ValueError("two independent fresh ASM producers required")
    for key in ("object_normalized_sha256", "bindings_normalized_sha256", "map_sha256", "mz_sha256"):
        if rounds[0][key] != rounds[1][key]:
            raise ValueError("ASM producers are not deterministic")
    for row in rounds:
        c = row["comparison"]
        if (c["size"] != entry["size"] or c["target_start"] != entry["target_start"] or c["candidate_start"] != c["target_start"]
                or any(c[k] is not True for k in ("raw_exact", "fixups_exact", "exact"))
                or c["target_fixups"] != entry["fixups"] or c["candidate_fixups"] != entry["fixups"]
                or c["target_sha256"] != entry["target_scope_sha256"] or c["candidate_sha256"] != c["target_sha256"]):
            raise ValueError("incomplete full ASM raw/ordered-fixup proof")
    n = record["negative_control"]["comparison"]
    if (n["raw_exact"] is not False or n["exact"] is not False or n["fixups_exact"] is not True
            or n["size"] != entry["size"] or n["target_fixups"] != entry["fixups"] or n["candidate_fixups"] != entry["fixups"]):
        raise ValueError("own semantic ASM mutation was not rejected")


def validate_receipt(path: Path, entries: dict) -> dict:
    record = json.loads(path.read_text())
    entry = entries[record["entry"]["id"]]
    check_record(record, entry)
    work = path.parent
    frozen = tomllib.loads((work / "manifest.toml").read_text())
    if next(r for r in frozen["units"] if r["id"] == entry["id"]) != entry:
        raise ValueError("frozen selected ASM manifest entry differs")
    for row in record["producer_inputs"] + record["verifier_inputs"]:
        if digest_file(work / "inputs" / relative_path(row["path"])) != row["sha256"]:
            raise ValueError("archived actual ASM source/verifier snapshot differs")
    c = UnitContext(ROOT, entry["artifact"])
    artifact, target, proof = load_unit_target(c, c.config(), cache=work / "target-view" if entry["artifact"] != "main" else None)
    if (artifact["sha256"] != record["target_sha256"] or proof != record["target_view"]
            or record["target_image"] != {"size": len(target.program_image), "sha256": digest_bytes(target.program_image)}):
        raise ValueError("actual target view disagrees with ASM proof")
    native_review(work / "native-review.json", entry, artifact, target)
    tool_path, reuse_path = work / "toolchain-attestation.json", work / "toolchain-reuse-proof.json"
    manifest, surfaces = static_toolchain(ROOT)
    validate_full_toolchain(json.loads(tool_path.read_text()), manifest, surfaces)
    reuse = json.loads(reuse_path.read_text())
    if (digest_file(tool_path) != record["toolchain_receipt_sha256"] or digest_file(reuse_path) != record["toolchain_reuse_proof_sha256"]
            or reuse["manifest_sha256"] != manifest or reuse["reused"] != record["toolchain_reused"]
            or reuse["original_full_receipt_sha256"] != record["toolchain_receipt_sha256"]):
        raise ValueError("frozen successful toolchain/reuse proof differs")
    for i, label in enumerate(("a", "b")):
        if observe(work / label, entry, target) != record["rounds"][i]:
            raise ValueError("saved complete ASM positive producer differs")
    if observe(work / "negative", entry, target, True) != record["negative_control"]:
        raise ValueError("saved own semantic ASM negative producer differs")
    return {**record, "replay_receipt_sha256": digest_file(path)}


def ledger(entries: dict) -> dict:
    result = json.loads(PUBLIC.read_text()) if PUBLIC.exists() else {"schema_version": 1, "units": {}}
    if result["schema_version"] != 1 or set(result["units"]) - entries.keys():
        raise ValueError("unknown ASM acceptance ledger member")
    return result


def reviewed_claims(root: Path, views: dict, *, verify_targets: bool = False) -> tuple[dict, str | None]:
    path = root / DECISION.relative_to(ROOT)
    if not path.exists():
        return {}, None
    entries = configuration()
    accepted = ledger(entries)["units"]
    decision = json.loads(path.read_text())
    if decision.get("schema_version") != 1 or decision.get("classification") != ORIGIN:
        raise ValueError("invalid explicit ASM family adoption")
    selected = decision["units"]
    if not selected or len({r["id"] for r in selected}) != len(selected):
        raise ValueError("explicit ASM selection must be nonempty and unique")
    claims = {}
    for row in selected:
        entry, record = entries[row["id"]], accepted[row["id"]]
        check_record(record, entry)
        if row != {"id": entry["id"], "acceptance_sha256": digest_object(record), "notes_sha256": digest_file(ROOT / entry["notes"])}:
            raise ValueError("stale ASM acceptance/source-review adoption")
        name = entry["artifact"]
        view = views[name]
        if (view["size"], view["sha256"]) != (record["target_image"]["size"], record["target_image"]["sha256"]):
            raise ValueError("ASM ownership coordinates differ from actual target view")
        if verify_targets:
            c = UnitContext(root, name)
            _, target, _ = load_unit_target(c, c.config())
            start = entry["target_start"]
            if digest_bytes(target.program_image[start:start + entry["size"]]) != entry["target_scope_sha256"]:
                raise ValueError("reviewed complete ASM native bytes differ")
        kinds = {"instructions": "accepted-reviewed-asm-instructions", "dispatch-table": "accepted-reviewed-asm-dispatch-table",
                 "alignment": "checked-uncredited-asm-alignment", "inert-branch": "checked-uncredited-asm-inert-branch",
                 "runtime-placeholder": "checked-uncredited-asm-runtime-placeholder"}
        for piece in layout(entry):
            start = entry["target_start"] + piece["offset"]
            claims.setdefault(name, []).append({"start": start, "end": start + piece["size"], "kind": kinds[piece["kind"]],
                                               "unit": entry["id"], "origin": ORIGIN})
    return claims, digest_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--output", type=Path)
    modes.add_argument("--accept", type=Path, action="append")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--plan", action="store_true")
    parser.add_argument("--unit")
    parser.add_argument("--native-review", type=Path)
    args = parser.parse_args()
    entries = configuration()
    accepted = ledger(entries)
    if args.plan:
        needed = []
        for key, entry in entries.items():
            try:
                check_record(accepted["units"][key], entry)
            except (KeyError, ValueError):
                needed.append(key)
        print(json.dumps({"selected": needed, "work_required": bool(needed), "tools_executed": False}, indent=2))
        return 0
    if args.check:
        for key, record in accepted["units"].items():
            check_record(record, entries[key])
        print(f"PASS: {len(accepted['units'])} source-current complete ASM families; adoption remains explicit")
        return 0
    if args.accept:
        imported = [validate_receipt(p.resolve(), entries) for p in args.accept]
        if len({r["entry"]["id"] for r in imported}) != len(imported):
            parser.error("duplicate ASM family import")
        accepted["units"].update({r["entry"]["id"]: r for r in imported})
        for key, record in accepted["units"].items():
            check_record(record, entries[key])
        PUBLIC.write_text(json.dumps(accepted, indent=2) + "\n")
        print("PASS: actual saved ASM producers revalidated and imported atomically")
        return 0
    if args.unit not in entries or args.native_review is None:
        parser.error("--output needs a configured --unit and --native-review")
    work, entry = args.output.resolve(), entries[args.unit]
    if work.exists():
        parser.error("cold ASM replay needs a fresh output directory")
    c = UnitContext(ROOT, entry["artifact"])
    artifact, target, proof = load_unit_target(c, c.config())
    native_review(args.native_review, entry, artifact, target)
    work.mkdir(parents=True)
    inputs, verifiers = producer_inputs(entry), verifier_inputs()
    for row in inputs + verifiers:
        destination = work / "inputs" / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / row["path"], destination)
    shutil.copyfile(CONFIG, work / "manifest.toml")
    shutil.copyfile(args.native_review, work / "native-review.json")
    if entry["artifact"] != "main":
        freeze_target_view(c, work / "target-view")
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        rounds = []
        for label in ("a", "b"):
            result = cold_round(work / label, entry, target)
            rounds.append(result)
            if not result["comparison"]["exact"]:
                raise ValueError("complete ASM raw/fixup mismatch; stopped before further builds")
        negative = cold_round(work / "negative", entry, target, True)
    record = {"schema_version": 1, "kind": "bounded-original-assembly-family-replay", "entry": entry,
              "producer_inputs": inputs, "verifier_inputs": verifiers, "counts": counts(entry), "origin": ORIGIN,
              "historical_source_recovered": False, "cxx_authored_credit": 0, "complete_executable_exact": False,
              "target_sha256": artifact["sha256"], "target_view": proof,
              "target_image": {"size": len(target.program_image), "sha256": digest_bytes(target.program_image)},
              "rounds": rounds, "negative_control": negative, "toolchain_reused": tool["reused"],
              "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
              "toolchain_reuse_proof_sha256": tool["proof_sha256"]}
    check_record(record, entry)
    (work / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: two fresh complete ASM producers and own negative: {work / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

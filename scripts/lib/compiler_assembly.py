"""Exact C/C++ compiled with TCC -S and an unedited TASM32 consumer.

This is a compiler recipe, not handwritten-assembly ownership. Empty foreign
CODE contexts come only from compiler GROUP declarations and the real binder.
"""
from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import tomllib

from .omf import describe_omf
from .pc98 import parse_mz
from .reference_build import Builder
from .replay_toolchain import (bindings_source, digest, entry_digest, include_closure,
    relative_path, scoped_snapshot as direct_snapshot, snapshot_paths, staged_paths,
    freeze_toolchain, static_toolchain, validate_full_toolchain, validate_snapshot)
from .tiny_com import UnitContext, compiler_arguments as direct_arguments, load_unit_target
from .unit_oracle import compare_mapped_unit, map_unit_scope
from .unit_sources import source_encoding, stage_inputs, validate_producer_inputs
from .unit_extents import unit_extent_kind
from . import binding_layout

PIPELINE = "tcc-s-tasm32"
KIND = "bounded-cxx-compiler-assembly-replay"
TRANSLATOR = ["Turbo Assembler  Version 5.0"]
ASSEMBLER = ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t"]
EPOCH = 315532800  # Reproducible input metadata, never an output-byte edit.
PRODUCER_FILES = (
    "scripts/lib/compiler_assembly.py", "scripts/lib/reference_build.py",
    "scripts/lib/replay_toolchain.py", "scripts/lib/unit_sources.py",
    "scripts/lib/unit_context.py", "scripts/lib/tiny_com.py",
    "scripts/lib/binding_layout.py",
    "scripts/lib/omf.py", "scripts/lib/unit_oracle.py",
    "scripts/lib/unit_extents.py", "scripts/replay_asm_family.py",
)
OMF_FIELDS = ("sha256", "dependency_timestamp_normalized_sha256", "module_name",
              "translator_comments", "dependency_paths")


def enabled(entry: dict) -> bool:
    value = entry.get("compiler_pipeline")
    if value is None:
        return False
    if value != PIPELINE:
        raise ValueError("unsupported compiler pipeline")
    return True


def validate_entry(entry: dict) -> None:
    if (not enabled(entry) or entry.get("origin") != "compiler-generated-cxx"
            or not entry["source"].endswith((".c", ".cpp"))
            or source_encoding(entry) != "raw" or entry.get("generated_sources")
            or unit_extent_kind(entry) != "code" or "function_symbol" in entry
            or binding_layout.after_compiler(entry) or entry.get("binary", "M") != "M"):
        raise ValueError("compiler assembly requires one raw MAIN whole C/C++ CODE contribution")
    if any(type(entry.get(key)) is not int for key in ("cs_base", "ds_base")) or not entry.get("group"):
        raise ValueError("compiler assembly requires reviewed native CS/DS/group context")
    if Path(entry["module"]).stem.casefold() in {"bindings", "unit"}:
        raise ValueError("compiler assembly output collides with its scaffold")


def arguments(entry: dict) -> list[str]:
    validate_entry(entry)
    argv = direct_arguments(entry, "M")
    if argv[0] != "-c":
        raise ValueError("unexpected direct compiler recipe")
    return ["-S", *argv[1:]]


def compiler_dependencies(raw: bytes, entry: dict) -> list[str]:
    """Decode TCC's actual E9 dependency records, including continuation lines."""
    records, pending = [], ""
    for line in raw.decode("ascii").splitlines():
        match = re.fullmatch(r"\s*\?debug\s+C\s+([0-9A-Fa-f]+)(\+?)\s*", line)
        if not match:
            if pending:
                raise ValueError("interrupted compiler dependency record")
            continue
        pending += match[1]
        if match[2]:
            continue
        body = bytes.fromhex(pending)
        pending = ""
        if body[:1] != b"\xe9" or len(body) == 1:
            continue
        if len(body) < 6 or len(body) != 6 + body[5]:
            raise ValueError("malformed compiler dependency record")
        records.append(body[6:].decode("ascii").replace("\\", "/"))
    if pending:
        raise ValueError("truncated compiler dependency continuation")
    if entry["module"].casefold() not in {name.casefold() for name in records}:
        raise ValueError("compiler assembly omits its real C/C++ wrapper")
    names = set()
    for name in records:
        if name.casefold() == entry["module"].casefold() or name.casefold().startswith("c:/tc4/include/"):
            continue
        names.add(relative_path(name))
    if entry["source"] not in names:
        raise ValueError("compiler assembly omits maintained C/C++ source")
    return sorted(names)


def assembly_wrapper(raw: bytes, binder: bytes, generated_name: str) -> bytes:
    """Supply only absent foreign CODE SEGDEFs; include compiler text verbatim."""
    if not re.fullmatch(r"[A-Za-z0-9_]+\.asm", generated_name, re.I):
        raise ValueError("invalid generated assembly filename")
    text, bindings = raw.decode("ascii"), binder.decode("ascii")
    defined = {name.casefold() for name in re.findall(r"^([\w]+)\s+segment\b", text, re.M | re.I)}
    binding_groups = {}
    for group, members in re.findall(r"^([\w]+)\s+group\s+([^\r\n;]+)", bindings, re.M | re.I):
        for member in members.split(","):
            binding_groups[member.strip().casefold()] = group.casefold()
    missing = []
    for group, members in re.findall(r"^([\w]+)\s+group\s+([^\r\n;]+)", text, re.M | re.I):
        for member in members.split(","):
            member = member.strip()
            if member.casefold() in defined:
                continue
            declaration = re.search(r"^" + re.escape(member) + r"\s+segment\s+([^\r\n;]+)",
                                    bindings, re.M | re.I)
            if (not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", member)
                    or group.casefold() == "dgroup" or declaration is None
                    or not re.search(r"['\"]CODE['\"]", declaration[1], re.I)
                    or not re.search(r"\bpublic\b", declaration[1], re.I)
                    or not re.search(r"\buse16\b", declaration[1], re.I)
                    or binding_groups.get(member.casefold()) != group.casefold()):
                raise ValueError("missing compiler segment is not a bound foreign CODE context")
            if member.casefold() not in {name.casefold() for name in missing}:
                missing.append(member)
    prefix = ".386p\n" + "".join(
        f"{name} segment byte public use16 'CODE'\n{name} ends\n" for name in missing)
    return (prefix + f"include {generated_name}\n").encode("ascii")


def required_paths(root: Path, entry: dict, dependencies: list[str]) -> set[str]:
    validate_entry(entry)
    names = {relative_path(name) for name in dependencies}
    if entry["source"] not in names or not names.issubset(include_closure(root, entry["source"])):
        raise ValueError("compiler dependency scope escapes maintained source")
    return names | include_closure(root, bindings_source(entry)) | set(PRODUCER_FILES)


def scoped_snapshot(root: Path, entry: dict, result: dict, snapshots: list[dict]) -> list[dict]:
    if not enabled(entry):
        return direct_snapshot(root, entry, result, snapshots)
    validate_result_metadata(entry, result)
    required = required_paths(root, entry, result["compiler_assembly"][0]["compiler_dependencies"])
    known = {item["path"]: item["sha256"] for item in snapshots}
    if len(known) != len(snapshots) or not required.issubset(known):
        raise ValueError("compiler assembly source/recipe snapshot is incomplete")
    return [{"path": name, "sha256": known[name]} for name in sorted(required)]


def validate_result_metadata(entry: dict, result: dict) -> None:
    validate_entry(entry)
    stages = result.get("compiler_assembly", [])
    if (len(stages) != 2 or result.get("compiler_arguments") != [arguments(entry)] * 2
            or stages[0]["compiler_dependencies"] != stages[1]["compiler_dependencies"]
            or any(stages[0].get(key) != stages[1].get(key) for key in
                   ("compiler_generated_assembly_sha256", "wrapper_sha256"))):
        raise ValueError("compiler assembly lacks two unedited compiler-stage witnesses")
    for index, stage in enumerate(stages):
        hashes = [stage.get(key) for key in ("compiler_generated_assembly_sha256",
                  "assembly_after_tasm_sha256", "wrapper_sha256", "map_sha256", "mz_sha256", "commands_sha256")]
        if (any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value) for value in hashes)
                or hashes[0] != hashes[1] or stage["comparison"] != result["rounds"][index]
                or stage["omf"] != result["omfs"][index]
                or stage["owned_CODE"]["size"] != entry["size"]
                or stage["owned_CODE"]["segment"] != entry["segment"]):
            raise ValueError("compiler assembly stage lineage or complete ownership differs")


def map_entry(entry: dict) -> dict:
    return {**entry, "module": "unit.asm"}


def observe(source: Path, entry: dict, record: dict, target, mutation: dict | None = None) -> dict:
    from replay_asm_family import omf_scope
    from replay_units import control_comparison
    stem = Path(entry["module"]).stem
    generated = source / (stem + ".asm")
    raw = generated.read_bytes()
    if (digest(generated) != record["compiler_generated_assembly_sha256"]
            or digest(generated) != record["assembly_after_tasm_sha256"]
            or (source / "unit.asm").read_bytes() != assembly_wrapper(raw, (source / "bindings.asm").read_bytes(), generated.name)
            or (source / "bindings.asm").read_bytes() != (source / bindings_source(entry)).read_bytes()
            or (source / "link.rsp").read_bytes() != link_response(entry)):
        raise ValueError("compiler assembly or generated consumer context was edited")
    prefix = ("#pragma option " + entry["wrapper_options"] + "\n") if entry.get("wrapper_options") else ""
    if (source / entry["module"]).read_text() != prefix + f'#include "{entry["source"]}"\n':
        raise ValueError("compiler assembly C/C++ wrapper changed")
    dependencies = compiler_dependencies(raw, entry)
    object_bytes = (source / (stem + ".obj")).read_bytes()
    description = describe_omf(object_bytes)
    if not description["valid"] or description["translator_comments"] != TRANSLATOR:
        raise ValueError("invalid compiler assembly consumer object")
    scope = map_unit_scope(source / "units.map", map_entry(entry))
    owned = omf_scope(object_bytes, {**entry, "size": scope["size"]})
    lines = (source / "units.map").read_text(encoding="cp437")
    rows = re.findall(r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=(\S+)\s+G=(\S+)\s+M=unit\.asm\s", lines, re.M | re.I)
    actual = [row for row in rows if row[3].casefold() == entry["segment"].casefold() and int(row[2], 16)]
    data = re.findall(r"^\s*([0-9A-F]{4}):[0-9A-F]{4}\s+[0-9A-F]{4}\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=bindings\.asm\s", lines, re.M | re.I)
    if (len(actual) != 1 or int(actual[0][0], 16) * 16 != entry["cs_base"]
            or actual[0][4].casefold() != entry["group"].casefold()
            or len(data) != 1 or int(data[0], 16) * 16 != entry["ds_base"]
            or scope["start"] != entry["target_start"]):
        raise ValueError("compiler assembly native frames or placement differ")
    candidate = parse_mz((source / "units.exe").read_bytes())
    if not candidate.valid:
        raise ValueError("invalid compiler assembly linked MZ")
    comparison = (control_comparison(target, candidate, entry, scope["start"], scope["size"])
                  if mutation else compare_mapped_unit(target, candidate, source / "units.map", map_entry(entry)))
    binder = describe_omf((source / "bindings.obj").read_bytes())
    if not binder["valid"] or any(binder["record_counts"].get(key, 0) for key in ("LEDATA", "LIDATA", "COMDAT")):
        raise ValueError("compiler assembly binder supplies initialized payload")
    return {"comparison": comparison, "compiler_dependencies": dependencies,
            "omf": {key: description[key] for key in OMF_FIELDS}, "owned_CODE": owned,
            "map_sha256": digest(source / "units.map"), "mz_sha256": digest(source / "units.exe"),
            "commands_sha256": digest(source.parent / "commands.json"),
            "compiler_generated_assembly_sha256": digest(generated),
            "assembly_after_tasm_sha256": digest(generated), "wrapper_sha256": digest(source / "unit.asm")}


def link_response(entry: dict) -> bytes:
    return f'-c -s -E bindings.obj {Path(entry["module"]).stem}.obj, units.exe, units.map,\r\n'.encode("ascii")


def producer_directories(work: Path) -> list[Path]:
    base = work.resolve()
    sources = [(work / name / "source").resolve(strict=True) for name in ("a", "b", "negative")]
    if len(set(sources)) != 3 or any(not path.is_relative_to(base) for path in sources):
        raise ValueError("compiler assembly requires independent contained producer directories")
    return sources


def command_lines(root: Path, entry: dict) -> list[list[str]]:
    dos = ["wine", str(root / "_reference/ReC98/bin/msdos.exe"), "-e", "-x"]
    stem = Path(entry["module"]).stem
    return [ASSEMBLER + ["bindings.asm", "bindings.obj"], [*dos, "tcc", *arguments(entry)],
            ASSEMBLER + ["unit.asm", stem + ".obj"], [*dos, "tlink", "@link.rsp"]]


def cold_round(root: Path, work: Path, inputs: Path, entry: dict, paths: set[str], target,
               mutation: dict | None = None) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    stage_inputs(inputs, source, [entry], paths, mutation=mutation)
    wrapper = source / entry["module"]
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    prefix = ("#pragma option " + entry["wrapper_options"] + "\n") if entry.get("wrapper_options") else ""
    wrapper.write_text(prefix + f'#include "{entry["source"]}"\n')
    shutil.copyfile(source / bindings_source(entry), source / "bindings.asm")
    (source / "build_dumb.bat").touch()
    for path in source.rglob("*"):
        if path.is_file():
            os.utime(path, (EPOCH, EPOCH))
    builder = Builder(source, root / ".analysis/toolchain/wineprefix", root / "_reference/ReC98/bin/msdos.exe")
    commands = command_lines(root, entry)
    builder.execute("bindings", commands[0])
    builder.execute("compiler-assembly", commands[1])
    generated = source / (Path(entry["module"]).stem + ".asm")
    before = digest(generated)
    (source / "unit.asm").write_bytes(assembly_wrapper(generated.read_bytes(), (source / "bindings.asm").read_bytes(), generated.name))
    builder.execute("compiler-object", commands[2])
    after = digest(generated)
    (source / "link.rsp").write_bytes(link_response(entry))
    builder.execute("link", commands[3])
    steps = [{**row, "log_sha256": digest(work / row["log"])} for row in builder.records]
    (work / "commands.json").write_text(json.dumps(steps, indent=2) + "\n")
    stage = observe(source, entry, {"compiler_generated_assembly_sha256": before,
                                   "assembly_after_tasm_sha256": after}, target, mutation)
    return stage


def replay(root: Path, entry: dict, manifest_bytes: bytes, work: Path) -> dict:
    validate_entry(entry)
    if work.exists():
        raise ValueError("compiler assembly requires a new output directory")
    work.resolve().relative_to((root / ".analysis").resolve())
    context = UnitContext(root)
    config = tomllib.loads(manifest_bytes.decode())
    controls = [row for row in config.get("controls", []) if row["unit"] == entry["id"]]
    if len(controls) != 1:
        raise ValueError("compiler assembly needs one normal compiled source control")
    mutation = controls[0]
    artifact, target, _ = load_unit_target(context, config)
    work.mkdir(parents=True)
    (work / "exact-units.toml").write_bytes(manifest_bytes)
    initial = staged_paths(root, entry) | set(PRODUCER_FILES)
    inputs = work / "inputs"
    for item in snapshot_paths(root, initial):
        destination = inputs / item["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / item["path"], destination)
    with (root / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(root, work / "toolchain-attestation.json")
        shutil.copyfile(root / "config/toolchain.toml", work / "toolchain.toml")
        rounds = [cold_round(root, work / name, inputs, entry, initial, target) for name in ("a", "b")]
        dependencies = rounds[0]["compiler_dependencies"]
        if rounds[1]["compiler_dependencies"] != dependencies:
            raise ValueError("independent compiler assembly dependency scopes differ")
        needed = required_paths(inputs, entry, dependencies)
        if mutation["source"] not in dependencies:
            raise ValueError("compiler assembly mutation is outside consumed C/C++ inputs")
        negative = cold_round(root, work / "negative", inputs, entry, initial, target, mutation)
        snapshots = snapshot_paths(inputs, needed)
        result = {"id": entry["id"], "entry_sha256": entry_digest(entry),
                  "rounds": [row["comparison"] for row in rounds], "omfs": [row["omf"] for row in rounds],
                  "compiler_assembly": rounds, "compiler_arguments": [arguments(entry)] * 2,
                  "producer_paths": ["a/source", "b/source"], "source_inputs": snapshots,
                  "object_normalized_equal": len({row["omf"]["dependency_timestamp_normalized_sha256"] for row in rounds}) == 1}
        result["exact"] = (result["object_normalized_equal"] and all(row["comparison"]["exact"] for row in rounds)
                           and rounds[0]["map_sha256"] == rounds[1]["map_sha256"]
                           and rounds[0]["mz_sha256"] == rounds[1]["mz_sha256"])
        receipt = {"schema_version": 1, "kind": KIND, "entry": entry, "input_epoch": EPOCH,
                   "target_sha256": artifact["sha256"], "manifest_sha256": digest(work / "exact-units.toml"),
                   "toolchain_manifest_sha256": tool["manifest_sha256"],
                   "toolchain_receipt_sha256": tool["receipt_sha256"],
                   "toolchain_reused": tool["reused"], "toolchain_reuse_proof_sha256": tool["proof_sha256"],
                   "source_inputs": snapshots, "result": result, "negative": negative, "mutation": mutation,
                   "complete_executable_exact": False,
                   "pass": result["exact"] and not negative["comparison"]["raw_exact"]}
        (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        validate_snapshot(root, snapshots)
    return receipt


def validate_receipt(receipt_path: Path, *, root: Path, units: list[str] | None = None,
                     artifact_name: str = "main", validate_only: bool = False) -> dict:
    import progress
    if artifact_name != "main":
        raise ValueError("compiler assembly currently supports MAIN C/C++ only")
    work = receipt_path.resolve().parent
    receipt = json.loads(receipt_path.read_text())
    if (receipt.get("kind") != KIND or receipt.get("schema_version") != 1
            or receipt.get("complete_executable_exact") is not False or receipt.get("input_epoch") != EPOCH):
        raise ValueError("invalid compiler assembly receipt")
    entry = receipt["entry"]
    validate_entry(entry)
    if units is not None and units != [entry["id"]]:
        raise ValueError("compiler assembly receipt has exactly one whole unit")
    context = UnitContext(root)
    config = context.config()
    live = next(row for row in config["units"] if row["id"] == entry["id"])
    frozen = tomllib.loads((work / "exact-units.toml").read_text())
    historical = next(row for row in frozen["units"] if row["id"] == entry["id"])
    if (entry_digest(live) != entry_digest(entry) or entry_digest(historical) != entry_digest(entry)
            or digest(work / "exact-units.toml") != receipt["manifest_sha256"]
            or frozen["artifact"] != context.artifact
            or receipt["mutation"] not in config.get("controls", [])
            or receipt["mutation"] not in frozen.get("controls", [])):
        raise ValueError("compiler assembly source/configuration identity changed")
    tool = json.loads((work / "toolchain-attestation.json").read_text())
    tool_sha, surfaces = static_toolchain(root)
    validate_full_toolchain(tool, tool_sha, surfaces)
    proof = json.loads((work / "toolchain-reuse-proof.json").read_text())
    if (digest(work / "toolchain-attestation.json") != receipt["toolchain_receipt_sha256"]
            or digest(work / "toolchain.toml") != tool_sha or tool_sha != receipt["toolchain_manifest_sha256"]
            or digest(work / "toolchain-reuse-proof.json") != receipt["toolchain_reuse_proof_sha256"]
            or proof["original_full_receipt_sha256"] != receipt["toolchain_receipt_sha256"]
            or proof["manifest_sha256"] != tool_sha or proof["reused"] != receipt["toolchain_reused"]):
        raise ValueError("compiler assembly pinned execution/tool proof changed")
    artifact, target, _ = load_unit_target(context, config)
    if receipt["target_sha256"] != artifact["sha256"]:
        raise ValueError("compiler assembly target changed")
    result = receipt["result"]
    if (result.get("entry_sha256") != entry_digest(entry)
            or receipt["mutation"]["unit"] != entry["id"]):
        raise ValueError("compiler assembly result/control entry identity differs")
    progress.validate_result(entry, result)
    snapshots = scoped_snapshot(root, entry, result, receipt["source_inputs"])
    if result.get("source_inputs") != snapshots:
        raise ValueError("compiler assembly result input scope differs")
    validate_snapshot(root, snapshots)
    validate_snapshot(work / "inputs", snapshots)
    producer_directories(work)
    rows = []
    for name, recorded, mutation in [("a", result["compiler_assembly"][0], None),
                                     ("b", result["compiler_assembly"][1], None),
                                     ("negative", receipt["negative"], receipt["mutation"])]:
        source = work / name / "source"
        validate_producer_inputs(root, source, entry, snapshots, mutation=mutation)
        steps = json.loads((work / name / "commands.json").read_text())
        if len(steps) != 4:
            raise ValueError("compiler assembly requires compiler, assembler, binder and linker commands")
        for row, command in zip(steps, command_lines(root, entry)):
            if row["command"] != command or row["returncode"] != 0 or digest(work / name / row["log"]) != row["log_sha256"]:
                raise ValueError("compiler assembly actual command/log evidence changed")
        observed = observe(source, entry, recorded, target, mutation)
        if observed != recorded:
            raise ValueError("saved compiler assembly artifacts disagree with receipt")
        if required_paths(root, entry, observed["compiler_dependencies"]) != {row["path"] for row in snapshots}:
            raise ValueError("compiler assembly consumed input scope changed")
        rows.append(observed)
    if result["producer_paths"] != ["a/source", "b/source"] or result["rounds"] != [row["comparison"] for row in rows[:2]]:
        raise ValueError("compiler assembly positive producer lineage changed")
    if any(rows[0][key] != rows[1][key] for key in ("map_sha256", "mz_sha256")):
        raise ValueError("compiler assembly MAP/MZ outputs are nondeterministic")
    control = rows[2]["comparison"]
    progress.validate_control(control)
    progress.classify_extent(entry, target_bytes=target.program_image[entry["target_start"]:entry["target_start"] + entry["size"]])
    if receipt["pass"] is not True or result["exact"] is not True:
        raise ValueError("compiler assembly did not pass complete acceptance")
    if validate_only:
        return receipt
    negative = {"unit_id": entry["id"], "entry_sha256": entry_digest(entry),
                "mutation": receipt["mutation"], "control_sha256": entry_digest(receipt["mutation"]),
                "producer_path": "negative/source", "comparison": control,
                "compiler_arguments": arguments(entry), "omf": receipt["negative"]["omf"]}
    imported = {"id": entry["id"], "entry_sha256": entry_digest(entry), "result": result,
                "source_inputs": snapshots, "toolchain_manifest_sha256": tool_sha,
                "toolchain_receipt_sha256": receipt["toolchain_receipt_sha256"],
                "replay_receipt_sha256": digest(receipt_path), "compiled_negative_control": control,
                "negative_control": negative, "receipt_aggregate_pass": True}
    return {"imported": [imported], "target_sha": artifact["sha256"], "tool_sha": tool_sha,
            "replay_sha": digest(receipt_path), "control": control, "target_view": None}

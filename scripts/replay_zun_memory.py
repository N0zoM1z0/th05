#!/usr/bin/env python3
"""Cold replay the complete standalone -M COM child, with ASM origin separate."""
from __future__ import annotations
import argparse
import fcntl
import json
from pathlib import Path
import re
import tomllib
import uuid

from lib.launcher import parse_launcher
from lib.omf import describe_omf
from lib.pc98 import digest_bytes, digest_file
from lib.reference_build import Builder
from lib.replay_toolchain import freeze_toolchain
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/zun_memory.toml"
PUBLIC = ROOT / "config/zun_memory_acceptance.json"


def target_child(config: dict) -> bytes:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    data = read_verified_artifact(ROOT, artifact)
    launcher = parse_launcher(data, expected_sha256=artifact["sha256"])
    member = next(p for p in launcher["payloads"] if p["name"] == config["member"])
    if (member["file_start"], member["size"], member["sha256"]) != (
            config["container_start"], config["size"], config["sha256"]):
        raise ValueError("launcher member disagrees with the reviewed child")
    return data[member["file_start"]:member["file_end"]]


def observe(source: Path, target: bytes, config: dict) -> dict:
    data = (source / "check.com").read_bytes()
    obj = describe_omf((source / "check.obj").read_bytes())
    if not obj["valid"] or obj["translator_comments"] != ["Turbo Assembler  Version 5.0"]:
        raise ValueError("invalid TASM object/producer")
    mapping = (source / "check.map").read_text(encoding="cp437")
    for name, offset in (("MEMORY_CHECK_START", 0x100), ("MEMORY_PRINT_DECIMAL_CHUNK", 0x15f)):
        matches = re.findall(r"^\s*0000:([0-9A-F]{4})\s+(?:idle\s+)?" + name + r"\s*$", mapping, re.M | re.I)
        # TLINK prints each public once in the alphabetical index and once by value.
        if not matches or any(int(value, 16) != offset for value in matches):
            raise ValueError(f"unexpected COM public boundary: {name}")
    code = config["code_bytes"]
    return {"size": len(data), "sha256": digest_bytes(data),
            "raw_exact": data == target,
            "code_exact": data[:code] == target[:code],
            "data_exact": data[code:] == target[code:],
            "code_sha256": digest_bytes(data[:code]), "data_sha256": digest_bytes(data[code:]),
            "object_sha256": obj["sha256"],
            "object_normalized_sha256": obj["dependency_timestamp_normalized_sha256"],
            "object_producers": obj["translator_comments"], "map_sha256": digest_file(source / "check.map")}


def cold_round(work: Path, text: str, target: bytes, config: dict, negative: bool = False) -> dict:
    source = work / "source"
    source.mkdir(parents=True)
    if negative:
        anchor = "MIN_FREE_PARAGRAPHS    equ 32500"
        if text.count(anchor) != 1:
            raise ValueError("negative mutation anchor changed")
        text = text.replace(anchor, "MIN_FREE_PARAGRAPHS    equ 32501")
    (source / "check.asm").write_bytes(text.encode(config["assembler_encoding"]))
    (source / "build_dumb.bat").touch()
    builder = Builder(source, ROOT / ".analysis/toolchain/wineprefix", ROOT / "_reference/ReC98/bin/msdos.exe")
    builder.execute("assemble", ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t", "check.asm", "check.obj"])
    (source / "link.rsp").write_bytes(b"-c -s -t check.obj, check.com, check.map,\r\n")
    builder.execute("link", ["wine", str(builder.msdos), "-e", "-x", "tlink", "@link.rsp"])
    return observe(source, target, config)


def check_public(record: dict, config: dict) -> None:
    if (record["manifest_sha256"] != digest_file(CONFIG)
            or record["toolchain_manifest_sha256"] != digest_file(ROOT / "config/toolchain.toml")
            or record["source_sha256"] != digest_file(ROOT / config["source"])
            or record["origin"] != "inferred-original-handwritten-assembly"
            or record["global_authored_credit"] != "unreviewed"):
        raise ValueError("ASM source, configuration or classification changed")
    rounds = record["rounds"]
    if len(rounds) != 2 or any(not all(r[k] for k in ("raw_exact", "code_exact", "data_exact"))
        or r["sha256"] != config["sha256"] or r["size"] != config["size"] for r in rounds):
        raise ValueError("incomplete full-child cold comparison")
    if (rounds[0]["object_normalized_sha256"] != rounds[1]["object_normalized_sha256"]
            or record["negative_control"]["raw_exact"]
            or record["negative_control"]["sha256"] == config["sha256"]):
        raise ValueError("ASM determinism or compiled negative control failed")


def accept(receipt_path: Path, config: dict) -> None:
    receipt = json.loads(receipt_path.read_text())
    if receipt["manifest_sha256"] != digest_file(CONFIG):
        raise ValueError("unit manifest changed after replay")
    tool_path = receipt_path.parent / "toolchain-attestation.json"
    tool = json.loads(tool_path.read_text())
    if (digest_file(tool_path) != receipt["toolchain_receipt_sha256"]
            or tool["manifest_sha256"] != digest_file(ROOT / "config/toolchain.toml")
            or not all(tool[k] for k in ("ready", "identity_pass", "execution_pass"))):
        raise ValueError("frozen toolchain attestation failed")
    if "toolchain_reuse_proof_sha256" in receipt:
        proof_path = receipt_path.parent / "toolchain-reuse-proof.json"
        if digest_file(proof_path) != receipt["toolchain_reuse_proof_sha256"]:
            raise ValueError("frozen toolchain reuse proof digest disagrees")
        proof = json.loads(proof_path.read_text())
        if (proof["manifest_sha256"] != tool["manifest_sha256"]
                or proof["original_full_receipt_sha256"] != receipt["toolchain_receipt_sha256"]
                or proof["reused"] != receipt["toolchain_reused"]):
            raise ValueError("reuse proof names a different executable toolchain report")
    frozen = receipt_path.parent / "input.asm"
    if digest_file(frozen) != receipt["source_sha256"] or digest_file(ROOT / config["source"]) != receipt["source_sha256"]:
        raise ValueError("maintained or frozen source changed")
    target = target_child(config)
    for index, label in enumerate(("a", "b")):
        if observe(receipt_path.parent / label / "source", target, config) != receipt["rounds"][index]:
            raise ValueError("saved child producer disagrees with its receipt")
    if observe(receipt_path.parent / "negative/source", target, config) != receipt["negative_control"]:
        raise ValueError("saved negative producer disagrees")
    record = {**receipt, "replay_receipt_sha256": digest_file(receipt_path)}
    check_public(record, config)
    PUBLIC.write_text(json.dumps(record, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", type=Path)
    group.add_argument("--accept", type=Path)
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raw_config = CONFIG.read_bytes()
    config = tomllib.loads(raw_config.decode())
    if args.check:
        check_public(json.loads(PUBLIC.read_text()), config)
        print("PASS: standalone -M payload acceptance is source-current; ASM origin remains inferred")
        return 0
    if args.accept:
        accept(args.accept, config)
        print("PASS: complete standalone -M payload accepted; global authored classification remains unreviewed")
        return 0
    if args.output is None and PUBLIC.exists():
        try:
            check_public(json.loads(PUBLIC.read_text()), config)
        except (OSError, ValueError, KeyError):
            pass
        else:
            print("No source or configuration changes; retained -M acceptance reused without executing tools")
            return 0
    target = target_child(config)
    source_bytes = (ROOT / config["source"]).read_bytes()
    text = source_bytes.decode(config["source_encoding"])
    work = (args.output or ROOT / ".analysis/zun-memory" / uuid.uuid4().hex).resolve()
    if work.exists():
        parser.error("cold replay requires a fresh output directory")
    work.mkdir(parents=True)
    (work / "input.asm").write_bytes(source_bytes)
    (work / "unit.toml").write_bytes(raw_config)
    with (ROOT / ".analysis/borland.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        tool = freeze_toolchain(ROOT, work / "toolchain-attestation.json")
        rounds = [cold_round(work / label, text, target, config) for label in ("a", "b")]
        negative = cold_round(work / "negative", text, target, config, negative=True)
    receipt = {"schema_version": 1, "kind": "standalone-zun-memory-com-replay",
               "manifest_sha256": digest_bytes(raw_config),
               "source_sha256": digest_bytes(source_bytes),
               "toolchain_manifest_sha256": digest_file(ROOT / "config/toolchain.toml"),
               "toolchain_receipt_sha256": digest_file(work / "toolchain-attestation.json"),
               "toolchain_reused": tool["reused"],
               "toolchain_reuse_proof_sha256": tool["proof_sha256"],
               "origin": config["origin"], "global_authored_credit": config["global_authored_credit"],
               "rounds": rounds, "negative_control": negative}
    check_public(receipt, config)
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS: two cold complete {config['size']}-byte COM outputs and compiled negative; {work / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

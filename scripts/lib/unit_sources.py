"""Canonical UTF-8 inputs and explicitly encoded compiler staging bytes."""
from __future__ import annotations
import hashlib
from pathlib import Path

from .replay_toolchain import bindings_source, include_closure


def source_encoding(entry: dict) -> str:
    encoding = entry.get("source_encoding", "raw")
    if encoding not in ("raw", "cp932"):
        raise ValueError("source_encoding must be raw or cp932")
    return encoding


def encoded_input(raw: bytes, encoding: str, *, path: str, mutation: dict | None = None) -> bytes:
    if mutation and mutation["source"] == path:
        text = raw.decode("utf-8")
        if not mutation["find"] or text.count(mutation["find"]) != 1 or mutation["find"] == mutation["replace"]:
            raise ValueError("compiled negative-control mutation anchor drifted")
        raw = text.replace(mutation["find"], mutation["replace"]).encode("utf-8")
    if encoding == "raw":
        return raw
    if encoding != "cp932":
        raise ValueError("unsupported source encoding")
    return raw.decode("utf-8").encode("cp932")


def stage_inputs(inputs: Path, producer: Path, units: list[dict], paths: set[str], *, mutation: dict | None = None) -> None:
    if mutation and mutation["source"] not in paths:
        raise ValueError("negative-control source is outside the staged input scope")
    modes = {name: set() for name in paths}
    for entry in units:
        encoding = source_encoding(entry)
        for name in include_closure(inputs, entry["source"]):
            modes[name].add(encoding)
        for name in include_closure(inputs, bindings_source(entry)):
            modes[name].add("raw")
    for name in sorted(paths):
        raw = (inputs / name).read_bytes()
        versions = {encoded_input(raw, encoding, path=name, mutation=mutation)
                    for encoding in modes[name] or {"raw"}}
        if len(versions) != 1:
            raise ValueError(f"shared compiler input has conflicting source encodings: {name}")
        destination = producer / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(versions.pop())


def producer_input_path(producer: Path, entry: dict, name: str) -> Path:
    path = producer / name
    if not path.is_file() and name == bindings_source(entry):
        path = producer / "bindings.asm"  # Historical scaffold archive spelling.
    return path


def producer_snapshot(producer: Path, entry: dict, snapshots: list[dict]) -> list[dict]:
    return [{"path": item["path"], "sha256": hashlib.sha256(
        producer_input_path(producer, entry, item["path"]).read_bytes()).hexdigest()}
        for item in snapshots]


def validate_producer_inputs(canonical: Path, producer: Path, entry: dict, snapshots: list[dict], *, mutation: dict | None = None) -> None:
    cpp_paths = include_closure(canonical, entry["source"])
    encoding = source_encoding(entry)
    for item in snapshots:
        name = item["path"]
        raw = (canonical / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("canonical UTF-8 source snapshot changed")
        expected = encoded_input(raw, encoding if name in cpp_paths else "raw", path=name, mutation=mutation)
        if producer_input_path(producer, entry, name).read_bytes() != expected:
            raise ValueError(f"saved compiler input disagrees with canonical {encoding} staging: {name}")
        if name == bindings_source(entry):
            assembled = producer / "bindings.asm"
            if assembled.is_file() and assembled.read_bytes() != expected:
                raise ValueError("assembled bindings.asm alias disagrees with canonical binding bytes")

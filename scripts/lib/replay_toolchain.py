"""Incremental replay identities, real include scopes and frozen probe reuse.

This module never treats a cached report as current without rehashing every
required installed surface. Frozen executable-probe evidence is copied intact.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tomllib

from .toolchain import attest_surface, tree_identity


DEFAULT_BINDINGS = "probes/units/main_bindings.asm"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry_digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def relative_path(value: str) -> str:
    value = value.replace("\\", "/")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"input path escapes the repository: {value}")
    return path.as_posix()


def bindings_source(entry: dict) -> str:
    return relative_path(entry.get("bindings_source", DEFAULT_BINDINGS))


def _includes(path: Path) -> list[tuple[str, bool]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".asm", ".inc"):
        return [(m[1].strip('"\''), False) for m in re.finditer(
            r"(?im)^\s*(?:include|incbin)\s+([^;\s]+)", text)]
    # C comments do not introduce dependencies; literal directives in inactive
    # branches are a staging superset, refined by actual OMF dependencies.
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    result = []
    for line in text.splitlines():
        if not re.match(r"\s*#\s*include\b", line):
            continue
        match = re.match(r'\s*#\s*include\s*(["<])([^">]+)[">]', line)
        if not match:
            raise ValueError(f"unsupported computed include in {path}")
        result.append((match[2], match[1] == "<"))
    return result


def include_closure(root: Path, initial: str) -> set[str]:
    pending = [relative_path(initial)]
    found: set[str] = set()
    root = root.resolve()
    while pending:
        name = pending.pop()
        if name in found:
            continue
        path = root / name
        try:
            path.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"include resolves outside the repository: {name}") from error
        if not path.is_file():
            raise ValueError(f"missing maintained include: {name}")
        found.add(name)
        for include, system in _includes(path):
            include = include.replace("\\", "/")
            if PurePosixPath(include).is_absolute() or re.match(r"^[A-Za-z]:", include):
                raise ValueError(f"absolute include is outside maintained source: {include}")
            options = ([root / include] if system else [path.parent / include, root / include])
            candidate = next((item for item in options if item.is_file()), None)
            if candidate is None:
                if system:
                    # Vendor includes are covered by the frozen tool surfaces,
                    # and their actual paths are checked in the OMF cross-check.
                    continue
                raise ValueError(f"unresolved maintained include {include} from {name}")
            try:
                local = candidate.resolve().relative_to(root).as_posix()
            except ValueError as error:
                raise ValueError(f"include resolves outside repository: {include}") from error
            pending.append(local)
    return found


def semantic_generators(root: Path, entry: dict, compiler_paths: set[str]) -> set[str]:
    """Pin and check explicitly declared generators of actual compiler inputs.

    A generator is maintained evidence, not a compiler dependency invented by
    an inactive include. Its output must already belong to the real input
    closure. Both files are frozen, and --check must leave the output intact.
    """
    rows = entry.get("generated_sources", [])
    if not isinstance(rows, list):
        raise ValueError("generated_sources must be a list")
    generators, outputs = set(), set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"generator", "output"}:
            raise ValueError("generated source needs exactly generator/output")
        if not all(isinstance(value, str) and value for value in row.values()):
            raise ValueError("generated source paths must be nonempty strings")
        generator, output = (relative_path(row[key]) for key in ("generator", "output"))
        script = root / generator
        if (not generator.startswith("scripts/") or not generator.endswith(".py")
                or script.is_symlink() or not script.is_file()
                or not script.resolve().is_relative_to(root.resolve())):
            raise ValueError("generator must be a maintained local Python script")
        if output not in compiler_paths or output in outputs or generator in generators:
            raise ValueError("generated output must be a unique actual compiler input")
        prior, script_prior = digest(root / output), digest(script)
        try:
            checked = subprocess.run([sys.executable, str(script.resolve()), "--check"],
                cwd=root, capture_output=True, timeout=10)
        except subprocess.TimeoutExpired as error:
            raise ValueError("semantic generator check timed out") from error
        if checked.returncode or digest(root / output) != prior or digest(script) != script_prior:
            raise ValueError("semantic generator output is stale or --check modified it")
        generators.add(generator)
        outputs.add(output)
    return generators


def staged_paths(root: Path, entry: dict) -> set[str]:
    source = include_closure(root, entry["source"])
    return source | include_closure(root, bindings_source(entry)) | semantic_generators(root, entry, source)


def compiler_dependencies(entry: dict, omfs: list[dict]) -> set[str]:
    rounds = []
    for omf in omfs:
        names = set()
        wrapper_seen = False
        for raw in omf["dependency_paths"]:
            normalized = raw.replace("\\", "/")
            if normalized.casefold().startswith("c:/tc4/include/"):
                continue
            normalized = relative_path(normalized)
            if normalized.casefold() == entry["module"].casefold():
                wrapper_seen = True
                continue
            names.add(normalized)
        if not wrapper_seen or entry["source"] not in names:
            raise ValueError("compiler dependencies omit wrapper or maintained unit source")
        rounds.append(names)
    if not rounds or any(names != rounds[0] for names in rounds[1:]):
        raise ValueError("cold compiler dependency closures disagree")
    return rounds[0]


def required_input_paths(root: Path, entry: dict, result: dict) -> set[str]:
    actual = compiler_dependencies(entry, result["omfs"])
    scanned = include_closure(root, entry["source"])
    if not actual.issubset(scanned):
        raise ValueError("OMF contains maintained dependencies omitted by include scanning")
    return (actual | include_closure(root, bindings_source(entry))
            | semantic_generators(root, entry, actual))


def scoped_snapshot(root: Path, entry: dict, result: dict, snapshots: list[dict]) -> list[dict]:
    """Trim legacy whole-tree snapshots using recorded real compiler dependencies."""
    known = {}
    for item in snapshots:
        path = bindings_source(entry) if item["path"] == "main_bindings.asm" else relative_path(item["path"])
        if path in known:
            raise ValueError("duplicate source snapshot path")
        known[path] = item["sha256"]
    required = required_input_paths(root, entry, result)
    if not required.issubset(known):
        raise ValueError("source snapshot omits maintained compiler dependencies or bindings")
    return [{"path": name, "sha256": known[name]} for name in sorted(required)]


def validate_snapshot(root: Path, snapshots: list[dict]) -> None:
    for item in snapshots:
        if digest(root / relative_path(item["path"])) != item["sha256"]:
            raise ValueError(f"accepted source changed: {item['path']}")


def snapshot_paths(root: Path, paths: set[str]) -> list[dict]:
    return [{"path": path, "sha256": digest(root / path)} for path in sorted(paths)]


def static_toolchain(root: Path) -> tuple[str, list[dict]]:
    path = root / "config/toolchain.toml"
    config = tomllib.loads(path.read_text())
    surfaces = [row for row in config["surfaces"]
                if row.get("required", True) and not row.get("bootstrap_only")]
    observed = [attest_surface(root, row) for row in surfaces]
    if not surfaces or any(not row["pass"] for row in observed):
        raise ValueError("required toolchain surfaces fail static identity; execution is forbidden")
    # The manifest pins canonical installed headers/libraries. TURBOC.CFG uses
    # independent C: copies, so those actual compiler inputs must agree too.
    canonical = {row["id"]: row for row in surfaces}
    for suffix, directory in (("include", "INCLUDE"), ("lib", "LIB")):
        original = canonical.get("tc40j-" + suffix)
        if original is None:
            continue
        active = root / config["paths"]["wine_prefix"] / "drive_c/TC4" / directory
        identity = tree_identity(active)
        if identity.sha256 != original["sha256"] or identity.file_count != original["file_count"]:
            raise ValueError(f"active TC4 {directory} differs from the pinned installed tree")
        observed.append({"id": "active-tc40j-" + suffix, "derived_from": original["id"],
                         "path": str(active.relative_to(root)), "required": True, "pass": True,
                         "actual_sha256": identity.sha256, "expected_sha256": original["sha256"],
                         "file_count": identity.file_count, "total_size": identity.total_size})
    return digest(path), observed


def validate_full_toolchain(report: dict, manifest_sha: str, surfaces: list[dict]) -> None:
    if report.get("manifest_sha256") != manifest_sha or not all(
            report.get(key) is True for key in ("ready", "identity_pass", "execution_pass")):
        raise ValueError("cached executable toolchain attestation is stale or incomplete")
    if report.get("execution", {}).get("pass") is not True:
        raise ValueError("cached toolchain report lacks successful executable probes")
    recorded = {row["id"]: row for row in report.get("surfaces", [])}
    selected = set(report.get("selected_surface_ids", []))
    for current in surfaces:
        if current.get("derived_from"):
            # This additional static proof is frozen separately; never insert
            # it into a historical executable-probe receipt.
            continue
        old = recorded.get(current["id"], {})
        if (current["id"] not in selected or not old.get("pass") or
                old.get("actual_sha256") != current["actual_sha256"] or
                old.get("expected_sha256") != current["expected_sha256"]):
            raise ValueError("cached toolchain report omits or disagrees with a required surface")


def freeze_toolchain(root: Path, destination: Path, *, allow_probes: bool = True) -> dict:
    """Reuse unchanged executable evidence, or run full probes after static identity.

    The caller serializes Wine writers. A source report is copied byte-for-byte;
    its timestamp and manifest identity are never rewritten as current evidence.
    """
    manifest_sha, surfaces = static_toolchain(root)
    current = root / ".analysis/toolchain/attestation.json"
    reused = True
    try:
        report = json.loads(current.read_text())
        validate_full_toolchain(report, manifest_sha, surfaces)
    except (OSError, ValueError, KeyError, TypeError):
        if not allow_probes:
            raise ValueError("full executable toolchain probes are required; reuse was rejected")
        subprocess.run([sys.executable, str(root / "scripts/attest_toolchain.py")], check=True)
        reused = False
        manifest_sha, surfaces = static_toolchain(root)
        report = json.loads(current.read_text())
        validate_full_toolchain(report, manifest_sha, surfaces)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(current, destination)
    if json.loads(destination.read_text()) != report:
        raise ValueError("toolchain report changed while freezing it")
    proof = {"schema_version": 1, "reused": reused, "manifest_sha256": manifest_sha,
             "original_full_receipt_sha256": digest(destination),
             "active_context": [row for row in surfaces if row.get("derived_from")],
             "required_surface_sha256": {row["id"]: row["actual_sha256"] for row in surfaces}}
    proof_path = destination.with_name("toolchain-reuse-proof.json")
    proof_path.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    return {"reused": reused, "manifest_sha256": manifest_sha,
            "receipt_sha256": digest(destination), "report": report,
            "proof_sha256": digest(proof_path),
            "required_surface_sha256": {row["id"]: row["actual_sha256"] for row in surfaces}}

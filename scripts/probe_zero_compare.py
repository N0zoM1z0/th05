#!/usr/bin/env python3
"""Probe one signed coordinate zero comparison with pinned TC86 -S.

Sixteen tiny, serial compilations; no link, emulator, product mutation, or exact
credit. The TH04 probe_tc4_score_rotate_intrinsics.py establishes TCC -S support.
Run through run_heavy; a valid unchanged full toolchain receipt is required.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

from lib.pc98 import parse_mz
from lib.reference_build import Builder
from lib.replay_toolchain import digest, freeze_toolchain
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
BASE_FLAGS = ("-S", "-I.", "-b-", "-3", "-d", "-DGAME=5", "-ml", "-DBINARY='M'")
PROFILES = (("O-Z", ("-O", "-Z")), ("O-Zminus", ("-O", "-Z-")),
            ("noO-Z", ("-Z",)), ("noO-Zminus", ("-Z-",)))
ZEROS = {
    "literal": ("", "0"),
    "typed": ("", "static_cast<pixel_t>(0)"),
    "local-const": ("    const pixel_t clip_zero = 0;\n", "clip_zero"),
    "enum": ("    enum { clip_zero = 0 };\n", "clip_zero"),
}
TARGET_START = 0x10D1A
TARGET_BYTES = bytes.fromhex("81f9a0017d0a3d00007e053d80017c0e")
MAX_ASM_BYTES = 65536
MAX_BODY_LINES = 160


def source_text(variant: str) -> str:
    declaration, zero = ZEROS[variant]
    return ('''// Local codegen experiment, not reconstructed product source.
#pragma option -zCZERO_TEXT -zPmain_01
#include <dos.h>
typedef signed short pixel_t;
extern "C" int near zero_compare(pixel_t top_in, pixel_t left_in)
{
''' + declaration + '''    _AX = top_in;
    _CX = left_in;
#define left static_cast<pixel_t>(_CX)
#define top static_cast<pixel_t>(_AX)
    if ((left > (32 - 16)) && (left < 416) &&
        (top > ''' + zero + ''') && (top < 384)) {
        return 1;
    }
    return 0;
#undef top
#undef left
}
''')


def is_zero(operand: str) -> bool:
    return bool(re.fullmatch(r"(?:0+|0+h|0x0+)", operand, re.I))


def inspect_asm(text: str) -> dict:
    """Read the one emitted function, without mistaking symbols for immediates."""
    lines = text.splitlines()
    start = [i for i, line in enumerate(lines)
             if re.match(r"^\s*_zero_compare\s+proc\b", line, re.I)]
    end = [i for i, line in enumerate(lines)
           if re.match(r"^\s*_zero_compare\s+endp\b", line, re.I)]
    if len(start) != 1 or len(end) != 1 or end[0] <= start[0]:
        raise ValueError("TC86 zero_compare PROC/ENDP boundary drift")
    body = lines[start[0] + 1:end[0]]
    if len(body) > MAX_BODY_LINES:
        raise ValueError("generated probe body exceeds the bounded inspection limit")
    instructions = []
    for number, line in enumerate(body, start[0] + 2):
        clean = line.split(";", 1)[0].strip()
        if not clean or clean.endswith(":") or clean.startswith(("?", ".")):
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9]*)\s*(.*)", clean)
        if not match:
            raise ValueError(f"unexpected generated assembly at line {number}: {clean}")
        op = match[1].lower()
        if op in {"assume", "align", "public", "local", "label"}:
            continue
        args = re.sub(r"\s+", "", match[2]).lower()
        instructions.append({"line": number, "mnemonic": op, "operands": args})
    sites = []
    for index, instruction in enumerate(instructions):
        op, args = instruction["mnemonic"], instruction["operands"]
        fields = args.split(",")
        form = None
        if op == "cmp" and len(fields) == 2 and fields[0] == "ax" and is_zero(fields[1]):
            form = "cmp-ax-zero"
        elif op in {"or", "test"} and args == "ax,ax":
            form = op + "-ax-ax"
        if form:
            following = instructions[index + 1] if index + 1 < len(instructions) else None
            sites.append({"form": form, "instruction": instruction, "following": following,
                          "followed_by_jle": bool(following and following["mnemonic"] == "jle")})
    selected = [site["form"] for site in sites if site["followed_by_jle"]]
    return {"body_lines": body, "instructions": instructions, "zero_test_sites": sites,
            "lower_bound_forms": selected, "emits_cmp_ax_zero_jle": "cmp-ax-zero" in selected}


def compile_case(work: Path, variant: str, profile: str, options: tuple[str, ...],
                 *, root: Path = ROOT, builder_factory=Builder) -> dict:
    work.mkdir(parents=True)
    source = work / "source"
    source.mkdir()
    (source / "build_dumb.bat").touch()
    (source / "zero.cpp").write_text(source_text(variant), encoding="ascii")
    builder = builder_factory(source, root / ".analysis/toolchain/wineprefix",
                              root / "_reference/ReC98/bin/msdos.exe")
    flags = [*BASE_FLAGS, *options]
    command = ["wine", str(builder.msdos), "-e", "-x", "tcc", *flags, "zero.cpp"]
    row = {"variant": variant, "profile": profile, "flags": flags,
           "source_sha256": digest(source / "zero.cpp"), "steps": builder.records}
    try:
        builder.execute("compile-asm", command)
        candidates = [path for path in source.iterdir() if path.name.lower() == "zero.asm"]
        if len(candidates) != 1:
            raise ValueError("expected exactly one generated zero.asm")
        asm = candidates[0]
        if not 0 < asm.stat().st_size <= MAX_ASM_BYTES:
            raise ValueError("generated assembly is empty or exceeds the bounded limit")
        row.update({"assembly_sha256": digest(asm),
                    "assembly_path": asm.relative_to(work).as_posix(),
                    "inspection": inspect_asm(asm.read_text(encoding="cp437")), "pass": True})
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        row.update({"pass": False, "error": str(error)[:3000]})
    # Hash logs even for failed compiler invocations. All full files stay private.
    row["artifacts"] = [{"path": path.relative_to(work).as_posix(), "sha256": digest(path),
                         "size": path.stat().st_size}
                        for path in sorted(work.rglob("*")) if path.is_file()]
    return row


def comparison_table(rows: list[dict]) -> str:
    lines = ["# Signed zero comparison experiment", "",
             "Compiler-generated assembly only; no Boss BG exactness claim.", "",
             "| Zero spelling | Flags | Lower-bound zero test before JLE | Result |",
             "|---|---|---|---|"]
    for row in rows:
        forms = ", ".join(row.get("inspection", {}).get("lower_bound_forms", [])) or "other / inspect ASM"
        lines.append(f"| {row['variant']} | {row['profile']} | {forms} | "
                     + ("compiled" if row["pass"] else "failed") + " |")
    return "\n".join(lines) + "\n"


def run(output: Path, *, root: Path = ROOT) -> dict:
    output = output.resolve()
    output.relative_to((root / ".analysis").resolve())
    output.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": 1, "claim_scope": "TC86 signed zero-comparison codegen only",
               "boss_bg_exact": False, "raw_replay_required": True,
               "method": "TCC -S (no assembler, linker, or executable invocation)",
               "matrix_size": len(ZEROS) * len(PROFILES), "results": [],
               "context_limit": "Small signed _AX/_CX clipping context, not the full particle renderer",
               "noO_meaning": "-O omitted; installed TURBOC.CFG is frozen, not rewritten"}
    try:
        with (root / ".analysis/borland.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            receipt["toolchain"] = freeze_toolchain(root, output / "toolchain-attestation.json",
                                                   allow_probes=False)
            shutil.copyfile(root / "config/toolchain.toml", output / "toolchain.toml")
            cfg = root / ".analysis/toolchain/wineprefix/drive_c/TC4/BIN/TURBOC.CFG"
            receipt["active_compiler_config"] = {"sha256": digest(cfg), "text": cfg.read_text(encoding="cp437")}
            # An omitted -O is meaningful only if no hidden default enables it.
            if any(re.match(r"\s*-O", line, re.I) for line in receipt["active_compiler_config"]["text"].splitlines()):
                raise ValueError("active TURBOC.CFG supplies an optimizer option; noO profile is ambiguous")
            shutil.copyfile(cfg, output / "TURBOC.CFG")
            manifest = root / "config/targets.toml"
            artifact = find_artifact(load_target_manifest(manifest), "th05-main")
            target_raw = read_verified_artifact(root, artifact)
            target = parse_mz(target_raw)
            if not target.valid or target.program_image[TARGET_START:TARGET_START + len(TARGET_BYTES)] != TARGET_BYTES:
                raise ValueError("pinned original zero-comparison target context drifted")
            receipt["target"] = {"artifact": "th05-main", "sha256": hashlib.sha256(target_raw).hexdigest(),
                                 "manifest_sha256": digest(manifest), "load_start": TARGET_START,
                                 "bytes_hex": TARGET_BYTES.hex(), "comparison_load": 0x10D20,
                                 "comparison": "CMP AX,0; JLE reject"}
            receipt["script_sha256"] = digest(Path(__file__))
            receipt["implementation_sha256"] = {name: digest(root / name) for name in
                ("scripts/lib/reference_build.py", "scripts/lib/replay_toolchain.py", "scripts/lib/toolchain.py")}
            for variant in ZEROS:
                for profile, options in PROFILES:
                    case = output / f"{variant}-{profile}"
                    row = compile_case(case, variant, profile, options, root=root)
                    row["directory"] = case.relative_to(output).as_posix()
                    receipt["results"].append(row)
            receipt["pass"] = all(row["pass"] for row in receipt["results"])
            receipt["cmp_candidates"] = [f"{row['variant']}/{row['profile']}" for row in receipt["results"]
                                         if row.get("inspection", {}).get("emits_cmp_ax_zero_jle")]
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        receipt.update({"pass": False, "error": str(error)[:3000]})
    (output / "comparison.md").write_text(comparison_table(receipt["results"]))
    receipt["comparison_sha256"] = digest(output / "comparison.md")
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--plan", action="store_true", help="print the matrix without running tools")
    args = parser.parse_args()
    if args.plan:
        print(json.dumps({"tools_executed": False, "matrix": [
            {"variant": variant, "profile": profile, "flags": [*BASE_FLAGS, *flags]}
            for variant in ZEROS for profile, flags in PROFILES]}, indent=2))
        return 0
    output = args.output or ROOT / ".analysis/compiler-probes" / ("zero-compare-" + uuid.uuid4().hex)
    receipt = run(output)
    print(json.dumps({"output": str(output.resolve()), "pass": receipt["pass"],
                      "compiled": len(receipt["results"]), "cmp_candidates": receipt.get("cmp_candidates", []),
                      "toolchain_reused": receipt.get("toolchain", {}).get("reused"),
                      "error": receipt.get("error"), "boss_bg_exact": False}, indent=2))
    return 0 if receipt["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

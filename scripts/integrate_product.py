#!/usr/bin/env python3
"""Replace ReC98 dump procedures in a built product tree with accepted units.

Run on the `source/` directory of a `build_reference.py --overlay` build; the
tree is edited in place and the product EXE relinked. See
`scripts/lib/product_integration.py` for the method.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from lib.product_integration import (Integration, asm_failed, TLINK_DUPLICATE, TLINK_UNDEFINED, UNDEFINED_ASM,
                                     base_name)
from lib.omf_edit import externs, publics, rename_externs
import build_reference

ROOT = Path(__file__).resolve().parents[1]
TASM_FLAGS = ["/m", "/mx", "/kh32768", "/t", "/dGAME=5"]


def runner(source: Path):
    env = {**os.environ, "WINEPREFIX": str(ROOT / ".analysis/toolchain/wineprefix"), "WINEDEBUG": "-all",
           "MSDOS_PATH": r"C:\TC4\BIN"}
    logs = source.parent / "logs"
    logs.mkdir(exist_ok=True)

    def run(label: str, command: list[str], check: bool = True) -> str:
        result = subprocess.run(command, cwd=source, env=env, capture_output=True, timeout=600)
        text = (result.stdout + result.stderr).decode("cp437", errors="replace")
        (logs / f"{label}.log").write_text(json.dumps(command) + "\n" + text)
        if check and result.returncode:
            raise RuntimeError(f"{label} failed:\n{text[-2000:]}")
        return text
    return run


def integrate(source: Path, artifact: str, rounds: int = 12) -> dict:
    overlaid = {s["reference_path"] for s in tomllib.loads(
        (ROOT / "config/maintained_sources.toml").read_text())["sources"] if s["artifact"] == artifact}
    run = runner(source)
    job = Integration(ROOT, source, artifact, run, TASM_FLAGS, overlaid)
    job.compile_modules()
    renames: dict[str, dict[str, str]] = {}
    product_publics: dict[str, str] = {}
    for attempt in range(rounds):
        job.marker()
        if not product_publics:
            product_publics = {base_name(n): n for n in job.addresses}
        job.plan()
        originals = {p: p.read_bytes() for p in job.files}
        for module, mapping in renames.items():
            job.objects[module] = rename_externs(job.objects[module], mapping)
        job.apply()
        failed = job.apply_cxx()
        if failed:
            job.restore_cxx()
            for path, raw in originals.items():
                path.write_bytes(raw)
            for module, cuts in job.cxx_cuts.items():
                for tu, _ in cuts:
                    if tu in failed:
                        job.excluded[module] = f"{tu}: {failed[tu]}"
            job.log.append(f"round {attempt}: C++ cuts failed: {failed}")
            continue
        out = job.assemble(job.dump_obj, f"dump-asm-{attempt}")
        missing = {m[3] for m in UNDEFINED_ASM.finditer(out)}
        if asm_failed(out):
            for path, raw in originals.items():
                path.write_bytes(raw)
            job.restore_cxx()
            if not missing:
                raise RuntimeError("dump assembly failed:\n" + out[-3000:])
            job.extra_labels |= missing
            job.log.append(f"round {attempt}: dump labels referenced from outside: {sorted(missing)}")
            continue
        anchor = build_reference.code_order_anchor(artifact, job.segments_for_anchor())
        (source / "anchor.asm").write_text(anchor)
        run("anchor", ["wine", r"C:\TASM50\bin\TASM32.EXE", "/m", "/mx", "/t", "anchor.asm", "obj\\th05\\anchor.obj"])
        objects = " ".join(m.obj for m in job.modules if m.module in job.removals)
        exe, map_path = f"bin\\th05\\{artifact}.exe", f"obj\\th05\\{artifact}.map"
        (source / exe.replace("\\", "/")).unlink(missing_ok=True)
        out = job.link(f"link-{attempt}", objects, exe, map_path)
        undefined = [(m[1], m[2]) for m in TLINK_UNDEFINED.finditer(out)]
        duplicate = [(m[1], m[2], m[3]) for m in TLINK_DUPLICATE.finditer(out)]
        problems = re.findall(r"(?m)^(?:Error|Warning|Fatal):.*$", out)
        if not problems and (source / exe.replace("\\", "/")).exists():
            (source / f"bin/th05/{artifact}.rsp").write_bytes((source / f"bin/th05/link-{attempt}.rsp").read_bytes())
            break
        for path, raw in originals.items():
            path.write_bytes(raw)
        job.restore_cxx()
        ours = {Path(m.obj.replace("\\", "/")).stem.lower(): m for m in job.modules}
        progressed = False
        for symbol, module in undefined:
            stem = Path(module.replace("\\", "/")).stem.lower()
            if stem in ours:
                module = ours[stem].module
                spelled = job.extern_name(module, symbol)
                target = spelled and (job.resolve(module, spelled) or job.dump_name(spelled)
                                      or product_publics.get(base_name(spelled)))
                if target:
                    if target != spelled:
                        renames.setdefault(module, {})[spelled] = target
                    if job.dump_name(target):
                        job.publicize.add(target)
                else:
                    job.excluded[module] = f"unresolved {symbol}"
                progressed = True
            else:
                job.extra_labels.add(symbol)
                progressed = True
        for symbol, left, right in duplicate:
            for module in (left, right):
                stem = Path(module.replace("\\", "/")).stem.lower()
                if stem in ours:
                    job.excluded[ours[stem].module] = f"duplicate {symbol}"
                    progressed = True
        job.log.append(f"round {attempt}: {len(undefined)} undefined, {len(duplicate)} duplicate, "
                       f"{len(problems)} problems")
        if not progressed:
            raise RuntimeError("link failed without a recoverable diagnosis:\n" + out[-3000:])
    else:
        raise RuntimeError("integration did not converge:\n" + "\n".join(job.log))
    units = [u for m in job.modules if m.module in job.removals for u in m.units]
    cut = sorted({tu for cuts in job.cxx_cuts.values() for tu, _ in cuts})
    return {"artifact": artifact, "integrated_modules": len(job.removals), "integrated_units": units,
            "removed_procedures": sorted(p.name for ps in job.removals.values() for p in ps),
            "cut_cxx_functions": sorted(n for cs in job.cxx_cuts.values() for _, names in cs for n, _ in names),
            "cut_cxx_units": cut,
            "excluded": job.excluded, "skipped": {k: len(v) for k, v in job.skipped.items()},
            "renamed_externs": renames, "log": job.log}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--artifact", choices=["main", "maine"], required=True)
    args = parser.parse_args()
    report = integrate(args.source.resolve(), args.artifact)
    (args.source.parent / "integration.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in report.items()
                      if k not in ("excluded", "renamed_externs", "log")}, indent=2))
    print(f"excluded {len(report['excluded'])}; log:", *report["log"], sep="\n  ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

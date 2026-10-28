#!/usr/bin/env python3
"""Lightweight exact-state checks; --full also runs tooling regression tests."""
import argparse
import ast
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def full_checks() -> int:
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT)
    if result.returncode:
        return result.returncode
    if (ROOT / "config/master_vendor_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master.py", "--structural-check"], cwd=ROOT, check=True)
    if (ROOT / "config/master_vendor_additions.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_additions.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/master_sin8_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_sin8.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/master_egc_shifts_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_egc_shifts.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/master_ems_transfers_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_ems_transfers.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/master_primary_circlefill_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_primary_circlefill.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/master_primary_circlex_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_master_primary_circlex.py", "--structural-check"],
                       cwd=ROOT, check=True)
    for context in ("op", "maine"):
        if (ROOT / f"config/vendor_ownership.{context}.json").exists():
            subprocess.run([sys.executable, "scripts/review_vendor_context.py", "--context", context,
                            "--structural-check"], cwd=ROOT, check=True)
    if (ROOT / "config/vendor_data_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_vendor_data.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/main_runtime_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_main_runtime.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/string_runtime_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_string_runtime.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/accepted_units.json").exists():
        subprocess.run([sys.executable, "scripts/progress.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/zun_memory_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_zun_memory.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/text_fx_data_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_text_fx_data.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/text_fx_render_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_text_fx_render.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/reviewed_text_fx_asm_units.json").exists():
        subprocess.run([sys.executable, "scripts/review_text_fx_asm.py", "--structural-check"], cwd=ROOT, check=True)
    if (ROOT / "config/enemy_vm_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_enemy_vm.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/accepted_asm_families.json").exists():
        subprocess.run([sys.executable, "scripts/replay_asm_family.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "resources/ownership.json").exists():
        subprocess.run([sys.executable, "scripts/ownership.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/font_resource.json").exists():
        subprocess.run([sys.executable, "scripts/review_font_resource.py"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("PASS: public source/configuration validation")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="also run all tooling tests and specialized metadata checks")
    args = parser.parse_args()
    for path in sorted((ROOT / "scripts").rglob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
    for path in (ROOT / "config").glob("*.toml"):
        tomllib.loads(path.read_text())
    if args.full:
        return full_checks()
    for script in ("progress.py", "ownership.py"):
        subprocess.run([sys.executable, "scripts/" + script, "--check"],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("PASS: exact source/configuration, progress and ownership checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

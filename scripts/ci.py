#!/usr/bin/env python3
"""Public validation; never needs proprietary games or compilers."""
import ast
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for path in sorted((ROOT / "scripts").rglob("*.py")):
        ast.parse(path.read_text(), filename=str(path))
    for path in (ROOT / "config").glob("*.toml"):
        tomllib.loads(path.read_text())
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
    for context in ("op", "maine"):
        if (ROOT / f"config/vendor_ownership.{context}.json").exists():
            subprocess.run([sys.executable, "scripts/review_vendor_context.py", "--context", context,
                            "--structural-check"], cwd=ROOT, check=True)
    if (ROOT / "config/vendor_data_ownership.json").exists():
        subprocess.run([sys.executable, "scripts/review_vendor_data.py", "--structural-check"],
                       cwd=ROOT, check=True)
    if (ROOT / "config/accepted_units.json").exists():
        subprocess.run([sys.executable, "scripts/progress.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/zun_memory_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_zun_memory.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "config/text_fx_data_acceptance.json").exists():
        subprocess.run([sys.executable, "scripts/replay_text_fx_data.py", "--check"], cwd=ROOT, check=True)
    if (ROOT / "resources/ownership.json").exists():
        subprocess.run([sys.executable, "scripts/ownership.py", "--check"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("PASS: public source/configuration validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

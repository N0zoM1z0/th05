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
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("PASS: public source/configuration validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

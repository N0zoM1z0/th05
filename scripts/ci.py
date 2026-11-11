#!/usr/bin/env python3
"""Fast public checks for the complete checkout, without private build inputs."""
from pathlib import Path
import ast
import json
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def public_files():
    names = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).split(b"\0")
    names = sorted({name for name in names if name})
    # --no-index also catches private files accidentally force-added to Git.
    ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "--stdin", "-z"],
        input=b"\0".join(names) + b"\0", cwd=ROOT, stdout=subprocess.PIPE, check=False
    )
    if ignored.returncode not in (0, 1):
        raise RuntimeError("git check-ignore failed")
    if ignored.stdout:
        raise ValueError("private/generated files in public tree: " +
                         ", ".join(name.decode() for name in ignored.stdout.split(b"\0") if name))
    return [ROOT / name.decode() for name in names]


def main():
    if sys.argv[1:] in (["--help"], ["-h"]):
        print("usage: ci.py [--full]\nDefault: complete public-tree syntax, ledgers, build configuration and private-file checks.\n--full: explicitly run the broad tooling suite.")
        return 0
    if len(sys.argv) > 1:
        if sys.argv[1:] != ["--full"]:
            print("Unknown CI option; use no arguments or --full.", file=sys.stderr)
            return 2
        return subprocess.call([sys.executable, str(ROOT / "scripts/ci-full.py"), "--full"], cwd=ROOT)
    for path in public_files():
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=str(path.relative_to(ROOT)))
        elif path.suffix == ".json":
            json.loads(path.read_text())
        elif path.suffix == ".toml":
            tomllib.loads(path.read_text())
        elif path.suffix == ".sh":
            subprocess.run(["bash", "-n", str(path)], check=True)
    for script in ("progress.py", "ownership.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), "--check"],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Lightweight source-current acceptance check for the separate ZUN.COM
    # -I child; no assembler, Wine, original target or cold replay is invoked.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_interrupt.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    print("PASS: public-tree syntax, ledgers, build configuration and private-file checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

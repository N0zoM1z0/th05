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
    # Static-only CL.LIB review of two large CODE SEGDEFs. Their 8 runtime
    # CS: placeholders are deliberately unowned, not zero-filled source.
    subprocess.run([sys.executable, str(ROOT / "scripts/review_vendor_reserved.py"), "--structural-check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Source-backed original CL setenvp CODE; the original data group is
    # eighteen bytes below the calibration's, and _DATA/_INIT_ remain unknown.
    subprocess.run([sys.executable, str(ROOT / "scripts/review_main_setenvp.py"), "--structural-check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # The original C0L CRT contributes 144 initialized DATA bytes, resolved
    # from its real _BSSEND FIXUPP; no other game DATA or CODE is claimed.
    subprocess.run([sys.executable, str(ROOT / "scripts/review_main_c0_data.py"), "--structural-check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # OP and MAINE each contain complete CL farheap/exec CODE SEGDEFs with
    # eight original unwritten CS: state bytes. Adopt actual OMF writes only.
    for context in ("op", "maine"):
        subprocess.run([sys.executable, str(ROOT / "scripts/review_context_reserved.py"),
                        "--context", context, "--structural-check"],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, str(ROOT / "scripts/review_context_remaining.py"),
                        "--context", context, "--structural-check"],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, str(ROOT / "scripts/review_maine_shifted_vendor.py"),
                    "--structural-check"],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    # Lightweight source-current acceptance check for the separate ZUN.COM
    # -I child; no assembler, Wine, original target or cold replay is invoked.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_interrupt.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # -G embeds 8192 reviewed font bytes, not authored code. Only verify its
    # source-current ledger here: no original game, Wine or asset is loaded.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_gaiji.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Only inspect the recorded -O member/OMF boundaries; no game or native
    # toolchain is loaded by this lightweight source-current check.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_adpcm.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # The inner ZUN dispatcher owns only 558 bytes, with proof-only zero ORG
    # placeholders for five children. Lightweight check never replays children.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_dispatcher.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Only 71 outer COMCSTM instruction bytes and 300 header/text bytes belong
    # to this wrapper. The 17,745-byte inner COM remains a foreign zero hole.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_outer.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # The vendor resident-data family is a narrow -S code owner, not the
    # whole unaccepted 6564-byte resident executable or authored C++.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_resdata.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # Four complete original Master buffered-file near functions within the
    # -S child; this source-current check does no native rebuild.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_file_native.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    # C0T startup: real Borland vendor CODE/DATA source-owned OMF, with the
    # two-byte writable CS: word still unclaimed; no native compile in CI.
    subprocess.run([sys.executable, str(ROOT / "scripts/replay_zun_crt.py"), "--check"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    print("PASS: public-tree syntax, ledgers, build configuration and private-file checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

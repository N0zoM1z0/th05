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



def check_public_ownership():
    """Without private inputs, check the committed inventory is self-consistent."""
    from collections import Counter
    data = json.loads((ROOT / "resources/ownership.json").read_text())
    total = Counter()
    for name, view in data["views"].items():
        cursor, counts = 0, Counter()
        for row in view["intervals"]:
            if row["start"] != cursor or row["end"] <= row["start"]:
                raise ValueError(f"ownership view {name} is not gapless at {cursor:#x}")
            counts[row["kind"]] += row["end"] - row["start"]
            cursor = row["end"]
        if cursor != view["size"] or dict(sorted(counts.items())) != view["byte_counts"]:
            raise ValueError(f"ownership view {name} counts disagree with its intervals")
        total.update(counts)
    if dict(sorted(total.items())) != data["byte_counts"]:
        raise ValueError("ownership totals disagree with the views")
    exact = sum(v for k, v in total.items() if k.startswith("accepted-"))
    if (data["authored_exact_bytes"] != exact or
            data["authored_denominator"] != exact + total["unknown"] or
            data["percentage"] != round(100 * exact / data["authored_denominator"], 3)):
        raise ValueError("published authored percentage disagrees with the inventory")

# Structural checks of the reviewed vendor, runtime, ASM and ZUN decisions.
# None of them loads an original game, Wine or a native toolchain.
STRUCTURAL = [
    ["review_vendor_reserved.py", "--structural-check"],      # CL.LIB CS: placeholders stay unowned
    ["review_main_setenvp.py", "--structural-check"],
    ["review_main_shifted_vendor.py", "--structural-check"],
    ["review_main_c0_data.py", "--structural-check"],         # C0L CRT's 144 DATA bytes
    ["review_main_atan8_data.py", "--structural-check"],
    ["review_main_master_literal_tables.py", "--structural-check"],
    ["review_main_runtime.py", "--structural-check"],
    ["review_main_sprites.py", "--structural-check"],
    ["review_main_bfnt_entry.py", "--structural-check"],
    ["review_maine_shifted_vendor.py", "--structural-check"],
    ["review_master.py", "--structural-check"],
    ["review_master_additions.py", "--structural-check"],
    ["review_master_super.py", "--structural-check"],
    ["review_master_super_helpers.py", "--structural-check"],
    ["review_master_bgm.py", "--structural-check"],
    ["review_master_grcg.py", "--structural-check"],
    ["review_master_circle_helpers.py", "--structural-check"],
    ["review_master_gap_functions.py", "--structural-check"],
    ["review_master_io.py", "--structural-check"],
    ["review_master_machine.py", "--structural-check"],
    ["review_master_pf.py", "--structural-check"],
    ["review_master_sin8.py", "--structural-check"],
    ["review_master_egc_shifts.py", "--structural-check"],
    ["review_master_ems_transfers.py", "--structural-check"],
    ["review_master_primary_circlefill.py", "--structural-check"],
    ["review_master_primary_circlex.py", "--structural-check"],
    *[[script, "--context", context, "--structural-check"]
      for context in ("op", "maine")
      for script in ("review_context_reserved.py", "review_context_remaining.py",
                     "review_context_string_runtime.py", "review_vendor_context.py")],
    ["review_context_pi_pack.py", "--structural-check"],
    ["review_context_master_large.py", "--structural-check"],
    ["review_context_super_helpers.py", "--structural-check"],
    ["review_context_master_hooks.py", "--structural-check"],
    ["review_context_graph_pack_noclip.py", "--structural-check"],
    ["review_context_bgm_timers.py", "--structural-check"],
    ["review_context_memory_vsync.py", "--structural-check"],
    ["review_context_machine_detect.py", "--structural-check"],
    ["review_vendor_data.py", "--structural-check"],
    ["review_string_runtime.py", "--structural-check"],
    ["review_text_fx_asm.py", "--structural-check"],
    ["review_font_resource.py"],
    ["replay_text_fx_data.py", "--check"],
    ["replay_text_fx_render.py", "--check"],
    ["replay_enemy_vm.py", "--check"],
    ["replay_asm_family.py", "--check"],
    # ZUN.COM children: source-current ledgers only, no native rebuild.
    ["replay_zun_interrupt.py", "--check"],
    ["replay_zun_gaiji.py", "--check"],
    ["replay_zun_adpcm.py", "--check"],
    ["replay_zun_dispatcher.py", "--check"],
    ["replay_zun_outer.py", "--check"],
    ["replay_zun_resdata.py", "--check"],
    ["replay_zun_file_native.py", "--check"],
    ["replay_zun_crt.py", "--check"],
    ["replay_zun_memory.py", "--check"],
]


def run_script(*args):
    subprocess.run([sys.executable, str(ROOT / "scripts" / args[0]), *args[1:]],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def main():
    if sys.argv[1:] in (["--help"], ["-h"]):
        print("usage: ci.py [--full]\nDefault: complete public-tree syntax, ledgers, build configuration and private-file checks.\n--full: also run the tooling tests in tests/.")
        return 0
    if sys.argv[1:] not in ([], ["--full"]):
        print("Unknown CI option; use no arguments or --full.", file=sys.stderr)
        return 2
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
    run_script("progress.py", "--check")
    if (ROOT / ".analysis").is_dir():
        # Rebuilding the inventory re-reads private originals and calibrations.
        run_script("ownership.py", "--check")
    else:
        check_public_ownership()
    for args in STRUCTURAL:
        run_script(*args)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
    if sys.argv[1:] == ["--full"]:
        tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-q", "-s", "tests"], cwd=ROOT)
        if tests.returncode:
            return tests.returncode
    print("PASS: public-tree syntax, ledgers, build configuration and private-file checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

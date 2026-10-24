#!/usr/bin/env bash
# Acquire and install the exact locally calibrated Borland candidate surfaces.
# Proprietary binaries remain below ignored .analysis/ and are never committed.
set -euo pipefail
export DISPLAY=""
export WAYLAND_DISPLAY=""

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
private_root="$repo_root/.analysis/toolchain"
prefix="$private_root/wineprefix"
drive_c="$prefix/drive_c"
tc_media="$private_root/media/tc40j/software/borland-4.0j"
tc_install="$private_root/installed/tc40j"
tasm_archive="$private_root/downloads/borland-tasm-5.0-3.5-144mb-candidate.7z"
tasm_media="$private_root/media/tasm50"
tasm_install="$private_root/installed/tasm50"
stage="$drive_c/TH05INST"
msdos="$repo_root/_reference/ReC98/bin/msdos.exe"

# Reuse an attested sibling installation without sharing writable Wine state.
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "usage: $0 [--from SIBLING_REPOSITORY]"
    exit 0
fi
if [[ "${1:-}" == "--from" ]]; then
    if [[ $# != 2 ]]; then
        echo "usage: $0 [--from SIBLING_REPOSITORY]" >&2
        exit 2
    fi
    python3 - "$repo_root" "$2" <<'PY_REUSE'
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib

root = Path(sys.argv[1]).resolve()
source = Path(sys.argv[2]).expanduser().resolve()
if source == root:
    raise SystemExit("source and destination repositories must differ")
sys.path.insert(0, str(root / "scripts"))
from lib.toolchain import attest_surface

config = tomllib.loads((root / "config/toolchain.toml").read_text())
surfaces = [row for row in config["surfaces"] if not row.get("bootstrap_only")]
checks = [attest_surface(source, row) for row in surfaces]
failed = [row["id"] for row in checks if row["required"] and not row["pass"]]
if failed:
    raise SystemExit("sibling tool identity failed: " + ", ".join(failed))
final = root / ".analysis/toolchain"
if final.exists() or final.is_symlink():
    raise SystemExit(f"refusing to overlay existing installation: {final}")
final.parent.mkdir(parents=True, exist_ok=True)
source_prefix = source / str(config["paths"]["wine_prefix"])
# Reflink when supported, independent copied files otherwise. Never hard-link
# Wine registry, Windows files, compiler config or writable build state.
def copy_entry(src, dst):
    subprocess.run(["cp", "-a", "--reflink=auto", "--", str(src), str(dst)], check=True)

with tempfile.TemporaryDirectory(prefix="toolchain-stage-", dir=final.parent) as tmp:
    stage = Path(tmp) / "toolchain"
    prefix = stage / "wineprefix"
    drive_c = prefix / "drive_c"
    drive_c.mkdir(parents=True)
    for name in ("system.reg", "user.reg", "userdef.reg", ".update-timestamp"):
        src = source_prefix / name
        if src.is_file():
            copy_entry(src, prefix / name)
    for name in ("windows", "Program Files", "Program Files (x86)",
                 "ProgramData", "users", "TC4", "TASM50"):
        src = source_prefix / "drive_c" / name
        if src.is_dir():
            copy_entry(src, drive_c / name)
    devices = prefix / "dosdevices"
    devices.mkdir()
    (devices / "c:").symlink_to("../drive_c")
    (devices / "z:").symlink_to("/")
    (stage / "installed").mkdir()
    for name in ("tc40j", "tasm50"):
        src = source / ".analysis/toolchain/installed" / name
        if src.is_dir():
            copy_entry(src, stage / "installed" / name)
    copied = []
    for row in surfaces:
        relative = Path(str(row["path"]))
        try:
            suffix = relative.relative_to(".analysis/toolchain")
        except ValueError:
            continue
        staged_row = {**row, "path": suffix.as_posix()}
        copied.append(attest_surface(stage, staged_row))
    failed = [row["id"] for row in copied if row["required"] and not row["pass"]]
    if failed:
        raise SystemExit("copied tool identity failed: " + ", ".join(failed))
    (stage / "reuse-receipt.json").write_text(json.dumps({
        "schema_version": 1, "source_repository": str(source),
        "copy_mode": "independent-reflink-or-copy", "source_surfaces": checks,
        "copied_surfaces": copied, "execution_performed": False,
    }, indent=2, sort_keys=True) + "\n")
    stage.rename(final)
print("Independent TH05 Wine/compiler installation copied; no Wine was executed.")
PY_REUSE
    python3 "$repo_root/scripts/attest_toolchain.py" --identity-only
    echo "Run python3 scripts/attest_toolchain.py serially for executable probes."
    exit 0
elif [[ $# != 0 ]]; then
    echo "usage: $0 [--from SIBLING_REPOSITORY]" >&2
    exit 2
fi

for command in curl wget 7z mcopy wine wineboot sha512sum python3; do
	command -v "$command" >/dev/null || {
		echo "missing required command: $command" >&2
		exit 1
	}
done
test "$(uname -m)" = x86_64 || {
	echo "the automatic toolchain bootstrap currently supports only x86_64 hosts" >&2
	exit 1
}
test -f "$msdos" || {
	echo "missing pinned ReC98 clone; run the README reference-clone command" >&2
	exit 1
}
for destination in "$tc_media" "$tc_install" "$tasm_media" "$tasm_install" "$prefix"; do
	if test -e "$destination"; then
		echo "refusing to overlay existing path: $destination" >&2
		echo "move the partial installation aside and retry" >&2
		exit 1
	fi
done

mkdir -p "$private_root/downloads" "$private_root/media/tc40j" "$private_root/installed"

# Turbo C++ 4.0J: mirror the complete flat installation directory.  The
# mirror has no independently published digest, so the checked-in tree digest,
# Japanese/PC-98 files, banners, probes, and cold builds all remain mandatory.
wget --no-host-directories --no-parent --recursive --level=1 \
	--accept='*.PAK,*.DSK,*.TXT,README,*.EXE,*.COM' \
	--directory-prefix="$private_root/media/tc40j" \
	'http://pc98.shiz.me/software/borland-4.0j/'

# TASM 5.0: validate WinWorld's independently published SHA-512 before use.
curl --fail --location --output "$tasm_archive" \
	'https://winworldpc.com/download/30487b55-c392-c592-11c3-a6c2bb2a5254/from/c39ac2af-c381-c2bf-1b25-11c3a4e284a2'
expected_tasm_sha512=0580f14adbb785e43ee3b057a5ec0417b3206b26fba4bda034140e7d6aa4947634dcbe167f337de2942fb4a3e3515e9eb829d6b666d31a64afe442111a070061
actual_tasm_sha512=$(sha512sum "$tasm_archive" | cut -d' ' -f1)
test "$actual_tasm_sha512" = "$expected_tasm_sha512" || {
	echo "TASM archive SHA-512 mismatch" >&2
	exit 1
}

# Before invoking UNPAK.EXE, MS-DOS Player, Wine, or archive extraction, require
# every acquisition/runner surface already present at this phase to match the
# checked-in manifest. A download URL or successful transfer is not identity.
python3 "$repo_root/scripts/attest_toolchain.py" --identity-only \
	--surface tc40j-media \
	--surface tasm50-archive \
	--surface msdos-player-p0281 \
	--output "$private_root/acquisition-attestation.json"

7z t "$tasm_archive"
mkdir -p "$tasm_media"
7z x -y "$tasm_archive" "-o$tasm_media"

# Use a project-local Wine prefix and DOS-visible short paths.  The Borland
# DPMI loader fails with error 0000 from the repository's deep Z: path.
mkdir -p "$prefix"
WINEPREFIX="$prefix" WINEDEBUG=-all wineboot -u
mkdir -p "$drive_c/TC4/BIN" "$drive_c/TC4/INCLUDE/SYS" \
	"$drive_c/TC4/LIB" "$drive_c/TC4/SOURCE/STARTUP" \
	"$drive_c/TASM50/bin" "$stage/tc" "$stage/tasm/disk1" "$stage/tasm/disk2"

cp "$tc_media/UNPAK.EXE" "$stage/tc/UNPAK.EXE"
for pak in BIN CMDLINE GENINC GENSYS CLIB SLIB MLIB LLIB HLIB EMU TLIB XLIB STARTUP; do
	cp "$tc_media/$pak.PAK" "$stage/tc/$pak.PAK"
done
run_unpak() {
	local archive=$1
	local destination=$2
	(
		cd "$stage/tc"
		WINEPREFIX="$prefix" WINEDEBUG=-all wine "$msdos" \
			-e -x UNPAK.EXE x "$archive.PAK" "$destination"
	)
}
run_unpak BIN 'C:\TC4\BIN'
run_unpak CMDLINE 'C:\TC4\BIN'
run_unpak GENINC 'C:\TC4\INCLUDE'
run_unpak GENSYS 'C:\TC4\INCLUDE\SYS'
for pak in CLIB SLIB MLIB LLIB HLIB EMU TLIB XLIB; do
	run_unpak "$pak" 'C:\TC4\LIB'
done
run_unpak STARTUP 'C:\TC4\SOURCE\STARTUP'

# Extract the command-line 32-bit Windows assembler from disk 2's CMD32.PAK.
tasm_disk_root="$tasm_media/Borland Turbo Assembler 5.0 (3.5-1.44mb)"
mcopy -s -o -i "$tasm_disk_root/disk01.img" '::*' "$stage/tasm/disk1"
mcopy -s -o -i "$tasm_disk_root/disk02.img" '::*' "$stage/tasm/disk2"
cp "$stage/tasm/disk1/UNPAK.EXE" "$stage/tasm/UNPAK.EXE"
cp "$stage/tasm/disk2/CMD32.PAK" "$stage/tasm/CMD32.PAK"
(
	cd "$stage/tasm"
	WINEPREFIX="$prefix" WINEDEBUG=-all wine "$msdos" \
		-e -x UNPAK.EXE x CMD32.PAK 'C:\TASM50\bin'
)

# Preserve a runner-independent canonical copy as well as the active C: copy.
mkdir -p "$tc_install" "$tasm_install/bin"
cp -a "$drive_c/TC4/." "$tc_install/"
cp "$drive_c/TASM50/bin/TASM32.EXE" "$tasm_install/bin/TASM32.EXE"
cp "$repo_root/probes/toolchain/TURBOC.CFG" "$drive_c/TC4/BIN/TURBOC.CFG"
cp "$repo_root/probes/toolchain/TLINK.CFG" "$drive_c/TC4/BIN/TLINK.CFG"

python3 "$repo_root/scripts/attest_toolchain.py"

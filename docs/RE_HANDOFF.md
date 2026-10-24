# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
The project is newly initialized; no authored units are accepted yet.
Public repository: https://github.com/N0zoM1z0/th05 .

The user's supplied Japanese image is accessible through WSL. Public
`config/targets.toml` pins its identity and four KAIKI executables. The image
digest differs from TH04's outer Japanese image, while all four TH05 executable
hashes agree with its calibration corpus. Original assets remain private.

Borland tools have an independent Wine prefix and pass identity plus executable
compiler/assembler/linker/OMF/determinism probes. Ghidra 12.1.3 and Temurin
21.0.12.1+1 pass installed identity checks. MAIN's `TH05-main-loader` project
passes independent database attestation, including all bytes and relocations.
Full automatic analysis hit the 768 MiB cgroup limit; use loader-only imports
and bounded analysis. The failed project is not accepted evidence.
TH05 MAIN is ordinary MZ (4032-byte header, 998 relocations); OP/MAINE are
DIET-packed MZ. ZUN is plain COM.

Independent DIET observation passes at two load segments for OP/MAINE. See
`python3 scripts/unpack_targets.py`; payloads/receipts are in `.analysis/decoded`.
MAIN's first pinned-reference calibration build completes 83 serial steps but
does not match original layout or bytes. It creates no authored credit.

Next: ownership denominator and bounded authored function cold replay. Player
angle and bullet tuning have local C++ sources and full local ABI declarations;
their exact replay is being established independently of the failed whole-file
calibration. No whole-program or standalone build claim is made.

TH03 has unrelated uncommitted work; do not modify it. TH04 is a read-only
reference. Use an independent Wine prefix and serialize heavy jobs.

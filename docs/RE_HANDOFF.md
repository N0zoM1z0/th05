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
21.0.12.1+1 pass installed identity checks; database import remains pending.
TH05 MAIN is ordinary MZ (4032-byte header, 998 relocations); OP/MAINE are
DIET-packed MZ. ZUN is plain COM.

Next: finish Ghidra import, independent DIET decoder validation, ownership
denominator and bounded authored function cold replay. MAIN calibration uses
the pinned reference only as a linking scaffold; it creates no authored credit.

TH03 has unrelated uncommitted work; do not modify it. TH04 is a read-only
reference. Use an independent Wine prefix and serialize heavy jobs.

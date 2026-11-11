# MAIN EGC interpage-copy setup: exact hardware-register C++

`egc_start_copy_noframe()` is the complete 63-byte near routine at MAIN
`[BC2E,BC6D)`. It initializes the PC-98 GRCG/EGC copy path using the real
register interface: disables GRCG mode at port `7C`, selects registers through
port `6A`, enables the correct mode, and writes the EGC mask, raster, and
copy-control WORD values through ports `4A0`, `4A2`, `4A4`, `4A8`, `4AC`, and
`4AE`. It has no input parameters, owned DATA/BSS, table or MZ relocations.
The following `BC6D` NOP is outside this function and receives no credit.

The maintained Borland C++ source uses compiler-visible `_AX`/`_AL`/`_DX`
register intrinsics and semantic `OUT` instructions for hardware port writes.
One native source-level `MOV AX,0` is kept explicit rather than the default
C++ zero-assignment lowering to `XOR AX,AX`, so both the required hardware
register value and the native instruction width are retained. No instruction
bytes, copied original image, switch table or synthetic DATA are supplied.
The separate EGC tile renderer calls this actual near provider; it is not
recompiled or re-counted here.

Full focused receipt:
`.analysis/unit-replays/gpt-web-main-egc-copy-setup-a/receipt.json`.
Two fresh deterministic TCC/TLINK producers match the complete 63 original
bytes and empty ordered fixup stream at CS `AE1`, DGROUP `209D`; the compiled
negative changes the EGC mode from `80h` to `C0h` and is rejected. This is a
bounded source-backed C++/hardware-intrinsic recovery; literal historical
source language remains uncertain because the pinned modern ReC98 names its
macro inside an ASM tile renderer.

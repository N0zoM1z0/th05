# General BB loader: exact original-language ASM, inexact C++ candidate

The complete native MAIN function is F930..F967, 55 instruction bytes, near
Pascal with one four-byte far filename argument and RET4. The following NOP
is outside this body. It returns a two-byte segment handle in AX. The sole
original ordered MZ fixup is relative 7 at the real far allocation call.

A natural C++ body uses the actual 2048-byte allocation, foreign scratch segment
at DS 4204 and direct DOS open/read/close calls, all unchecked. It retains the
full far-filename and segmented-result API. The maintained candidate snapshots
SP after the near-Pascal allocator has removed its argument, then loads the far
filename from `SS:[BX+4]`; this avoids the compiler's unnecessary BP frame.

Two independent native producers emit the original **55-byte extent** and the
original far-call relocation at relative offset **7**. The maintained C++ now
matches **51/55** original bytes: `_BX = _SP` produces the exact `8B DC` stack
snapshot, while the far filename and all DOS transfer operations remain
source-level. The only remaining four-byte difference is the compiler's
mandatory return-value load before its saved-SI epilogue (`mov ax,[4204]; pop si`)
instead of the original order (`pop si; mov ax,[4204]`). This is an ABI return
lowering difference, not a wrong filename offset, extent, or relocation.
Both fresh producers have identical bytes and normalized OMF. The C++ candidate
remains an inexact context provider with no additional CODE credit; the exact
55-byte original-ASM owner remains authoritative. Evidence:
`.analysis/gpt-web-bb-load-sp-intrinsic-results-20261113.json`.
The BB text lifecycle has its own [independent exact acceptance](bb_text.md).

## Complete original 55-byte ASM recovery — 2026-11-10

`BB_LOAD` is now a reviewed original-assembly source owner at `[F930,F967)`,
recovering **55/55 native instruction bytes** through two independent real
TASM32/TLINK producers, the original single allocator far-call relocation at
relative offset **7**, and a compiled negative that changes the real DOS read
length from 2048 to 2047. The genuine ReC98
`th05/formats/bb_load.asm` preserves the original 16-bit near-Pascal register
sequence and unchecked DOS file access semantics.

The function pushes SI, allocates exactly 2048 bytes through the actual far
`HMEM_ALLOCBYTE`, saves the returned segment at the foreign DS `4204` word,
then snapshots the caller stack in BX. With SI retaining the original DS, the
far filename is loaded from `SS:[BX+4]` into `DS:DX`, followed by DOS
`INT 21h` open (3D00h), read (AH=3Fh) and close (AH=3Eh). It restores the
original DS and SI, loads the segment handle into AX and returns with
`RET 4`. There is no allocation-failure branch, file-open error handling or
additional memory ownership. The original 0x90 after the function is outside
this complete function and is not credited.

The maintained source is `bb_load.asm`, with named semantic constants in
`bb_load_types.inc`, external symbol declarations in
`probes/units/bb_load_symbols.inc` and the existing source-free physical
binder. It emits no DATA or BSS. Receipt:
`.analysis/gpt-web-main-bb-load-asm-first-a/receipt.json`.
The 55 bytes gain **reviewed ASM instruction credit**. The natural C++
context candidate remains inexact; no additional C++ ownership is inferred.

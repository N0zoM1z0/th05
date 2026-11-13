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
## 2026-11-13: return-order source experiments

The exact four-byte tail difference was isolated with fresh, focused native
producers. The original ends `POP SI; MOV AX,[bb_load_seg]; RET 4`; the current
C++ candidate ends `MOV AX,[bb_load_seg]; POP SI; RET 4`. The 55-byte extent,
`+7` relocation and all preceding instructions remain intact. The compiler
loads a C++ return expression before its callee-saved SI epilogue, which is the
only observed difference in the retained candidate.

New source variants changed `original_ds` from `register` to an ordinary local,
then to `volatile`; tested explicit `-O` and `-O-`; and inserted a zero-code
barrier before/around the return. The ordinary local and both optimization
profiles preserve the same 51/55 output. `volatile` forces a 61-byte BP-frame
implementation. The tested barrier declaration is rejected by this BB
translation unit's current TCC configuration (`storage class inline not
allowed here`). Manual SI save/restore variants produce a duplicate
compiler-managed SI save, while DS-on-stack variants lose the original
prologue/stack-argument layout. None improves the four-byte tail. Results are
retained in `.analysis/gpt-web-bb-load-return-order-experiments-20261113.json`
and `.analysis/gpt-web-bb-load-return-barrier-experiments-20261113.json`.

The C++ translation unit now asserts the actual four-byte far filename
argument and 2,048-byte payload; the shared header already asserts the
two-byte near segment result. This pins the `SS:[BX+4]` source assumption at
compile time without changing generated instructions. No
additional code ownership is claimed; the complete 55-byte reviewed ASM
family remains the sole exact owner.

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

## 2026-11-13: post-allocation DS-stack alternative

A fresh C++ shape experiment avoids SI entirely by pushing the **post-
`hmem_allocbyte()` DS** after the allocator returns. That one-word stack save
still places the far filename at `SS:[BX+4]`. After DOS open returns the handle
in AX, the candidate moves it to BX, pops DS to restore the allocator's DS,
then pushes that same DS again before switching DS to the allocated buffer.
After read and close it pops DS once more, leaving caller SI untouched and
letting the compiler load the segment return value without a saved-SI
epilogue.

Two independent actual cold native producers emit the same complete **51-byte**
shape and OMF. Its far allocator relocation moves to relative offset **6**
(instead of the native **7**), and only four byte positions match the original
at their same offsets. This is a useful source-level DS-lifetime alternative,
not an exact reconstruction and not an improvement over the maintained
51/55-byte natural candidate, which preserves 51 original byte positions and
the native relocation. The diagnostic was not emulator-executed and receives
zero CODE credit. The maintained C++ context provider and the exact 55-byte
reviewed ASM owner are unchanged.

Evidence:
`.analysis/gpt-web-bb-load-post-alloc-ds-stack-a-20261113/native-diagnostic.json`
and
`.analysis/gpt-web-bb-load-post-alloc-ds-stack-b-20261113/native-diagnostic.json`.

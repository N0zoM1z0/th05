# BB loader natural C++ candidate experiments

This file records C++-only source experiments and is deliberately separate from the accepted ASM owner notes, which are inputs to the frozen reviewed-ASM receipt.

## 2026-11-13: scoped register lifetime and explicit-save follow-up

Moving the existing `original_ds` register local into a nested block does not
move Borland's saved-SI restore ahead of scalar return-value materialization.
The fresh 55-byte candidate retains the original `+7` allocator relocation
and every preceding instruction, but its final four bytes remain
`MOV AX,[bb_load_seg]; POP SI` rather than the native `POP SI; MOV AX,[bb_load_seg]`.
The compiler treats SI as a function-level callee-saved register even after
the source local's block ends. Evidence:
`.analysis/gpt-web-bb-load-scoped-register-lifetime-a-20261113/`.

Manual SI push/pop around a `_SI` pseudoregister use makes the compiler add a
second SI save/restore; that candidate grows to 62 bytes. Saving the original
DS through ES also grows the complete contribution to 66 bytes and duplicates
the return load. These alternatives do not improve the maintained 51/55-byte
C++ source and are not promoted. The complete reviewed 55-byte ASM owner
remains the only exact credited implementation.

## 2026-11-13: stack-preserved DS alternative

A fresh C++/DOS-intrinsic variant replaces the compiler-managed SI copy with
an explicit one-word DS save around the file operation. Moving `push ds`
*before* the near-Pascal allocation keeps the far allocator call at the
original relocation offset **+7**. After the allocator removes its argument,
`BX = SP` still addresses the filename at `SS:[BX+4]`. The code opens with the
original DGROUP, switches DS to the allocated 2,048-byte payload for read and
close, then restores DS with `pop ds` before returning the segment handle.

The actual one-producer result is a complete **49-byte** contribution with
ordered fixups `[7]`. It is not raw exact: it uses `PUSH DS` rather than the
original `PUSH SI`, omits the original `MOV SI,DS`/`MOV DS,SI` preservation
sequence, and is six bytes shorter than the native 55-byte function. It does,
however, retain the original far-call relocation coordinate and the true
stack-argument address without a BP frame. The post-allocation `push ds`
variant instead moved the fixup to `+6`; moving the save before allocation
corrects that one coordinate. A separate explicit-SI hybrid attempt emitted
57 bytes because TC++ added its own callee-saved SI pair around the inline
save/restore. None of these is an acceptance producer or receives CODE
credit; the reviewed 55-byte ASM owner remains authoritative.

One-producer diagnostic:
`.analysis/gpt-web-bb-load-stack-ds-before-allocation-a-20261113/`.

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

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

## 2026-11-13 correction: stack-preserved DS candidate and follow-up probes

The earlier 49-byte `push ds` candidate preserved the original far-allocator
relocation at **+7** and addressed the filename at `SS:[BX+4]`, but a later
semantic re-read found a critical DS error. `LDS DX,SS:[BX+4]` changes DS to
the filename segment. After DOS open, the candidate moved the returned handle
to BX and immediately loaded `bb_load_seg` through `[4204]` without first
restoring DGROUP. That absolute load therefore reads from the filename
segment, not the game's DS. Its final `pop ds` occurs only after the payload
read/close and cannot repair the earlier wrong segment access. The 49-byte
result is a compiler-shape diagnostic with fixup `[7]`, **not a valid semantic
candidate**; the prior paragraph's claim that it correctly switches to the
payload segment is withdrawn.

Two corrected stack-preservation directions were compiled:

- Mirroring the saved original DS into ES, restoring DS from ES immediately
after open, and then loading the allocated payload emits **57 bytes** with
  fixup `[7]`. It uses `MOV AX,DS; MOV ES,AX` and `MOV AX,ES; MOV DS,AX`,
  rather than the original two-byte `MOV SI,DS` / `MOV DS,SI` sequence. This
  still fails raw comparison and additionally depends on ES surviving the
  DOS calls, which this experiment did not independently establish.
- Keeping a stack anchor in BP, restoring DS from `SS:[BP]`, and preserving
  BP/DS emits **58 bytes** with fixup `[8]`; the extra saved BP shifts the
  allocator relocation away from its native +7 coordinate.

Neither corrected candidate is accepted. The maintained natural C++ source
remains the **51/55-byte** candidate with the real SI-held DS restoration;
the complete reviewed **55-byte original ASM** remains the sole exact CODE
owner. Evidence for the original 49-byte diagnostic, the 57-byte ES variant
and the 58-byte BP variant is retained in:

- `.analysis/gpt-web-bb-load-stack-ds-before-allocation-a-20261113/`
- `.analysis/gpt-web-bb-load-es-stack-save-a-20261113/`
- `.analysis/gpt-web-bb-load-bp-stack-anchor-a-20261113/`

No new code credit or acceptance is claimed.

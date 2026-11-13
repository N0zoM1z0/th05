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


## 2026-11-13: explicit inline-SI preservation

A hybrid C++/inline-ASM attempt removed the C++ `register original_ds` local
and made the save/restore boundary explicit:

```cpp
asm { push si; mov si, ds; }
// DOS open/read/close remains ordinary C++ and intrinsic calls.
asm { mov ds, si; pop si; }
return bb_load_seg;
```

It was compiled both with and without a forward declaration carrying
`#pragma aux bb_load = modify [si]`. Turbo C++ 4.02 still recognizes SI as a
callee-saved register used by the inline-ASM body and emits its own additional
save/restore. Both variants produce **57 bytes** with duplicate `PUSH SI` at
entry and duplicate `POP SI` at return. Moving the pragma before the header
prototype also does not suppress the compiler-managed pair; that variant is
57 bytes with the original +7 relocation but has the same duplicate save.
None is accepted.

## 2026-11-13: stack-only DS lifetime and manual epilogue probes

A stack-only alternative was compiled in two source spellings. It snapshots
`SP` after the near-Pascal allocator cleanup, saves original DS with `PUSH DS`,
loads the filename through the saved stack base, restores DS after DOS open,
saves it again while DS addresses the allocated payload, and restores it after
read/close. Both spellings produce **51 bytes** with the allocator relocation
at **+6**, not the native **+7**. They avoid SI and preserve the original DS
across the DOS calls, but omit the native initial `PUSH SI` / `MOV SI,DS`
sequence and do not reproduce the complete function. The two variants match
only two bytes at the same offsets; they are not a byte-level improvement over
the existing 51/55 candidate.

A manual `POP SI; MOV AX,[bb_load_seg]; RET 4` epilogue was also tried. The
inline assembler cannot resolve the C++ variable's `_bb_load_seg` spelling
directly. Using the reviewed absolute DS slot instead causes Turbo C++ to
allocate the saved DS in DI, retain another callee-save pair and grow the
contribution to **61 bytes** with relocation +8. No inline epilogue variant
is accepted.

The remaining natural-C++ issue is still specifically the order of the return
load and the compiler-managed callee-save epilogue. The original 55-byte ASM
owner remains exact and authoritative; no new DATA, CODE or partial credit is
claimed.

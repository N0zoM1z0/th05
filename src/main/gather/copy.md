# Gather template copy: exact original-register ASM; ordinary C++ still inexact

The near Pascal helper MAIN16F70..16F8B is a complete 27-byte procedure,
taking one near gather reference and returning with RET2. It copies the full
14-byte bullet_template at DS577E into the gather's member at offset24.
Its original ordered MZ fixup stream is empty. ReC98 b6ba5b0a gather.cpp
describes the same operation with copy_near_struct_member; the existing
maintained gather/BulletTemplate declarations assert all fields and extents.

The ordinary struct assignment in copy_to_bullet.cpp emits a valid 27-byte
Borland object, but its bytes differ: it pushes far source and destination
pointers and calls F_SCOPY@. The native helper instead saves SI/DI, sets ES=DS
and copies seven WORDs with REP MOVSW. Equal size grants no acceptance.
The normal focused replay stops at the unresolved real F_SCOPY@ dependency;
no placeholder provider, second producer, negative or behavior model was added.
The proposal is outside the live manifest. The neighboring reverse copy is
not recompiled, and neither procedure gains C++ or ASM credit from this trial.

The complete object diagnostic is `.analysis/gather-copy-to-natural-review.json`,
which records the failed link and source dependencies.
The current simple source and symbol-only binder remain available for further
natural source work; they are not accepted build inputs.

## 2026-11-10: complete 27-byte original-register copy

The complete near-Pascal `set_gather_template_to_bullet_template` function
at MAIN `[16F70,16F8B)` now has a **reviewed source-backed ASM owner**,
`main-gather-copy-to-asm`. The original 27-byte code, all 15 instructions,
actual MAP/public and OMF boundaries, empty relocation stream and a compiled
semantic negative are checked in two independent genuine TASM/TLINK rounds.
The negative reduces the real word count 7→6 and fails raw comparison.

The semantic provenance is pinned ReC98 `th04/main/gather.cpp`:
`copy_near_struct_member(gather,offsetof(gather_t,bullet_template),
bullet_template,0,sizeof(BulletTemplate),prepare_si_di)` implements the
original register-level bulk copy. The TH05 actual native 16-bit instructions
independently confirm `PUSH BP; MOV BP,SP`, preserved SI/DI, `MOV CX,7`,
`PUSH DS; POP ES`, `SI=offset bullet_template` at DS577E,
`DI=[BP+4]+24`, `REP MOVSW`, and original near-Pascal `RET 2`.
No foreign DATA object, allocation, helper body, source-owned padding or
machine-code byte template is emitted. The existing 14-byte BulletTemplate,
38-byte gather record and 24-byte member offset remain unchanged.

The maintained semantic ASM source is `copy_to_bullet.asm`, with named size
constants in `copy_to_types.inc` and real source-free external symbols in
`probes/units/gather_copy_symbols.inc`; the existing original physical
binder stays in place. Receipt:
`.analysis/gpt-web-main-gather-copy-asm-a/receipt.json`.
This adds **27 reviewed ASM instruction bytes**. The earlier ordinary
`gather.bullet_template = bullet_template` C++ remains inexact and unaccepted;
it is not retroactively credited as compiler-exact C++.

## 2026-11-13: natural word-copy loop and pointer-walk diagnostics

The ordinary C++ struct assignment remains a 27-byte object but depends on
Borland's unresolved `F_SCOPY@` helper, so it cannot be treated as a native
replacement for the original inline `REP MOVSW`. Several source-only loop
forms were then compiled as bounded one-producer diagnostics:

- An indexed seven-WORD loop emits **50 bytes**. It creates a BP frame and
  recomputes both indexed addresses on every iteration.
- A register SI/DI pointer walk with a WORD trip count emits **44 bytes**.
  It does avoid per-iteration index multiplication, but the loop still uses
  explicit word loads/stores and pointer increments rather than REP MOVSW.
- A `do/while` pointer walk with a register WORD trip count emits **42 bytes**,
  the best of these new natural-C++ shapes. Borland keeps the count in DX and
  emits a decrement/test/branch loop; it still has the BP/SI/DI save/restore
  sequence and is 15 bytes larger than the 27-byte native function.
- Making the trip count an unsigned byte emits **44 bytes**; it adds an AL/DL
  transfer and byte decrement rather than selecting the native CX/REP form.
- An explicit standard `memcpy()` compiles but fails link on unresolved
  `_memcpy`. It does not provide an inline native copy implementation.

These are first-producer shape diagnostics only; no second producer, negative,
acceptance receipt or CODE credit is claimed. The exact 27-byte reviewed ASM
owner remains authoritative. The retained diagnostics are:
`.analysis/gpt-web-gather-copy-word-loop-a-20261113/native-diagnostic.json`,
`.analysis/gpt-web-gather-copy-pointer-walk-b-20261113/native-diagnostic.json`,
`.analysis/gpt-web-gather-copy-register-do-loop-a-20261113/native-diagnostic.json`,
`.analysis/gpt-web-gather-copy-byte-count-a-20261113/native-diagnostic.json`,
and the failed link log under
`.analysis/gpt-web-gather-copy-memcpy-a-20261113/`.

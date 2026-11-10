## 2026-11-10 accepted complete 283-byte original-register ASM owner

**`SWORDS_UPDATE` is now exact** at MAIN `[1EDBA,1EED5)`: one complete
**283-byte** 100-instruction near-Pascal original-language assembly function,
with the original single ordered MZ relocation at relative `+75` (the true
SHARED-frame sound call). This resolves the two original `JL/JGE` near
conditional branches which Turbo C++ repeatedly shortened into local
jump pairs. The native original CPU/branch semantics and source-language
reference are preserved in `_reference/ReC98/th05/main/bullet/swords_add_update.asm`;
its historical original translator/assembler identity is not claimed.

The maintained `swords_update.asm` uses only named real sword structure offsets
and semantic constants from the canonical `patterns.hpp` (26-byte entity,
63 sword slots, fixed pattern indices and signed subpixel hit geometry).
The compiler owns no fake table, game-state DATA, BSS, padding or copied code
array. Its source-free binder imports the true `custom_entities`, stage/shot
state, original player position, near motion and pattern functions and far
sound provider at the real main_01/SHARED/main_03 frames. No instruction
bytes, nearby accepted sword allocator or attack callback bodies are supplied
by that binder.

Two independent TASM32/TLINK positive producers emit **283/283 exact raw
bytes**, the literal original ordered fixup, true MAP symbol boundaries and
complete OMF linked extent; its own meaningful semantic negative increases
the clockwise twirl step 2→3 and is rejected. Receipt:
`.analysis/gpt-web-yumeko-swords-asm-a/receipt.json`; native source review:
`.analysis/gpt-web-yumeko-swords-asm-native-review.json`.

All **283 bytes are classified as reviewed ASM instruction credit**, not C++
codegen credit. The original experimental natural
`src/main/boss/yumeko/swords_update.cpp` remains useful as an inexact
source-language port; its previously attempted 283-byte generated code is
*not* credited. The two accepted 354/428-byte Yumeko sword attack callbacks,
the 121-byte sword allocator and the other original-order accepted callbacks
are unchanged and not replayed, with **no ownership overlap**.

---

# Sword updater candidate

Original MAIN `[1EDBA,1EED5)` is283 bytes, with one far relocation at75 and
no NOPs, tables or padding. The old routing-table distance2504 crossed later
functions and was not a function boundary.

The new C++ covers bullet-clear transition, unsigned twirl countdown and index-dependent rotation,
angle-based sprite restoration, real Motion Point-return consumption, clipping,
player collision, velocity halving and sprite decay. Full canonical Sword26,
template25, custom pool and player types remain unchanged. Returned AX/DX are
read only within their actual Point ABI lifetime, before another foreign call.
No physical arithmetic kernel, target bytes or shortened record is used.

One normal-profile diagnostic emits280 bytes, with its far relocation still75.
The native clip has a two-byte local removal proxy absent from the result;
a second two-byte loop-tail jump is merged, while the player-Y calculation is
one byte longer. Together these explain the three-byte gap. The body remains
unaccepted and outside the live manifest. Diagnostic:
`.analysis/native-producers/main-yumeko-swords-update-a`.

Disabling jump optimization emits 285 and shifts the relocation to 76. Removing
the nested continue or using a decay `else` under that profile still emits 285.
Statement-scoped `-O-` pragmas leave 280 unchanged; a switch emits 286. A scalar
word-pair alias either fails the frontend or emits 320; it is not adopted.
All trials failed, and the ordinary 280-byte source is restored.

Restoring this complete function is also important for the genuine compiler
context of the adjacent354/428-byte attacks; see
[attack recovery](laser_swords.md).

## 2026-11-10 exact-size controller reconstruction experiments

The full original `swords_update` remains a 283-byte near Pascal function,
with original ordered relocation `[75]`. A fresh isolated rebuild of the old
maintained source confirms 280 bytes, while whole-function `-O-` produces 285.
We tested explicit early free-slot control flow, true bounded DX:AX point-return
use, and ordinary source-level clip/collision expressions. The natural
`-O-` branch where the free-slot condition encloses the active body, combined
with the actual pair of register-word player deltas and a nested Y comparison,
now emits **283 complete bytes with the original ordered fixup `[75]`**.
The two specific first-producer diagnostics are
`.analysis/gpt-web-yumeko-reg-dx-mutate-compare-a/` and
`.analysis/gpt-web-yumeko-reg-register-add-then-test-a/`.

**This is not raw-exact and receives no credit.** In the twirl section the
original uses near conditional branches from `+5E` and `+72` directly to the
loop tail, whereas current `-O-` lowering uses shorter local tests plus
additional jumps. The code after the twirl through the final return can be
recovered at the original complete offsets, but no byte-range subset is counted.
Twelve more source-equivalent twirl/continue/goto and local `#pragma -O` variants
emitted 283, 287, 288 or 293 bytes; none was full raw-equal. Private immutable
first producer/variant snapshots reside under `.analysis/gpt-web-yumeko-*`.
The maintained 280-byte natural source, frozen accepted neighbors and original
relocation data are unchanged. Future work should focus on genuine compiler
control-flow lowering or original adjacent TU context, not patching jumps.

## Current 283-byte context source, still not raw-exact

The maintained `swords_update.cpp` now uses the source-equivalent `-O-` scoped
candidate from `.analysis/gpt-web-yumeko-variants/reg-dx-mutate-compare.cpp`.
It consumes the genuine DX:AX return of `PlayfieldMotion::update_seg3()`
immediately and computes both player-relative deltas before the shot overlap
predicate. The complete body emits **283 instruction bytes** and its correct
relative relocation `[75]`, but the original twirl branch graph still differs.
It earns no standalone acceptance.

This precise-length ordinary function is essential real context in the same
compiler object as the 66-byte renderer, 121-byte allocator and later Yumeko
attacks. The follow-on aimed 354 and laser 428 callbacks now compile
raw/ordered-exact; see `laser_swords.md`. Its `-O-` jump profile is reset to
`-O` before later independent pattern definitions, with no code padding,
manual branch bytes or fabricated helper. Earlier 280-byte baseline remains
recoverable from Git history; the noopt natural source is maintained for
continued full-function reconstruction.

## Exact-size context, adjacent attack owners recovered

The natural `-O-` word-result consumer in `swords_update.cpp` now serves as a
**283-byte genuine C++ context prefix** inside `attacks_context.cpp`. It
preserves the real original position of the next seven functions and enables
both previously blocked 354- and 428-byte attack functions to reproduce their
original raw code **and unsorted ordered relocations**. In the compiled combined
cohort the updater still differs at twirl control-flow branches, so it remains
**unaccepted** in its entirety. No subsection earns partial credit. The
positive and negative receipts for the two newly accepted large attacks are
linked in [the attack context review](laser_swords.md); only their affected
standalone accepted neighbors were refreshed.

## Second twirl control-flow pass, 2026-11-10

The correct-length, original-order coherent compiler context remained fixed.
Eight new source-equivalent twirl cases were compiled with the real sword
renderer, allocator and seven later attack functions, without artificial
prefixes. Fall-through without `else`, direct early `continue`, shared loop-tail
gotos and reversed parity dispatch generated full MAIN03 contributions of
2141/2144/2147/2149 versus the original 2139 bytes. None had complete raw
agreement. Actual one-producer and source snapshots are retained under
`.analysis/gpt-web-sword-twirl2-*-a/`. The maintained 283-byte updater, original
relocation stream and the 354/428-byte accepted Boss attacks remain unchanged.
The remaining difference is two twirl branches at updater relative `+5E` and
`+72`, which must naturally target the loop tail rather than local skip/jump
pairs. No partial credit or manual instruction repair is claimed.

## 2026-11-10 native-tail twirl branch variants

Following exact recovery of the adjacent MAINE Staff source, twelve further
source-level twirl variants were compiled in the **real original-order Yumeko
attack translation unit**, not against a fabricated byte prefix. They tested
negative-parity fall-through, genuine empty `if/else`, early `continue`,
conditional loop-tail `goto`, a single `do/while` exit, and mixed semantic
branch/jump forms. The normal complete original updater remains 283 bytes.
The new coherent source lengths were 2139 at baseline, otherwise 2141–2149
bytes rather than the original 2139. None reproduced the native two near
conditional branches from updater-relative `+5E` and `+72` to the loop tail.
The extra local short branches and jumps are still produced by the original
compiler; there is no trustworthy native-authored C++ exactness claim.

All twelve literal trial sources and first-producer MAP/OMF/MZ outputs are
frozen under `.analysis/gpt-web-yumeko-twirl-else-*.cpp` and
`.analysis/gpt-web-yumeko-twirl-else-*-a/`. The canonical updater and both
accepted adjacent 354/428-byte major Boss attack owners were **not modified**;
no acceptance receipt or partial CODE credit was created. The failed direct
loop-tail trials are evidence for further compiler-control-flow recovery, not
permission to insert a missing jump byte into generated output.

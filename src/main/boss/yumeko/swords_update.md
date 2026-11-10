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

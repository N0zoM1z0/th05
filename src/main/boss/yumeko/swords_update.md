# Yumeko `swords_update()` — exact ASM owner and exact C++ alternative

The complete near-Pascal updater occupies MAIN `[1EDBA,1EED5)`, **283 bytes**,
with one ordered relocation at relative `+75`. The accepted
`main-yumeko-swords-update-asm` family is the sole physical owner and sole
credit for these bytes.

The maintained `swords_update.cpp` is now fully natural C++. Two fresh native
Borland/TLINK producers reproduce the complete original-order **2,139-byte**
MAIN03 contribution `[1ED41,1F59C)`, including all **25** original ordered MZ
relocations. They also reproduce the complete 283-byte updater slice and its
relative relocation `[75]`. The compiled twirl-step mutation `2→3` is rejected
with the original relocation order unchanged. This is an exact source-language
alternative, not overlapping C++ CODE ownership.

The updater keeps normal `-O` for the original short twirl branches. Two empty,
false-returning `optimization_barrier()` calls preserve the original separate
clip and collision exits; they emit no instructions. The DX:AX result from
`update_seg3()` is consumed before another call. Twirl, collision mutations,
decay and loop index/pointer advancement remain ordinary C++.

The complete context includes the real sword renderer, allocator, updater and
seven adjacent attack routines in native definition order. The 354-byte aimed
swords and 428-byte laser/swords functions remain separate accepted complete
owners. Their ownership and the updater's 283-byte ASM ownership are unchanged.

Current evidence:

- Natural C++ positives: `.analysis/gpt-web-yumeko-natural-owner-positive-a-20261113/`
  and `...-positive-b-20261113/`.
- Compiled negative: `.analysis/gpt-web-yumeko-natural-owner-negative-twirl-step-20261113/`.
- Verification summary: `.analysis/gpt-web-yumeko-natural-owner-verification-20261113.json`.
- Accepted ASM receipt: `.analysis/gpt-web-yumeko-swords-asm-a/receipt.json`.
- Full-context source and ABI details: [`attacks_context.md`](attacks_context.md).

Earlier branch-shape, loop, register-hint and inline-assembly trials are
superseded by this complete-context result. They are not current blockers or
separate ownership claims.

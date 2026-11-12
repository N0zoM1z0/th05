# MAIN genuine large Boss explosion frame: native 16-bit C global

The original decoded MAIN `[222B4,222B6)` is a complete two-byte
near-C initialized-DATA contribution at DGROUP `209D:18E4`. The
original assembly's `th04/main/boss/explosions_big[data].asm` declares
the C public `_explosion_big_frame dw 0` immediately following the
aligned final near resource filename and before the separate original
Stage Clear score text pointers. The physical address and signed
16-bit width are independently corroborated by the actual native
`boss_explosion_bindings.asm`, not inferred from matching zero bytes.

The already accepted **452-byte two-function Boss explosion source**
reads and increments `explosion_big_frame` after updating each real
big explosion sprite, then uses that same original frame as the one
palette flash/fade clock. On a dead explosion, the actual source resets
it to zero. The 16-bit `int near` value is genuine mutable gameplay
state, not a copied asset, a compiler jump table or a guessed zero
padding block.

`src/main/boss/explosion_frame.c` creates one natural
`int near explosion_big_frame = 0;`, with a native width assertion and
one source-level C public. The binder supplies only the authentic
outside MAIN CODE frames and DATA prefix. Two independent pinned
Borland C/TLINK producers reproduce the exact original two bytes,
OMF/LEDATA/MAP, the original empty ordered MZ fixup stream, and reject
the *compiled* frame-initializer mutation zero→one:
`.analysis/unit-replays/gpt-web-big-boss-explosion-frame-a/receipt.json`.

This interval had previously been **misattributed** to two other C
globals because their different location also contained two zeros.
The earlier score-counters contribution is now correctly accepted at
`[22432,22434)`, the source addresses used in both complete 561/579
byte score functions. That previous owner was moved rather than
retained as an invalid duplicate. See
`src/main/stage/bonus_previous_resources.md`.

This restores the correct physical and source semantic ownership,
without adding fake instructions or doing a whole-program cold replay.
The entire original 452-byte Boss explosion consumer is independently
verified after its separate source ABI is connected.

# Yumeko `swords_update()` — exact C++

The near-Pascal updater occupies MAIN `[1EDBA,1EED5)`, 283 bytes, with one
ordered relocation at +75. It is the C++ public `swords_update()`
inside the original MAIN03 contribution `[1ED41,1F59C)`, between the
accepted C++ `swords_add` and the Yumeko pattern functions. ReC98 still has
this span in its undecompiled `swords_add_update.asm` slice, and the
neighbouring `swords_add` from the same slice is already accepted C++ here.

`swords_update.cpp` is compiled as part of `attacks_context.cpp` with normal
`-O`. It reads the DX:AX `Point` result of `update_seg3()` directly.
Two empty, false-returning `optimization_barrier()` calls keep the original
separate clip and collision exits and emit no instructions. Two producers of
the whole context match the complete function and its relocation, and the
compiled twirl-step 2→3 negative is rejected. Receipt:
`.analysis/unit-replays/claude-yumeko-swords-update-cxx-20261114b/receipt.json`.

This C++ function replaces the earlier reviewed-ASM owner.

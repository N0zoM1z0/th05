# Original one-byte playfield shake redraw clock

Original MAIN DS `209D:0F4A`, decoded byte `[2191A,2191B)`, is the mutable
`playfield_shake_redraw_time` byte. Its zero initializer and immediate
`evendata` after the byte are explicitly in pinned ReC98
`th04/main/playfld[data].asm`. The next byte `[2191B,2191C)` is **not** part
of the declared variable or this accepted owner.

The accepted complete `playfield_shake_update_and_render()` controller
independently writes 2 redraw frames after EGC shifting, decrements the
same original byte during restoration, and resets the shift offsets when
redrawing finishes. Its binary access is at DS `0F4A`; the canonical
`src/main/playfield/shake.hpp` declares this as `char`, not a 16-bit timer.

The maintained C++ initializer `shake_redraw_initial.cpp` compiles to one
complete original `_DATA` LEDATA at this physical address. Both independent
Borland/TLINK producer scopes match the raw byte, native MAP/OMF and empty
loader relocations. A compiled change from zero to one is rejected.
Evidence: `.analysis/unit-replays/gpt-web-main-shake-redraw-clock-20261112-a/receipt.json`.
It adds **one original semantic C++ initialized DATA byte** without
recrediting the existing playfield/EGC code.

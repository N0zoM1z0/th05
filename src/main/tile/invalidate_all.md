# Half-tile dirty-map fills — exact C++

`tiles_invalidate_reset()` at MAIN `[BD24,BD37)`, one alignment NOP at
`BD37`, and `tiles_invalidate_all()` at `[BD38,BD4E)` form one 42-byte
contribution. The accepted `tiles_render()` unit follows at `BD4E`, which
matches ReC98's `th04/main/tile/tile.cpp` order. Each function fills the
1,600-byte `halftiles_dirty` map at DS:4ADA with 400 `REP STOSD` stores of
0 or 0x01010101. It preserves DI and does not clear DF. There are no
relocations.

`invalidate.cpp` follows ReC98's `tiles_invalidate_set_all()`. It is a macro
because TCC rejects inline assembly in inline functions. `_ES = FP_SEG(...)`
produces the original `MOV AX,DS / MOV ES,AX`, `_EAX` the XOR/MOV
immediate, and the build uses the `tcc-s-tasm32` pipeline for the 386
`rep stosd`. The NOP comes from `#pragma codestring "\x90"` and is compared
but not credited. Both producers match all 42 bytes, and the 400→399 DWORD
negative is rejected. Receipt:
`.analysis/unit-replays/claude-tile-invalidate-20261114b/receipt.json`.

A plain `__memset__` call is not exact: it emits 800 `REP STOSW` stores.
These functions replace the earlier reviewed-ASM owners.

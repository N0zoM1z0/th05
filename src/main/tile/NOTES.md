# Tile rendering: notes

Per-routine notes for the assembly sources: `sections.md` (initial fill and
full render), `redraw.md`, `scroll_strip.md`, `invalidate_around.md` and
`bb_mask_family.md`.

## Dirty-map fills (`invalidate.cpp`)

`tiles_invalidate_reset()` and `tiles_invalidate_all()` fill the 1600-byte
`halftiles_dirty` map with 400 `REP STOSD` stores of 0 or 0x01010101; one
alignment NOP separates them, and `tiles_render()` follows in ReC98's
th04/main/tile/tile.cpp order.

- A plain memset compiles to 800 `REP STOSW` stores, so the fill is written
  with pseudo-registers. `_ES = FP_SEG(...)` produces the original
  `MOV AX,DS / MOV ES,AX`.
- The 386 `rep stosd` needs the unit's TASM32 assembly pipeline
  (`tcc-s-tasm32`).

## EGC copy setup (`egc_copy_setup.cpp`)

The original sets the EGC address register with `MOV AX,0`. Writing
`_AX = 0` gives the shorter `XOR AX,AX`, so that one instruction is inline
assembly.

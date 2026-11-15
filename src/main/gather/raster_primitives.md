# Gather raster and GRCG helpers (original assembly)

`raster_primitives.asm` holds three small register-interface functions in
main_03, the same code as ReC98's `th04/hardware/grcg_modecol.asm` and
`th04/main/gather_point_render.asm`:

- `GATHER_GRCG_COLOR_DIRECT` (declared to C++ as
  `grcg_setcolor_direct_seg3_raw()`): takes a 4-bit color in AH and writes
  the four GRCG tile registers (port 7Eh) with interrupts disabled.
  ZUN bloat: main_01 has its own copy (`grcg_setcolor_direct_raw()`).
- `GATHER_GRCG_MODE_RMW`: enables read-modify-write mode (0C0h, port 7Ch).
- `gather_point_render(left, top)`: fastcall with AX = left and DX = top,
  draws one 8-row point from the shifted pellet sprites at DS:0E4A into the
  VRAM plane in ES, writing a byte or a word per row and wrapping at the
  bottom of the 400-line plane. Relies on a clear direction flag.

Two `EVEN` alignment NOPs sit between the functions.

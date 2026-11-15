# Scroll coordinate conversion (`scroll_subpixel_y_to_vram_seg1`)

`coordinates.asm` is the built version (ReC98 th04/main/scroll_y_1.asm). The
function is near Pascal without a BP frame: it reads its single signed word
parameter through `MOV BX,SP` / `SS:[BX+2]`, arithmetic-shifts it right by 4,
adds `scroll_line` if `scroll_active` is set, corrects by 400 lines at most
once in either direction, and returns in AX with `RET 2`.

`coordinates.cpp` is a C++ version that compiles to the same 40 bytes (unit
`main-scroll-coordinate`). It is not counted, since the assembly already
covers the function, so `replay_units.py --plan` lists the unit as `missing`;
that is expected. What it needs:

- The value has to stay in `_AX`. With an ordinary local, Borland moves it to
  DX and back, and three immediate operations get one byte longer each
  (47 bytes). An inline helper function gives 51 bytes.
- `_AX` is unsigned, so the `short` casts are what produce `SAR` instead of
  `SHR` and keep the signed comparisons of the wrap.

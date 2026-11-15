# hud_5_digit_put() and hud_points_put() (numbers.asm)

Two far Pascal entry points in `main_03` that share one decimal rendering tail
and the final `RETF 8`:

- `hud_5_digit_put(left, y, value, attribute)` writes a five-digit unsigned
  word into the last five cells of the shared glyph row.
- `hud_points_put(left, y, points)` writes seven digits of an unsigned long in
  white, followed by a fixed 0 in the continues-used cell.

Both divide by the powers of ten in `decimal_tables.cpp`. Leading zeroes become
empty glyphs (02h); the units digit is always shown. The glyph row is
`hud_gaiji_row` (`decimal_scratch.c`).

- ZUN quirk: numbers with more than seven digits are not clipped. The highest
  digit overflows into the glyphs after 9, i.e. the A-Z range.
- ZUN landmine: relies on a clear direction flag.
- The second entry point jumps into the middle of the first function's code,
  with the digit state packed into EDX, BX, AX and CH:CL. That, and the two LEA
  instructions kept by `nosmart`, mark it as hand-written ASM. There is one
  `even` alignment NOP between the two entry points.

ReC98's `th05/main/hud/number_p.asm` documents the same code.

# hud_bar_put() (bar.asm)

Draws an eight-cell bar (boss HP, dream, power) at column 56 of the given row.
It is near Pascal with three word parameters: row, value and attribute. The
value is declared `int`, but only its low byte is read.

Each cell stands for 16 units. A value of 128 or more draws the eight distinct
"full bar" glyphs 30h-37h. Smaller values draw full cells (2Fh), one partial
cell (20h-2Fh) and empty glyphs (02h) for the rest. The glyphs go into the
shared row at `hud_gaiji_row` (`decimal_scratch.c`) and are drawn with
`gaiji_putsa()`.

- ZUN bug: a value of 0 draws one full cell, because the partial-cell index
  wraps around. `hud_hp_put()` avoids this by not calling the bar for 0.
- ZUN landmine: the routine relies on the direction flag being clear.
- The routine reads its arguments through BX = SP, before pushing DI, and
  pushes the `gaiji_putsa()` arguments before computing the glyphs. This
  stack and register usage is why it is treated as hand-written ASM.

ReC98's `th05/hud_bar.asm` documents the same routine.

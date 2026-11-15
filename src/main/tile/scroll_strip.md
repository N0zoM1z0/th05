# Scrolling tile strip copy

`copy_scroll_strip.asm` (descriptive name `tiles_copy_scroll_strip`; sub_BC6A
in ReC98 th05_main.asm) copies the 24 tile columns of the strip that scrolling
just exposed, to VRAM offset `scroll_line * 80 + 4`. The first fragment starts
`scroll_line % 16` lines into a tile; if the strip crosses a tile row, a second
fragment comes from the next ring row. Crossing the bottom of the 400-line VRAM
also wraps the ring index by its full 1600-byte size. Three scratch words keep
the first fragment's source skip, destination and height.

It is kept as assembly: BP carries the EGC transfer word (no stack frame), AX
holds the ring cursor, DH/DL hold the second fragment's height and the column
count, BL tracks the pending fragment and CX counts lines. The caller must
have enabled the EGC; zero or excessive heights are not checked.

# Point popup rendering (`put.asm`, `render.asm`)

Kept as assembly because both use a private register interface (ReC98
th05/main/pointnum/render.asm, th04/main/pointnum/num_put.asm).

`pointnum_put` draws one 8x8 digit glyph. Input: AX = top, DX = left,
CX = glyph, ES = VRAM. It picks the glyph row for the horizontal shift from the
mask bank (12 glyphs x 8 shifts x 8 rows x 2 bytes = 1536 bytes), skips zero
mask words, writes a single byte when the right byte of the mask is zero, and
wraps from the bottom of VRAM to row 0 without resetting the source. It
returns DX advanced by 8 pixels, restores AX/SI/DI, and clobbers BX/CX. Its row
loop is aligned with `EVEN`. Requires a clear direction flag for `LODSW`.

`pointnums_render` returns immediately for an empty alive list. Otherwise it
sets ES = A800h and, with interrupts disabled, writes four white tile bytes to
the GRCG (port 7Eh), then re-enables interrupts; at
`pointnum_first_yellow_alive` it switches to yellow (FF/FF/00/FF). The caller
must have enabled the GRCG. Each popup is centered on its position: left =
X + 32 - width / 2, and top is Y + 12 pixels (playfield top 16 minus half the
glyph height) converted through `scroll_subpixel_y_to_vram_seg1()`. It draws
the stored digits from the highest visible one down, then the trailing 0.

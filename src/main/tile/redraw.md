# Dirty half-tile redraw

`redraw.asm` (`tiles_redraw_invalidated`, ReC98 th04/main/tile/redraw.asm)
scans the 50x32 half-tile dirty map from bottom to top, testing the 24 visible
columns of each row. For each set flag it clears the flag and copies the
corresponding 16x8 half of the tile from the tile ring through the EGC latch.
The parity of DH selects the top or bottom half, and the ring cursor moves to
the next row only after both halves. Ring entries are VRAM offsets of tile
images, not pixel data.

It is kept as assembly because of its register protocol: CX counts scanlines,
DH is the half-row and DL the column, ES stays at A800h, and the word copies
do not depend on the direction flag. SI/DI/BP/DS are preserved. It calls
`egc_start_copy_noframe()` and master.lib's `egc_off()`.

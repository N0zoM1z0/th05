# Tile invalidation around a hitbox

`invalidate_around.asm` (`tiles_invalidate_around`, ReC98
th04/main/tile/inv.asm) marks the half-tiles covered by `tile_invalidate_box`
centered on a subpixel point as dirty. It is near Pascal, takes the point as
two stack words (read through BX, no BP frame) and returns with `RET 4`.

It clips the box to the 384x368 playfield, converts to 16-pixel columns and
8-line half-tile rows, adds the scroll origin of the back page, and handles
the 400-line wrap with two row-fill loops using ES:DI, AH/CL for the column
count, and `REP STOSB` into the 1600-byte dirty map. Geometry constants are in
`invalidate_around_types.inc`.

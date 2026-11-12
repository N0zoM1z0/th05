# Main shot-laser eight-pixel coverage-cel sequence

The original MAIN decoded interval `[21E66,21E6B)` is one complete
**five-byte** initialized C data contribution: the five horizontal
raster coverage states for the fired player laser. The original
`_reference/ReC98/th04/main/player/shot_laser[data].asm` defines the
five-byte `_SHOT_LASER_DOTS` public in this exact order; the independently
reviewed real raster painter `src/main/player/shot_laser_put.asm` reads
`SHOT_LASER_DOTS[bx]` into AL, rotates that occupancy pattern by the
actual pixel-alignment shift and writes one or two bytes per scanline
into the PC-98 VRAM plane. The source is therefore a **laser width/
occupancy control table**, not a sprite bitmap, CDG pixel image,
level art resource, or compiler dispatch table.

The native C initializer generates its values from source-level bit
geometry: centered 2-, 4- and 6-pixel strips, a fourth cel with the
two missing inner edge bits (6 and 1), and full eight-pixel coverage.
This intentionally preserves the fourth cel's non-monotone `0xBD`
occupancy; replacing it with a generic seven-pixel strip would *change*
the original game. All widths and bit locations are ordinary visible
C constants and bit operations rather than an opaque target-byte blob.
It exports one mutable `unsigned char near SHOT_LASER_DOTS[5]` object,
consistent with the original near-data pointer arithmetic.

The original DATA begins at true DGROUP `209D:1496`. The source-free
binder holds only the authentic MAIN code-group frames and the outside
DATA prefix; it supplies no raster masks, source instructions,
relocations or fake fill. The next separately accepted `LS00.BB`
resource filename starts at `[21E6B,21E73)`, and the preceding source
state remains unknown outside this 5-byte contribution.

The focused native proof
`.analysis/unit-replays/gpt-web-shot-laser-mask-a/receipt.json`
contains two genuine Borland C producers, complete 5-byte raw equality,
original OMF initialized-DATA and MAP extents, empty ordered MZ
fixups and a rejected *compiled* mutation of the third cel's centered
width from six to four. No other unit or full MAIN cold replay was run.

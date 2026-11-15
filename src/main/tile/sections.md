# MAP section offsets, initial tile fill and full tile render

`section_offsets.c` builds the 32-entry table of byte offsets into the loaded
MAP data: section N starts at N * 320 bytes (5 rows of 32 tile words). The
loaded MAP segment starts directly with section data, since `map_load` reads
the 8-byte file header separately. TH05 STD files store section IDs already
multiplied by 2, so they index this WORD table as byte offsets.

Two hand-written assembly routines use the table and the 25x32-word tile ring:

- `fill_initial.asm` (`tiles_fill_initial`, ReC98 th04/main/tile/fill_ini.asm)
  fills the ring from the first five sections, bottom to top. It keeps the
  STD segment in FS, the MAP segment in DS and the game's DS in ES, packs the
  section and row counters into AL/AH, and copies the 24 visible words of each
  32-word row with REP MOVSD. The 8 hidden columns of each ring row are left
  untouched. Requires a clear direction flag.
- `render_all.asm` (`tiles_render_all()`, ReC98 th04/main/tile/render_a.asm)
  copies all 24x25 tiles from the ring into the playfield through the EGC
  latch, 16 lines per tile. Its row loop is aligned with `EVEN`. It calls
  `egc_start_copy_noframe()` and master.lib's `egc_off()`.

TLINK prints the public `@TILES_RENDER_ALL$QV` as `tiles_render_all()` in the
MAP file; the unit manifest has to use that spelling.

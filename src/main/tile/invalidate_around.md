# Complete scroll-wrapped tile collision invalidation

MAIN `TILES_INVALIDATE_AROUND` is the complete `[BAD2,BB9E)` near-Pascal
function: **204 original instruction bytes**, 82 instructions, no table,
padding or relocations. Its two stack words are the original Point coordinates,
and it returns with `RET 4`. It marks the actual uninitialized 50×32 dirty
flag bank from a caller-provided hitbox, without clipping away the original
unchecked state behavior.

The algorithm clips horizontal and vertical coverage to the 384×368 game
field, converts subpixels to 16-pixel tiles, accounts for the 400-line PC-98
scroll origin on the active back page, and applies an 8-line dirty grid. It
handles the modulo-400 wrap with the original two row-fill loops, using ES:DI,
AH/CL to retain the horizontal count, and `REP STOSB` over the actual 1600-byte
bank. Source types and symbolic geometry are in `invalidate_around_types.inc`;
the real page/scroll/hitbox/buffer globals live in the foreign DGROUP. No map,
tile, image, or bitmap data is compiled into this function.

The reference ReC98 `th04/main/tile/inv.asm`, native register/segment protocol,
stack-argument access through BX, and the split-wrap string loops support
reviewed original assembly reconstruction, not C++ attribution. Historical
source identity remains unproved. The maintained ASM uses semantic expressions,
not target-derived instruction bytes or artificial branch filler. The
independent symbol-only binder anchors original CS `AE1`, DS `209D`, original
buffer `209D:4ADA..511A`, and every external cursor and scrolling label.

The strict focused replay passes with two independent TASM32/TLINK builds,
complete native raw **204/204**, original empty ordered relocation list,
verified CRC-valid OMF/LEDATA, CODESEG/map start/end and true foreign frames.
Its own compiled semantic negative changes the dirty-row offset mask from
`(8-1)` to `(8-2)` and is rejected with the same full instruction extent.

- Accepted receipt: `.analysis/gpt-web-main-tile-invalidate-around-b/receipt.json`
- Full original native review: `.analysis/gpt-web-main-tile-invalidate-around-native-review.json`
- Source: `src/main/tile/invalidate_around.asm`

The 204 bytes receive **reviewed ASM instruction credit only**. Neighboring
accepted tile fill, draw, redrawing, reset and set-all implementations and
all genuine C++ callers retain their existing accepted producer provenance.
No unchanged owner is recompiled for this independently bound function.

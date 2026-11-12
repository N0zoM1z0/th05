# MAINE masked-PI quarter-image coverage phases

The decoded original `[107EE,1080E)` holds the complete 32-byte
`PI_MASKS[4][4]` planar coverage bank. The maintained C source defines
four native-word mask stages, each a four-row 16-pixel repeating coverage
pattern. The first masks are sparse; the next interleave the bit planes
and the last fills three or four staggered quarter-pixel columns. The
original semantic patterns are cross-checked against
`_reference/ReC98/th03/formats/pi_put_masked[data].asm`.

These are source-level arithmetic patterns, not a copied PI image, bitmap
asset or encoded target byte table. Each nibble is repeated by a normal
constant-folded 16-bit word expression, and the compiler enforces all
4×4×2 bytes. The actual cutscene `script_op()` picture-transition path
calls `pic_put_both_masked()`, which invokes the foreign masked-PI drawing
service that indexes `PI_MASKS`; no additional drawing CODE or assets are
claimed by this DATA source.

The source-only native binder preserves MAINE group_01, SHARED and DGROUP
at `A540`, `E800` and `10110` and the real DATA prefix DS:06DE. Two
independent Borland C compiles reproduce all 32 bytes, complete compiler
DATA scope, exact MAP placement and empty original ordered MZ fixups. A
compiled mutation of the final-stage third-row coverage is rejected.
Receipt: `.analysis/unit-replays/gpt-web-maine-pi-mask-patterns-a/receipt.json`.
The preceding foreign PI staging bytes and following tables are not
accepted by this unit; no whole-program replay was requested.

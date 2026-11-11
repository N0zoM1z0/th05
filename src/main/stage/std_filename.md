# MAIN `ST00.STD` initialized stage resource name (9 bytes)

The original MAIN DATA `[21924,2192D)` contains the complete nine-byte
`ST00.STD\0` filename used by the TH05 standard-stage event loader. The
actual retained source `th04/formats/std[data].asm` independently names this
literal under the standard-stage filename label. It is a game resource
*filename*, not the resource payload or an artificial initialized pointer.

`std_filename.c` represents this original semantic state as one natural
nine-byte C char array in a genuine near object. Its compile-time `sizeof`
and `offsetof` checks preserve the original layout. The symbol-only binder
positions the complete C DATA at DGROUP:0F54 without copying any foreign CODE
or initialized data. The *following zero byte* at original `2192D` remains
unknown and is never credited as a declared array element or padding.

The original full nine bytes and empty ordered MZ relocation list matched two
independent native Borland/TLINK producers. Changing `ST00.STD` to `ST01.STD`
in the actual compiler input was compiled and rejected. Focused receipt:
`.analysis/unit-replays/gpt-web-main-std-filename-20261111/receipt.json`.
The maintained grouping is source semantics, not a claim about the exact
historical C struct declaration.

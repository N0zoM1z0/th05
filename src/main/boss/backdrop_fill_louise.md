# Louise stage-two backdrop callback

MAIN `[14AAA,14AB8)` contains a complete 14-byte near original-register
`louise_backdrop_colorfill()` callback. The full stage-two initialization at
`14699` installs its near address `9C9A`, relative to MAIN `main_01` base
`AE10`; this resolves the previously unnamed final function after
`stagex_setup`. The preceding `14AA9` alignment byte is not part of it.

The callback preserves DI, selects PC-98 window `AC10`, initializes ES:DI to
`AC10:36B4`, and calls the already accepted near `grcg_fill_playfield_rows`
at MAIN `10600`, preserving the original GRCG color state. The semantic
register recipe appears in pinned ReC98 `th05_main.asm` as Louise's
`GRCG_FILL_PLAYFIELD_ROWS 192,176`. The Yumeko callback uses the same
window geometry elsewhere but remains a *separate* near function and source
owner. The self-contained TASM source owns no row-painter implementation,
initialized DATA, MZ relocation site, or padding byte.

The focused receipt
`.analysis/asm-replays/gpt-web-main-louise-backdrop-a/receipt.json`
records two independent TASM32/TLINK builds, all 14 original bytes,
the empty ordered relocation stream, original `main_01` entry and complete
MAP/OMF CODE scope. A source mutation changing the final row by one byte is
assembled and rejected. The caller and source-origin evidence is in
`.analysis/gpt-web-main-louise-backdrop-native-review.json`. All 14 bytes
are credited to reviewed register-level ASM.

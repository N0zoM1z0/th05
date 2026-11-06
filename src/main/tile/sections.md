# MAP section offsets and visible tile cache

The table is the complete 64-byte initialized contribution at MAIN
218DA..2191A, DS0F0A..0F4A: 32 WORD offsets. Each is section_id times the
320-byte MAP section size, derived from five rows of 32 WORDs. The loaded MAP
segment begins with section data; map_load consumes the separate eight-byte
file header before allocating and reading the section payload. The table
therefore starts at offset 0. It contains geometry, not tile-image pixels.

`section_offsets.c` generates all entries from the format's row/column/word
sizes. It owns no CODE, BSS or padding. The complete existing C++
map_section_tiles_t also asserts 320 bytes. ReC98 b6ba5b0a
th04/main/tile/section[data].asm corroborates the 32-entry source model; its
acceptance and source language do not transfer. The current maintained
initializer is C, and the claim is initialized semantic DATA only.

Two complete handwritten-kernel candidates consume that table or its cache:

| Procedure | Complete MAIN scope | Compared | Instructions | Checked alignment |
| --- | --- | ---: | ---: | --- |
| `TILES_FILL_INITIAL` | BB9E..BBEC | 78 | 78 | None |
| `@TILES_RENDER_ALL$QV` | BBEC..BC2E | 66 | 65 | Relative 23 |

The initializer keeps the STD selector in FS, MAP selector in DS and incoming
game DS in ES. AL/AH pack section/row counters; REP MOVSD copies 24 visible
WORDs from each 32-WORD source row, stepping both row cursors backward. Five
sections of five rows fill the visible columns of the complete 25x32-WORD
tile ring at DS511A..575A. TH05 STD IDs already contain the WORD table's byte
offset; no extra doubling or validation is added. The STD cursor at DS575A,
STD selector at 0F52 and MAP selector at 4AD8 remain foreign.

The initializer preserves DS/SI/DI/BP and leaves ES at entry DS, FS at the STD
selector. AX/BX/CX/DX and arithmetic flags are scratch. IF/DF are unchanged;
the string copy requires clear DF. The unfilled eight columns in each cache
row remain untouched. No cache, map, script, segment handle or pixel values
are supplied by the binder or counted as owned DATA/BSS.

The renderer traverses the cache from bottom to top, copying 24 tiles per row
and 16 scanlines per tile. Its manual ES:A800 reads and writes use the EGC
latch to transfer the tile's planes into the playfield at x32 over 400 lines.
It preserves SI/DI/BP/DS and leaves ES=A800. AX/BX/CX/DX and flags are scratch;
IF/DF are unchanged and the manual word-copy loop is independent of DF.
Native near-Pascal no-argument callers retain their real interfaces.

The FS/DS/ES cache-fill protocol, packed counters and specialized REP loop,
and the renderer's nested EGC latch loop with CX/DL counters support separate
original-handwritten-ASM inference. This does not rely on a failed C++ trial.
Candidate algorithms are ReC98 th04/main/tile/fill_ini.asm and render_a.asm.
The nearby EGC setting helper BC2E..BC6E is explicitly excluded: its ordinary
hardware API does not inherit either kernel's source-language decision.
The renderer calls that actual near provider and the known Master far EGC_OFF
at 0000:085E. The primary Master 0.23 EGC.ASM confirms the latter's mode shutdown;
neither provider body receives new ownership or credit. Historical source,
assembler identity and exhaustive vendor ancestry remain unproved.

The renderer's row-loop NOP compares normally, with zero credit; EVEN expresses
the loop alignment. No instruction byte, asset payload, artificial stack,
inside-function gap or defensive behavior is introduced. Ordered MZ fixups
are empty for fill and `[61]` for render.

## Complete focused acceptance

The C table passes two deterministic builds, valid OMF and complete DATA
LEDATA/MAP ownership, all 64 raw bytes and the empty original fixup stream.
Its DATA-specific mutation shifts every section index by one and is rejected.
The following eight bytes are not a continuation of the section-offset formula
and stay outside the complete table object and generated contribution.

Both ASM kernels pass two independently built source objects, complete
CODE/LEDATA, native frames/publics, raw bytes and original ordered fixups.
Each normal negative omits visible columns and is rejected with unchanged
extent and fixup order. Normalized OMF, MAP and whole MZ outputs are deterministic.
Only dependency metadata is normalized; instruction bytes and relocations are
never changed. DATA/BSS contributions from these kernels are empty.

The renderer's first assembly/link produced the correct 66 bytes, but its
manifest locator incorrectly used the raw `@TILES_RENDER_ALL$QV` spelling.
TLINK displays that real public as `tiles_render_all()`. Correcting only this
MAP lookup allowed the identical saved first producer to be revalidated after
all source/verifier/tool identities were checked. The continuation builds only
the independent second producer and negative, then passes the unchanged saved
receipt validator. No symbol, generated artifact, ABI or source was changed.
The original stopped packet and file hashes remain in the receipt's lineage.

| Unit | Receipt under `.analysis/` | Receipt SHA-256 |
| --- | --- | --- |
| C table | `unit-replays/main-tile-section-offsets-exact/receipt.json` | `d9d494eafb17b98988093c67cba2ca867edbaa091aeeab0c21f02c9b1c7210e6` |
| ASM fill | `asm-replays/main-tile-fill-a/receipt.json` | `1feb64ed688b3f8d491579255a0f9984a3be19652e37fb90b2158d21fbfcd6b6` |
| ASM render | `asm-replays/main-tile-render-b/receipt.json` | `ea08b179162a1b946258a63b301b9b25a4221bb3ce5408d4c7b59346c4685740` |

Complete private native/source proofs are `tile-section-offsets-native-review.json`
(`994360ac6ced5c0bb4982c2aae0a488090bdf58d2d1031558aa95fcb0fa22e49`),
`tile-fill-native-review.json`
(`3a30c1761b16413a8898ca477c4406be83f083dab1c84a5136f56a3d42aee90d`)
and `tile-render-native-review.json`
(`fb6d57fea37fda8607645d70f5be9264719fcc7e906ff9e4c8b438a609e194ee`),
all under `.analysis/`.

Explicit adoption credits 64 initialized C semantic DATA bytes and, separately,
143 reviewed ASM instruction bytes. One alignment byte is compared with zero
credit. No C/C++ function, raster, foreign provider, complete executable or global
percentage is newly accepted. Unchanged accepted units and installed execution
proofs were reused after identity checks; no full replay, CPU model or extra
per-function tests were run.

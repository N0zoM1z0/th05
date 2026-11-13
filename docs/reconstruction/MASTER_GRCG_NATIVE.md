# Original Master graphics and display in TH05 MAIN

**Twenty-four complete Master 0.23 graphics and display procedures now reproduce 3,988
previously unknown MAIN CODE bytes** from the original assembly source,
the actual TASM OMF and the authentic C0L linker layout. The large
polygon clipping and line-drawing functions are included in full.
The second source pass adds 1,378 bytes of palette, text, font and other
display code to the initial 2,604-byte GRCG proof.

The original GRCG primitive family:

| Complete function | Original MAIN extent | CODE bytes | OMF FIXUPP |
| --- | --- | ---: | ---: |
| `GRCG_BOXFILL_RETURN` | `0EA0..0EA6` | 6 | 0 |
| `GRCG_BOXFILL` | `0EA6..0F76` | 208 | 7 |
| `GRCG_BYTEBOXFILL_X` | `0F76..100E` | 152 | 3 |
| `GRCG_CIRCLE` | `10AE..1146` | 152 | 13 |
| `GRC_SETCLIP` | `130C..139E` | 146 | 12 |
| `GRC_CLIP_POLYGON_N` | `139E..1690` | 754 | 24 |
| `GRCG_HLINE` | `1690..1716` | 134 | 7 |
| `GRCG_LINE` | `1716..18B4` | 414 | 8 |
| `GRCG_POLYGON_CX` | `18B4..1A44` | 400 | 7 |
| `GRCG_PSET` | `1A44..1A88` | 68 | 5 |
| `GRCG_SETCOLOR` | `1A88..1AB2` | 42 | 0 |
| `GRCG_VLINE` | `1AB8..1B3E` | 134 | 5 |

Additional complete graphics, font, palette, text and math procedures:

| Complete function | Original MAIN extent | CODE bytes | OMF FIXUPP |
| --- | --- | ---: | ---: |
| `BFNT_EXTEND_HEADER_ANALYSIS` | `03F0..0450` | 96 | 0 |
| `cutline` | `0778..07EC` | 116 | 6 |
| `GAIJI_PUTSA` | `1DBE..1E14` | 86 | 1 |
| `GRAPH_400LINE` | `1E14..1E62` | 78 | 12 |
| `GRAPH_EXTMODE` | `1E86..1EDC` | 86 | 1 |
| `GRAPH_SCROLLUP` | `1EE2..1F3A` | 88 | 2 |
| `IATAN2` | `1F3A..1FA6` | 108 | 2 |
| `draw_trapezoidx` | `1FAC..2038` | 140 | 17 |
| `SUPER_LARGE_PUT` | `2048..20DC` | 148 | 6 |
| `PALETTE_SHOW` | `2158..2262` | 266 | 4 |
| `TEXT_BOXFILLA` | `24A8..24F6` | 78 | 1 |
| `TEXT_PUTCA` | `2540..2598` | 88 | 1 |

The six-byte `GRCG_BOXFILL_RETURN` is the original return-only procedure
immediately before the public `GRCG_BOXFILL` entry. Its original archive block
is named `RETURN` in `GC_BOXFI.ASM`; the maintained source gives the label a
context-specific name. The actual source-built TASM OMF and original MAIN bytes
both contain `5F 5E 5D CA 08 00` (`pop DI`, `pop SI`, `pop BP`, `retf 8`). This
sequence also occurs at other legitimate return sites, so its physical extent
is anchored by the original TASM procedure listing and source/OMF context, not
by an invalid uniqueness assumption. It is a separate six-byte owner, not an
extension or duplicate credit for the 208-byte `GRCG_BOXFILL` body.

The [native verifier](../../scripts/review_master_grcg.py) reads the
pinned original Master author archive, complete active procedure
boundaries from the TASM listing, and the exact source-built OMF object.
The original and maintained instruction bodies compare without operand
rewriting. The allowed spelling differences are comments/spacing, `@@`
local-label scopes, the renamed `GRCG_BOXFILL_RETURN` exit, and
`GC_CIRCL_`, `PALSHOW_`, `LARGEPUT_`, and `KOIZOIDX_`-scoped local
labels or struct member aliases. Opcodes and real register operands
are not normalized.

Each complete CODE segment extent is reconstructed from genuine source
LEDATA and original ordered FIXUPP records. The calibrated and original
MAIN executables are checked independently; the native C0L startup
anchors the 18-byte original DATA/BSS offset difference. All 23
functions have empty original ordered MZ relocation lists, also checked
against the OMF-derived lists. `GRCG_SETCOLOR` and `BFNT_EXTEND_HEADER_ANALYSIS` correctly
have zero OMF fixups; zero is not evidence of an incomplete function.

The [proof](../../config/master_grcg_ownership.json) and
[explicit adoption](../../config/reviewed_master_grcg.json) select only
these complete, previously unknown CODE extents. The already reviewed
`GRCG_CIRCLEFILL` and `GRCG_CIRCLE_X` are **not double-counted**.
Remaining neighboring Master functions and the gaps between procedures
retain their original ownership classifications.

```sh
python3 scripts/review_master_grcg.py --check
python3 scripts/review_master_grcg.py --structural-check
python3 scripts/ownership.py --check
```

All 3,988 bytes are source-backed third-party Master CODE. They
contribute zero game-authored C++ credit, and no whole-game replay,
source-byte copy or inferred global denominator is involved.

# Original Master GRCG and polygon geometry in TH05 MAIN

**Eleven complete Master 0.23 graphics procedures now reproduce 2,604
previously unknown MAIN CODE bytes** from the original assembly source,
the actual TASM OMF and the authentic C0L linker layout. The large
polygon clipping and line-drawing functions are included in full.

| Complete function | Original MAIN extent | CODE bytes | OMF FIXUPP |
| --- | --- | ---: | ---: |
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

The [native verifier](../../scripts/review_master_grcg.py) reads the
pinned original Master author archive, complete active procedure
boundaries from the TASM listing, and the exact source-built OMF object.
The original and maintained instruction bodies compare without operand
rewriting. The allowed spelling differences are only comments/spacing,
`@@` local-label scopes, the renamed `GRCG_BOXFILL_RETURN` exit,
and `GC_CIRCL_`-scoped scratch/dispatch labels in the circle routine.

Each complete CODE segment extent is reconstructed from genuine source
LEDATA and original ordered FIXUPP records. The calibrated and original
MAIN executables are checked independently; the native C0L startup
anchors the 18-byte original DATA/BSS offset difference. All eleven
functions have empty original ordered MZ relocation lists, also checked
against the OMF-derived lists. `GRCG_SETCOLOR` correctly has zero OMF
fixups; zero is not evidence of an incomplete function.

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

All 2,604 bytes are source-backed third-party Master CODE. They
contribute zero game-authored C++ credit, and no whole-game replay,
source-byte copy or inferred global denominator is involved.

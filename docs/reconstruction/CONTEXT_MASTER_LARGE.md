# Native Master 0.23 functions in OP and MAINE

Sixty-five complete functions from the original Master 0.23 assembler source
now reconstruct **9,934 previously unknown CODE bytes** in OP/MAINE.
The largest are OP's **536-byte GRCG_POLYGON_C** and the two **420-byte
BGM_INIT** routines; both targets also gain full 320-byte BGM_READ_SDATA
and 240-byte SUPER_PUT and HMEM_ALLOC functions. The extended proof
adds 43 complete OP/MAINE functions (5,836 bytes), notably both
302-byte BGM_PLAY routines, two 298-byte BGM_MGET routines, exact
file-reading/writing, drawing and SUPER-entry source procedures.

| Complete function | OP | MAINE | Source |
| --- | ---: | ---: | --- |
| SUPER_PUT | 240 B | 240 B | SUPERPUT.ASM |
| SUPERPUT_DISP1–DISP4 and DISP | 191 B | 191 B | SUPERPUT.ASM |
| BGM_INIT | 420 B | 420 B | B_INIFIN.ASM |
| PALETTE_SHOW | 266 B | 266 B | PALSHOW.ASM |
| HMEM_ALLOC | 240 B | 240 B | MEMHEAP.ASM |
| BGM_READ_SDATA | 320 B | 320 B | B_R_SDAT.ASM |
| GRCG_POLYGON_C | 536 B | — | GC_POLGC.ASM |
| GRCG_BOXFILL | — | 208 B | GRCG original Master source |
| FILE_FLUSH, FILE_READ, FILE_WRITE | 454 B | 454 B | FILCLOSE, FILREAD, FILWRITE |
| GRCG_BYTEBOXFILL_X, GRCG_HLINE, GRCG_VLINE | 420 B | 420 B | Original Master graphics |
| GRC_SETCLIP, GRCG_PSET | — | 214 B | Original Master clipping/pixel |
| GRAPH_400LINE, GRAPH_EXTMODE | 164 B | 164 B | Original Master display |
| SUPER_ENTRY_PAT, SUPER_ENTRY_AT, SUPER_CANCEL_PAT, SUPER_FREE | 436 B | 436 B | Original Master SUPER |
| SUPER_CONVERT_TINY, SUPER_PUT_TINY_SMALL | — | 300 B | Original Master tiny sprites |
| HMEM_FREE | 168 B | 168 B | MEMHEAP.ASM |
| _BGM_MGET, _BGM_PLAY, BGM_FINISH, _BGM_EFFECT_SOUND, BGM_SOUND | 888 B | 888 B | Original Master BGM |
| GAIJI_PUTSA, GAIJI_PUTCA, IATAN2 | — | 262 B | Original Master text/math |
| **Totals** | **4,743 B** | **5,191 B** | |

All sixty-five complete function bodies match their independent original
author-archive assembler procedures (including local-label aliases) and
the actual retained TASM translation unit. The
[scoped original OMF verifier](../../scripts/review_context_master_large.py)
reconstructs raw CODE from gapless `_TEXT` LEDATA and every original CODE
FIXUPP via each real MAP's `_TEXT`, `_DATA`, `_BSS` and DGROUP layout.
The complete original and calibrated machine-code scopes agree, with the
**actual ordered MZ fixups** preserved. BGM_READ_SDATA has one original
segment relocation at function-relative **+197** in each target.

MAINE's original DGROUP begins one paragraph later than the calibration;
OP's paragraph is identical. The source-linked reconstruction reads the
original CRT group value, rather than normalizing differing segment words.
The [source proof](../../config/context_master_large.json) and
[explicit decision](../../config/reviewed_context_master_large.json)
adopt only these sixty-five original complete function/PROC extents.

**Boundary caveat:** SUPER_PUT is exactly **240 bytes**, not the
434 bytes through the next symbol in the public MAP: later standalone SUPERPUT dispatcher PROC bodies occupy the intervening bytes.
Their **191 genuine source-written bytes per executable** are now adopted
as five separate complete functions. The three intervening EVEN bytes are
not credited. A separate private source review
of some overlapping functions was reconciled before adoption; its unique
MAINE GRCG_BOXFILL was incorporated and duplicate claims discarded.

No new claim is made for source-inexact or ambiguous candidates such as
ISQRT, several source-modified machine/graph functions, or the duplicate
palette-source variants. For each included procedure, original author
assembler source, the exact TASM output, all linked bytes, native MAP
entry, and the *original unsorted* relocation list are compared in the
affected scope; no full cold replay is required.

```sh
python3 scripts/review_context_master_large.py --check
python3 scripts/review_context_master_large.py --structural-check
python3 scripts/ownership.py --check
```

These are third-party original Master ASM contributions and add **zero
game-authored C++ credit**. Other CODE, helpers, DATA and BSS remain
unchanged until independently recovered.

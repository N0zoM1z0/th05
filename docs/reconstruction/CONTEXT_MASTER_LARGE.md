# Native Master 0.23 functions in OP and MAINE

Twenty-two complete functions from the original Master 0.23 assembler source
now reconstruct **4,098 previously unknown CODE bytes** in OP/MAINE.
The largest are OP's **536-byte GRCG_POLYGON_C** and the two **420-byte
BGM_INIT** routines; both targets also gain full 320-byte BGM_READ_SDATA
and 240-byte SUPER_PUT and HMEM_ALLOC functions.

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
| **Totals** | **2,213 B** | **1,885 B** | |

All twenty-two entire function bodies match their independent original
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
adopt only these twenty-two original complete function/PROC extents.

**Boundary caveat:** SUPER_PUT is exactly **240 bytes**, not the
434 bytes through the next symbol in the public MAP: later standalone SUPERPUT dispatcher PROC bodies occupy the intervening bytes.
Their **191 genuine source-written bytes per executable** are now adopted
as five separate complete functions. The three intervening EVEN bytes are
not credited. A separate private source review
of some overlapping functions was reconciled before adoption; its unique
MAINE GRCG_BOXFILL was incorporated and duplicate claims discarded.

```sh
python3 scripts/review_context_master_large.py --check
python3 scripts/review_context_master_large.py --structural-check
python3 scripts/ownership.py --check
```

These are third-party original Master ASM contributions and add **zero
game-authored C++ credit**. Other CODE, helpers, DATA and BSS remain
unchanged until independently recovered.

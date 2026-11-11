# Four original Master literal initialized-DATA tables in MAIN

This source-linked review resolves **224 formerly unknown DATA bytes**, all
third-party Master 0.23 original assembler initializers, not game-authored
C/C++ or instruction bytes. Each table has an exact original author source,
an independently retained native TASM initializer, full ordinary DATA LEDATA,
real MAP public, unique original target occurrence, and matching original /
calibration bytes with an empty ordered MZ relocation list.

| Source table | Original MAIN location | Bytes | Original author |
| --- | --- | ---: | --- |
| `BFNT_ID` | `20D36..20D3C` | 6 | `BFNTID.ASM`, literal `BFNT`, `1Ah`, NUL |
| `EDGES` | `20D4C..20D6E` | 34 | `EDGES.ASM`, 17 actual 16-bit VRAM edge masks |
| `BYTE_MASK` | `2107C..21084` | 8 | `WORDMASK.ASM`, eight progressive one-byte masks |
| `note_dat` + `lcount` | `210B4..21164` | 176 | `B_DATA.ASM`, 24 pitch + 64 duration words |

The BGM source includes a real `UNDF` sentinel. Its value is independently
pinned from the original author `BGM.INC` as **100**, rather than guessed
from the decoded target. The complete 24-entry pitch table and 64-entry
note-duration table remain consecutive 16-bit words; the original linker
also exports a distinct `lcount` label 48 bytes after `note_dat`. The source
normalizer accepts numeric text only in the documented `DW`/`DB` forms; it
uses no table bytes copied from the original executable.

The original image's TASM DATA frame is **22h below** the retained calibration
frame. Each adopted position is verified against the actual 8000-byte `_DATA`
SEGDEF, genuine ordinary OMF LEDATA, original/public MAP offsets, and both
unaltered linked images. The complete four original target subarrays occur
uniquely and have no CODE or relocation claims.

Importantly, the two original zeros at `20D2E..20D30` after ATAN8, the
original `intdiv` word at `210B2`, and any unknown bytes after `21164` **stay
unknown**. They are not absorbed by adjacent tables; neither `glb` nor
uninitialized/relocated Master state has been credited.

Evidence: [`config/main_master_literal_tables_ownership.json`](../../config/main_master_literal_tables_ownership.json)
and its explicit decision
[`config/reviewed_main_master_literal_tables.json`](../../config/reviewed_main_master_literal_tables.json).
Run `python3 scripts/review_main_master_literal_tables.py --check` for the
bounded genuine source/OMF/MZ recheck. CI uses the structural check only,
without a whole-executable cold replay. All **224 bytes are third-party
initialized DATA** with zero authored credit.

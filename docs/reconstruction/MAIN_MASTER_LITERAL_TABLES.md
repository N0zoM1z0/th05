# Seven original Master literal initialized-DATA tables in MAIN

This source-linked review resolves **306 formerly unknown DATA bytes**, all
third-party Master 0.23 original assembler initializers, not game-authored
C/C++ or instruction bytes. Each table has an exact original author source,
an independently retained native TASM initializer, full ordinary DATA LEDATA,
real MAP public, unique original target occurrence, and matching original /
calibration bytes with an empty ordered MZ relocation list.

| Source table | Original MAIN location | Bytes | Original author |
| --- | --- | ---: | --- |
| `BFNT_ID` | `20D36..20D3C` | 6 | `BFNTID.ASM`, literal `BFNT`, `1Ah`, NUL |
| `EDGES` | `20D4C..20D6E` | 34 | `EDGES.ASM`, 17 actual 16-bit VRAM edge masks |
| `EPSON_NOTES` | `20D74..20D7E` | 10 | `GETMAC98.ASM`, nine notebook IDs + zero sentinel |
| IBM video/font + `EXENTRY` | `20D7E..20D94` | 22 | `GETMACAT.ASM`, two nine-byte DOS device names and a zero far entry |
| Original 16-color palette + tone | `20DAA..20DDC` | 50 | `PAL.ASM`, one 16-bit 100% tone + 16 three-byte RGB colors |
| `BYTE_MASK` | `2107C..21084` | 8 | `WORDMASK.ASM`, eight progressive one-byte masks |
| `note_dat` + `lcount` | `210B4..21164` | 176 | `B_DATA.ASM`, 24 pitch + 64 duration words |

The EPS0N machine-specific list is not generic padding: it contains nine
explicit hexadecimal model IDs, followed by its original zero terminator.
The two original IBM device names are `$IBMADSP` and `$IBMAFNT`, each NUL
terminated; the same 22-byte author block ends with a genuine zero 32-bit
extension-entry initializer. Neither creates a fabricated code pointer.
`PAL.ASM` supplies the true 100% tone word and sixteen exact three-byte
RGB entries, including gray `77h` and the reduced-intensity `AAh` colors.
The surrounding live palette and detector state is not included.

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
unaltered linked images. The complete seven original target subarrays occur
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
without a whole-executable cold replay. All **306 bytes are third-party
initialized DATA** with zero authored credit.

# Eleven original Master literal initialized-DATA scopes in MAIN

This source-linked review resolves **333 formerly unknown DATA bytes**, all
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
| Original VRAM geometry | `20D94..20D9F` | 11 | `GRP.ASM`, four geometry words, zoom word and 55h mesh byte |
| Joystick startup state | `20DA0..20DA8` | 8 | `JS.ASM`, four actual zero-initialized WORD fields |
| Machine ID state | `20DA8..20DAA` | 2 | `MACHINE.ASM`, one actual zero-initialized WORD |
| Original 16-color palette + tone | `20DAA..20DDC` | 50 | `PAL.ASM`, one 16-bit 100% tone + 16 three-byte RGB colors |
| Resident palette flags | `20DDC..20DE2` | 6 | `PAL.ASM`, PaletteNote, ResPalSeg and SdiExists WORD defaults |
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
unaltered linked images. The nonzero literal tables occur
uniquely and have no CODE or relocation claims. The original zero-initialized
joystick, machine and palette runtime state fields cannot be identified by
searching for a zero-byte sequence. Their proof instead requires the actual
original public MAP symbol addresses, complete matched upstream/native
scalar declarations, ordinary source-written OMF LEDATA and exact full image
bytes. These fields can later change at runtime; the scope here is *only*
their initial source-defined bytes.

Importantly, the two original zeros at `20D2E..20D30` after ATAN8, the
original `intdiv` word at `210B2`, and any unknown bytes after `21164` **stay
unknown**. They are not absorbed by adjacent tables; neither `glb` nor
uninitialized/relocated Master state has been credited.

Evidence: [`config/main_master_literal_tables_ownership.json`](../../config/main_master_literal_tables_ownership.json)
and its explicit decision
[`config/reviewed_main_master_literal_tables.json`](../../config/reviewed_main_master_literal_tables.json).
Run `python3 scripts/review_main_master_literal_tables.py --check` for the
bounded genuine source/OMF/MZ recheck. CI uses the structural check only,
without a whole-executable cold replay. All **333 bytes are third-party
initialized DATA** with zero authored credit.

The single original zero after `GRP.ASM`'s 11-byte geometry/mesh initializer
at `20D9F` remains **unknown**; it is the boundary before the joystick fields
at `20DA0`. The source review does not claim the following file-buffer,
packed-file or random-seed defaults without their own complete source proof.

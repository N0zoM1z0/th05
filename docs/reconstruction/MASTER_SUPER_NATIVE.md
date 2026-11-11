# Native Master SUPER graphics source recovery — MAIN

Ten complete source-backed Master 0.23 assembly procedures in MAIN have
been recovered from the original archive and the genuine TASM-built MAIN
object, then relinked against the original game's data layout. They provide
**2,568 newly reviewed CODE bytes**, zero game-authored C++ credit.

| Function | Complete original MAIN extent | CODE bytes | Original CODE FIXUPP |
| --- | --- | ---: | ---: |
| `SUPER_ENTRY_PAT` | `2A2E..2ADA` | 172 | 4 |
| `SUPER_PUT_1PLANE` | `2ADA..2CA2` | 456 | 18 |
| `SUPER_ENTRY_AT` | `2CA2..2D16` | 116 | 10 |
| `SUPER_CANCEL_PAT` | `2DA0..2DF0` | 80 | 8 |
| `SUPER_CLEAN` | `2DF0..2E1A` | 42 | 2 |
| `SUPER_ROLL_PUT_1PLANE` | `2E1A..2FE0` | 454 | 15 |
| `SUPER_ROLL_PUT` | `2FE0..31F6` | 534 | 26 |
| `SUPER_PUT_RECT` | `31FC..333A` | 318 | 22 |
| `SUPER_PUT` | `33F0..34E0` | 240 | 16 |
| `SUPER_CONVERT_TINY` | `35A2..363E` | 156 | 4 |

## Source and compiler identity

The [scoped verifier](../../scripts/review_master_super.py) reads the
pinned author's original Master 0.23 distribution, the saved genuine
TASM32 OMF, actual calibration MZ, original MZ and active MAP/listing
boundaries from the existing Master native review. It verifies the
*complete* original assembly instruction text of each function against
the maintained port, with explicit and limited source adaptations:
comments/whitespace and the port's `@@`-scoped labels, plus the
`SUPERL1P_` / `SUPERPUT_` local names and the explicit shared
`SUPERPAT_NO_MEMORY` label. Instruction mnemonics, immediate values,
register operands and all other instruction text must still agree.

This is an independently sourced assembly-language **adaptation** of
Master, not a claim that the port's text is byte-for-byte the author's
literal original file. The compiled CODE is verified through the real
OMF source LEDATA and ordered FIXUPP records. The source is not created
from the original executable, and the original target is never edited.

## Original Borland/TLINK DATA fixups

The genuine calibrated OMF binds local `_TEXT` at offset `0272h`,
the monolithic `_DATA` at offset `0090h`, and `_BSS` at offset
`262Ch`. The actual original CRT startup independently establishes the
native DATA/INIT and BSS positions **18 bytes lower** than calibration,
while `_TEXT` is unchanged. Resolving every actual CODE FIXUPP through
these original symbol offsets reproduces each **complete original
function byte for byte**. All ten have the correct empty original
ordered MZ relocation stream.

The 456-byte one-plane renderer, 454-byte one-plane roll renderer,
534-byte full roll renderer and 318-byte clipped rectangular renderer are
recovered in full, including their local bytecode-facing operations.
Only the complete named procedure extents receive vendor CODE ownership;
adjacent callbacks, unnamed gaps, alignment outside the functions,
and the rest of the large `SUPER` family remain unknown.

## Reproduction and limitations

The [native evidence](../../config/master_super_ownership.json) and
[separate adoption](../../config/reviewed_master_super.json) pin the
complete source contribution boundaries, original OMF fixup actions,
native object/source identities and all raw linked CODE hashes.

```sh
python3 scripts/review_master_super.py --check
python3 scripts/review_master_super.py --structural-check
python3 scripts/ownership.py --check
```

Targeted negative trials changed an actual source LEDATA byte, changed
the original DATA/BSS fixup delta, and changed an instruction register
operand. Each failed the corresponding complete-byte or semantic-source
comparison. No compiler, full cold replay or game execution was needed:
the already-pinned native source-built TASM object is revalidated in the
affected scopes.

This is **source-backed third-party CODE ownership**, not authored game
code, not all instruction bytes (a CODE segment can include live data),
and not a full-game or packed-file reconstruction. The 98% authored-code
goal and its denominator are unchanged.


## Additional source-exact helper procedures

The separate [SUPER helper source review](../../scripts/review_master_super_helpers.py)
recovers **12 further complete original Master procedures (650 bytes)**,
bringing the now source-verified SUPER total to **3,218 CODE bytes** across
22 complete procedure extents. The new members are:

| Complete group | Original MAIN extents | Native CODE |
| --- | --- | ---: |
| `SUPER_ENTRY_BFNT` | `2D16..2DA0` | 138 B |
| `superptr_draw_shift`, `superptr_draw_noshift` and `superptr_draw` | `333A..3380`, `3380..33B0`, `33B0..33EF` | 181 B |
| `SUPERPUT_DISP1`–`DISP4` and `SUPERPUT_DISP` | `34E0..3503`, `3504..3531`, `3532..3568`, `3568..3599`, `359A..35A2` | 191 B |
| `SUPER_PUT_8` | `40E6..4162` | 124 B |
| `SUPERPAT_NO_MEMORY` and `SUPERPTR_EXIT` | `2A24..2A2E`, `31F6..31FC` | 16 B |

The independently pinned original Master 0.23 archive contains the full
`PROC/ENDP` bodies for the inner renderers/dispatchers. The maintained
port only namespaces their original patch/label names; the original
commands, immediates and control flow remain identical. The entry-BFNT
routine's original large-model `_push` is reconstructed through the
real active `LDATA` branch. Full TASM OMF LEDATA and ordered FIXUPP
reproduce all 12 complete original CODE ranges and their empty MZ
relocation streams. Adjacent `EVEN` alignment bytes at `3503`,
`3531`, `3599` and `33EF` remain outside these claimed functions.

Evidence: [source/OMF proof](../../config/master_super_helpers.json) and
[explicit adoption](../../config/reviewed_master_super_helpers.json).

```sh
python3 scripts/review_master_super_helpers.py --check
```

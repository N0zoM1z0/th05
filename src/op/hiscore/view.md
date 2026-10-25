# OP High Score viewer candidate

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/formats/scoredat/recreate.cpp`, `th04/hiscore/score_ld.cpp` and
`th04/hiscore/view.cpp`, selected for **GAME=5 / BINARY='O'**. The owner keeps
score recreation, load/decode recovery, gaiji score rendering, viewing and
unlock-state loading. It contains no ASM, emit, keep-zero helper, copied
instruction stream, opaque data array or code-generation barrier.

Canonical files are UTF-8, CP932-stage-compatible. This unit's seven filename
and song literals are ordinary ASCII, with no Japanese UI literal payload.
Existing OP/resident/rank/sound types and filename macros are reused without
editing accepted headers. The gaiji digit arithmetic deliberately preserves
the original signed integer promotion and overflow behavior; it is not clamped
or rewritten as raw BCD digits.

## Complete original code

Packed OP SHA-256:
`c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb`.
This work uses the independently observed decoded 77,798-byte payload,
SHA-256 `7c112a4a7dc4231e9be2d0f69555f0736f69165c80621a3fcd67324dad77ec47`.
Addresses below are decoded load-module offsets, not packed-file positions.

Original contribution **`[C8E2,CE65)`**, **1411 bytes**, SHA-256
`a5a9e27718c08b1ff90f4de951e7dca254269349a2c7e5b739c6b46968487120`.

| Function | Half-open original span | Instructions | CODE-data |
| --- | --- | ---: | ---: |
| `scoredat_recreate` | `C8E2..C9BE` | 220 | 0 |
| `hiscore_scoredat_load_for` | `C9BE..CA1B` | 93 | 0 |
| `score_put` | `CA1B..CAB0` | 149 | 0 |
| `stage_put` | `CAB0..CB00` | 80 | 0 |
| `place_put` | `CB00..CBDC` | 204 | 16 |
| `rank_render` | `CBDC..CC5C` | 128 | 0 |
| `regist_view_menu` | `CC5C..CD94` | 312 | 0 |
| `cleardata_and_regist_view_sprites_load` | `CD94..CE65` | 209 | 0 |

The complete extent contains **1395 instruction bytes / 507 instructions +16
semantic switch-table bytes**, with no padding. All 54 local branch targets
are instruction starts. The load helper has multiple real returns: its last
six bytes remain instructions, not a fabricated boundary after the first RET.
The two four-entry place switches occupy **`[CBCC,CBD4)`** and
**`[CBD4,CBDC)`**, unit-relative **`[2EA,2F2)`** and **`[2F2,2FA)`**. All eight
entries point to instruction starts in the same function. Maintained source
contains the semantic switches, not address-word arrays. The original code
has **50 ordered MZ segment fixups**, all retained in full comparison.

Use wrapper `th05/hi_view.cpp` including `src/op/hiscore/view.cpp`, the OP
context (`BINARY='O'`), `SCORE_TEXT` / `op_01`. Original frame is **`0A39`**,
load base **`A390`**, code group offset **`2552`**; DGROUP frame is **`0EFE`**.

## Complete score/state ABI

The canonical eight-byte `score_lebcd_t` union is reused. `scoredat_t` is
**92 bytes**: five nine-byte names at 0, five eight-byte gaiji scores at 45,
five stage glyphs at 85, clear byte at 90 and real unused byte at 91.
`scoredat_section_t` is **96 bytes**: signed key bytes at 0 and 1, signed
checksum word at 2, payload at 4. Every field and complete size is asserted;
no offset spacer is substituted for actual record fields.

The OP codec interfaces remain near Pascal with **no arguments**; decode
returns a byte. Both real score sections are retained because the OP decode
helper also processes `hi2`, despite its absence from TH05's rendering path.
The load helper takes a real signed-word `playchar2`, not the byte character
enum. File I/O retains far buffers and filenames, unsigned-word sizes and the
true signed-long seek argument.

Source-owned BSS is logical DGROUP **`[5060,5137)`**, **215 bytes**, with no
internal padding: `hi` at `5060` (96), `hi2` at `50C0` (96), unused byte at
`5120`, rank at `5121`, 4×5 clear-state bytes at `5122`, and `extra_unlocked`
at `5136`. These logical BSS addresses lie beyond the stored decoded payload;
their types and operand positions are reviewed, but no BSS byte-copy or
authored-byte credit is claimed. No `.stack` or duplicate owner objects belong
in the bounded linker context.

Source-owned initialized DATA is DGROUP **`[2818,284D)`**, **53 bytes**,
SHA-256 `04f3c8a04a428d1a927bc78956634e01f6ec535369425844abd474c628070d03`.
It comprises seven natural terminated strings: `GENSOU.SCR`, `name`,
`hi01.pi`, `op1.pi`, `op`, `scnum.bft` and `hi_m.bft`. There are no DATA
fixups, pointer tables or padding in this extent. These are filenames/song
names, not copied game assets.

## Bindings and validation packet

Near external codec destinations are `@SCOREDAT_DECODE$QV` at load `C7D5`,
op_01:`2445`, and `@SCOREDAT_ENCODE$QV` at `C87E`, op_01:`24EE`.
All other 23 external callees are far, preserving their real C/C++, Pascal
cleanup and return types. Exact names, frames and every call site are in
`.analysis/op-hiscore-boundary-review.json` and the unbuilt symbol-only
`.analysis/op_hiscore_bindings.asm`.

The only external globals are the resident far pointer at DGROUP:`2DEC` (4),
input word at `3A92` (2), palette tone at `054E` (2) and four character-unlock
bytes at `513F`. All high-score viewer state remains compiler-owned. The
private binder contains only labels and outside-owned ORG holes, with no
instructions, string values, score payload or artificial stack.

A natural negative control changes the unique
`PLACE_1_PADDING_BOTTOM = 8` to 7, altering displayed row placement. No
source-current exact acceptance or packed-container equality is claimed before
focused cold raw-byte/fixup replay.

## Accepted complete function subset

The original `op-hiscore-view-b` receipt retains its failed aggregate: all
1,411 raw bytes match but the 312-byte `regist_view_menu` has differing ordered
fixups and remains unaccepted. Seven other whole functions pass both raw and
ordered comparisons, totaling 1,099 bytes (1,083 instructions, 16 tables).
`op-hiscore-scopes-a` derives and validates these complete scopes from the two
unchanged original cold producers, including the actual negative-control
owner, without another compiler invocation. It archives the intact parent
and recomputes real MAP boundaries, OMF identities and negative output.

The later canonical factor supersedes those seven records with fresh current
evidence and separately accepts the complete312-byte menu. All three receipts
`op-score-code-canonical-a`, `op-score-files-canonical-a` and
`op-score-menu-canonical-a` passed and were imported atomically: the seven
CODE scopes share their actual place-padding negative, while DATA53 and menu312
each have their own compiled negative. The original mixed receipt and its
menu-order failure remain unchanged. See `canonical_menu.md` for actual source,
resource ownership and validation details; no relocation normalization or
packed-container acceptance is claimed.

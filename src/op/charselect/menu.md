# TH05 character-selection candidate

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/m_char.cpp`,
`th04/op/darken.cpp`, `planar.h` and `th04/op/impl.hpp`.
The complete candidate includes darkening because its source is a real pair
of C++ loops and a typed far-memory assignment. It contains no ASM, emitted
instructions, optimization barriers or reconstructed helper instruction bodies.

`VRAM_PLANE_B` remains the actual **external four-byte far-pointer object**;
it is not replaced with a hardcoded hardware address. The source writes the
genuine alternating `AAAAAAAA` / `55555555` graphic patterns through that
pointer as `uint32_t`. These are semantic 1bpp drawing masks, not executable
bytes. Signed VRAM offsets, byte arithmetic, word booleans, full four-character
arrays and the volatile vsync counter retain their original types. The shared
resident, rank and character domains are reused without accepted-header edits.

## Complete original boundary

Packed OP SHA-256:
`c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb`.
The independently observed decoded 77,798-byte payload has SHA-256
`7c112a4a7dc4231e9be2d0f69555f0736f69165c80621a3fcd67324dad77ec47`.
All offsets below refer to that decoded load module, not the packed file.

Complete contribution **`[CE65,D303)`**, **1182 bytes**, SHA-256
`dda77b9a9f592deef8bd40d62a62577bd218b7c6dd5ea990a3a8ec8953151274`.

| Function | Half-open original span | Instructions | CODE-data | Padding |
| --- | --- | ---: | ---: | ---: |
| `pic_darken` | `CE65..CEFF` | 146 | 8 | 0 |
| `pic_put` | `CEFF..D095` | 397 | 8 | 1 |
| `playchar_menu_put_initial` | `D095..D12D` | 152 | 0 | 0 |
| `playchar_menu` | `D12D..D303` | 470 | 0 | 0 |

All **393 instructions / 1165 bytes** decode through the real returns, including
the final RET at `D302`; all **48** local branch targets are instruction starts.
The two semantic four-entry tables are `[CEF7,CEFF)` and `[D08D,D095)`, or
unit-relative `[092,09A)` and `[228,230)`. All eight words target instruction
starts in their own function. Source contains semantic switches, not table
arrays. The observed zero at `D08C`, unit-relative `227`, is alignment and
receives no credit. Potential authored code is **1181 bytes**, after excluding
that byte while retaining it in full raw comparison. There are **40** ordered
original code fixups.

## State and source data

Wrapper `th05/m_char.cpp` should include `src/op/charselect/menu.cpp` with the
OP (`BINARY='O'`) context, `M_CHAR_TEXT` / `op_01`, and retained `-a2` pragma.
Original op_01 frame is **`0A39`**, load base **`A390`**, unit offset **`2AD5`**;
DGROUP frame is **`0EFE`**. Canonical UTF-8 files are CP932-stage-compatible;
the sole source-owned string is ASCII `slb1.pi`.

Initialized DATA is DGROUP **`[284E,2856)`**, eight bytes for that terminated
filename. It has no fixups or padding. Uninitialized state is logical DGROUP
**`[5138,5147)`**, 15 bytes: selection at `5138`, original unused byte at
`5139`, menu rank at `513A`, original unused four-byte member at `513B`, four
character-unlock bytes at `513F`, and four selectable bytes at `5143`.
The unused members preserve the real source state rather than substituting
an invented layout spacer; no BSS authored credit is requested. Both arrays
retain all `PLAYCHAR_COUNT` entries. The original local input-history variable
is preserved without adding an initializer or changing its byte width.

External globals are the real VRAM far pointer at `0AA4` (4), volatile
`vsync_Count1` at `2E4E` (2), clear matrix at `5122` (20), palette tone at
`054E` (2), resident far pointer at `2DEC` (4), and input word at `3A92` (2).
All 20 external callees are far; their exact C/C++ linkage, frames and call
sites are in `.analysis/op-charselect-boundary-review.json` and the private
`.analysis/op_charselect_bindings.asm`. No foreign helper body is synthesized.

## Important linker context boundary

The real owner ends at **`D303`**, three bytes beyond the observed shared far
frame base **`D300`**. Moving the complete owner backward or truncating its last
three bytes is invalid. The unbuilt binder therefore lets the owner finish,
then uses one outside-owned alignment byte and a word-aligned context at
**`D304`**. The linker must retain its true paragraph frame `0D30`, adding the
four-byte contribution bias to callee offsets. Calibration MAP corroborates
that layout; the context itself is synthetic and carries no external ownership
or whole-program placement claim. Its exact frames require cold linker checks.

All binder labels and ORG holes are outside compiler-owned CODE/DATA/BSS.
There is no artificial `.stack`, byte value, instruction or owner-state alias.
The typed far-VRAM source, two CODE tables and complete relocation list must
all pass unmasked comparison before acceptance.

A natural negative control changes the unique `RAISE_W = 8` to 7, altering
actual selected-picture geometry. No source-current exact acceptance or packed
OP.EXE equality is claimed by this packet.

## Accepted focused replay

`op-character-menu-a` validates both genuine linker contexts and all 1,182
complete bytes / four functions: 1,165 instruction bytes, 16 compiler-table
bytes and one excluded zero padding byte. All 40 ordered fixups and the compiled
geometry mutation pass. Eight initialized DATA bytes match both producers with
no added credit; BSS remains layout evidence.

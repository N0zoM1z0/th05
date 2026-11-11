# Seventeen further complete original Master functions: 1,079 CODE bytes

Seventeen previously unknown complete MAIN functions are now attributed to
**original Master 0.23 third-party assembly**. They are source-linked from the
pinned author's CP932 archive and retained native TASM object, checked against
both the actual calibration MZ and the original Japanese MAIN MZ. No original
machine-code bytes, guessed padding or external symbol implementation are
supplied by a binder.

| Original Master functions | Full CODE bytes |
| --- | ---: |
| RTC `rtc_int_set`, `RTC_INT` | 213 |
| BFNT `BFNT_PALETTE_SET` | 64 |
| Text `TEXT_FILLCA`, `TEXT_PUTSA` | 170 |
| Display `GAIJI_PUTCA`, `GRAPH_CLEAR`, `IRAND` | 146 |
| VSYNC `VSYNC_START`, `VSYNC_COUNT`, `VSYNC_END`, `VSYNC_WAIT` | 274 |
| Palette `PALETTE_WHITE_IN`, `PALETTE_WHITE_OUT` | 128 |
| EMS `EMS_EXIST`, `EMS_SETNAME`, `EMS_SPACE` | 84 |
| **Total** | **1,079** |

The original assembly listing supplies every complete PROC boundary, including
RTC `0454..04E5`, the full 114-byte `TEXT_PUTSA` at `2598..260A`, and the
adjacent VSYNC family at `260E..272A`. The full set contains **71 original OMF
fixup actions**. Each procedure has complete source LEDATA coverage and
matches every original raw CODE byte and actual *ordered* MZ relocation (empty
for these source scopes), not a matched prefix or patched normalization.
All 17 original image byte occurrences are unique at their reviewed bounds.

The source comparison permits only reviewed, semantic-preserving spellings:
private RTC/VSYNC hardware port and label prefixes, the `RTC_INT` local
`skipslot1` label rename, `BFNT_HEADER.col` typed-field syntax, explicit
`word ptr` on a text argument, and `NOPCALL` for the original linker's
relaxed far-to-near call site. The pinned native OMF and original MZ still
compare literally, including any emitted relaxation NOPs. The call, register,
branch, word and real storage operands are not removed or inferred. Each
procedure additionally matches its complete original author's ASM block
under these restricted spellings; the evidence records the original archive
member and hashes for both source blocks.

The authoritative source/link proof is
[`config/master_gap_functions_ownership.json`](../../config/master_gap_functions_ownership.json).
The separate adoption decision is
[`config/reviewed_master_gap_functions.json`](../../config/reviewed_master_gap_functions.json).
Recheck only these scopes using `python3 scripts/review_master_gap_functions.py
--check`; public CI runs its structural source-identity check without native
tools. Ownership remains gapless, and prior accepted C/C++ or ASM units are
not replayed. These are **vendor CODE bytes, zero game-authored credit**;
all unreviewed neighbors retain their unknown classification and the authored
denominator is still not measured.

## Three complete private near procedures (202 additional CODE bytes)

The original Master archive and the retained native TASM OMF now also
reconstruct three complete source-written functions in TH05 MAIN:

| Original source procedure | MAIN decoded extent | CODE bytes | OMF fixups |
| --- | --- | ---: | ---: |
| `LARGEPUT_DISP8` (author `LARGEPUT.ASM` `DISP8`) | `20DC..2121` | 69 | 2 |
| `make_linework` (author `MAKE_LIN.ASM`) | `2122..2158` | 54 | 0 |
| `SUPERPT8_DISP` (author `SUPERPT8.ASM` `DISP`) | `4162..41B1` | 79 | 0 |

These real private near procedures are not guessed from a matching byte prefix.
Their complete boundaries come from the original TASM listing and their actual
source-led CODE lengths. The archived `DISP8` body differs only in private
`LARGEPUT_` label names; the archived `DISP` differs only in its namespaced
procedure name; `make_linework` preserves all arithmetic and control flow,
with namespaced linework fields and an explicitly typed word store. Each
whole normalized author source block matches the actual compiler input under
exactly those renames. Original and calibrated MZ raw bytes and ordered
relocations match, with the original two offset16 OMF fixups preserved in
`LARGEPUT_DISP8`.

**Two adjacent non-procedure bytes remain unknown**: at `2121`, calibration
emits an `EVEN` NOP (`90`) while the original contains `00`; at `41B1`, a
zero follows the private `SUPERPT8_DISP` return. Neither byte is swallowed by
the restored function extent, given instruction credit or normalized away.
The enlarged evidence/decision now cover 20 source-written functions and
**1,281 bytes overall**, 202 more than the previous 17-function review.
All 202 additional bytes remain Master third-party CODE with zero authored
C++ or game-authored ASM credit.

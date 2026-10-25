# Default midboss rewards and defeat candidate

Natural-source provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/mb_dft.cpp` including
`th04/main/midboss/defeat.cpp`, GAME=5. The owner keeps the real randomized
bonus-popups and defeat state transitions, reusing the canonical 22-byte
midboss, 24-byte Boss and callback types through the maintained stage interface.
It supplies no instruction emissions, fake helpers or partial object layouts.

Original MAIN **`[1C54E,1C669)`**, **283 bytes**, contains:

| Function | Original half-open span | Bytes |
| --- | --- | ---: |
| `midboss_score_bonus` | `1C54E..1C5B8` | 106 |
| `boss_score_bonus` | `1C5B8..1C628` | 112 |
| `midboss_defeat_update` | `1C628..1C669` | 65 |

All 106 original instructions decode contiguously through actual returns.
All 14 local branch destinations are instruction starts. There are no CODE
tables, padding, MZ fixups or source-owned DATA/BSS. The two bonus values
deliberately preserve the real type distinction: midboss `unsigned int` 1280
versus Boss `unsigned long` 1000. That distinction changes multiplication
width and is part of the source algorithm.

The reference writes an explicit `PUSH CS` / near call of the far
`midboss_reset()` in the final function. This owner instead uses the genuine
typed far C++ call. Original bytes encode four total bytes at `1C663`; natural
compiler/linker relaxation is unproven. If a five-byte call is produced, the
entire final 65-byte function remains inexact and unaccepted. Nothing pads,
patches or reclassifies it. The first two complete functions provide a separate
218-byte candidate scope if independently confirmed by strict cold replay.

Wrapper `th05/mb_dft.cpp` uses `MB_DFT_TEXT/main_03`, original frame **`1527`**
and group offset **`72DE`**. DS is **`209D`**. Real external interfaces are:

| Symbol | Original load destination | ABI |
| --- | --- | --- |
| `@RANDRING2_NEXT16_MOD$QUI` | `152C0` | C++ near Pascal, unsigned word argument/result |
| `@POINTNUMS_ADD_YELLOW$QIIUI` | `16E28` | C++ near Pascal, two signed subpixel words and unsigned points word |
| `@midboss_reset$qv` | `1C4A1` | C++ far C order in actual main_03 |

External state is `pointnum_times_2` at DS `18AA` (1),
`boss_phase_timed_out` at `1FC8` (1), `playfield_shake_anim_time` at `3520` (2),
`score_delta` at `3712` (4), `midboss` at `5AA4` (22), `boss` at `5ABA` (24),
and `midboss_active` at `C4AA` (1). The scaffold only labels these real objects.

The standalone symbol context uses a separate paragraph-aligned CODE segment
after the whole compiler contribution. Both an original-size end at `1C669`
and a possible natural-call end at `1C66A` align to **`1C670`**, keeping DS
placement stable without an origin hole inside any function. Verify the actual
MAP tail before using this diagnostic scaffold. The source contribution still
retains its actual compiler size and complete-function boundaries.

Private `.analysis/midboss-default-boundary-review.json` records original
boundaries, call encodings, globals and the unresolved reset-call shape.
A natural negative control changes the unique
`MIDBOSS_BONUS_UNIT_VALUE = 1280` to 1281, altering the actual midboss score and
popup labels. No source-current exact acceptance is claimed.

## Accepted complete bonus functions

`main-midboss-bonuses-b` accepts the two full bonus functions, 106 and 112
instruction bytes, through independent cold producers and the compiled
1280-to-1281 reward-value negative. Both use their actual next function as the
end boundary. The first declaration of the real random helper belongs to
main_03 before including foreign main_01 callback declarations; restoring this
actual frame fixes both near calls without synthesizing helper code.

The complete original 65-byte defeat update remains unaccepted: its natural
far reset call produces one extra byte, giving 66. The outside-owned paragraph
context preserves original DS without padding or truncating that function.
The failed whole-contribution diagnostics retain their original verdict.

## Later local-definition acceptance

The new complete six-function lifecycle/HP/rewards TU restores the genuine
local-definition context for the typed far reset call. Its full456 bytes
match, and only the previously missing65-byte defeat update is imported.
See [complete midboss lifecycle](lifecycle.md). The old two bonus acceptance
rows and all state/HP/default source identities remain unchanged; the old
66-byte failed result is preserved rather than relabeled.

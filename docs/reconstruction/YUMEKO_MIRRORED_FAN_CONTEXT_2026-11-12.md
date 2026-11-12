# Yumeko sword fan: mirrored angle and reposition protocols

The complete four-function `main-yumeko-patterns` context uses the same
real mirrored-side flag twice per sword-fan shot: first it transforms the
sword's aim before computing the offset launch position, then restores the
base angle before the next shot. Both operations now use
`YUMEKO_SWORD_FAN_MIRROR()`. The sword-fan and red-ring attacks also share
the exact phase-clock reset and entry into `YUMEKO_MODE_REPOSITION`, without
changing their distinct timing, sprite, RNG, bullet or sound behavior.

`patterns.cpp` is included in the real nine-function Yumeko context, so the
full dependent acceptance closure was replayed rather than only compiling
the small edited regions:

| Source owner | Original bytes | Ordered native relocations |
| --- | ---: | --- |
| `main-yumeko-patterns` | 435 | `[413,403,353,232,34]` |
| `main-yumeko-aimed-swords-context` | 354 | `[71,329,309,203]` |
| `main-yumeko-laser-swords-context` | 428 | `[232,72,402,382]` |

Two genuine Borland/TLINK producers per owner match every complete raw byte
and original relocation order; the existing compiled negative was rejected.
Evidence: `.analysis/unit-replays/gpt-web-yumeko-mirrored-fan-reposition-context-20261112-a/receipt.json`.
The already accepted 283-byte `swords_update()` remains a reviewed ASM owner;
its separate natural C++ attempt is still inexact. No duplicated authored
CODE byte credit is taken for these source refactors.

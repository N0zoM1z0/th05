# MAIN Extra midboss: exact initial callback, 3×2 attacks and dash bearings

The original decoded MAIN interval `[21E4A,21E60)` is now one complete
**22-byte** source-defined initialized C++ contribution. Its real live
consumer is the separately accepted 366-byte `midbossx_update()`, which
changes `midbossx_pattern` after every dash and uses a 3×2 callback
selection indexed by its existing sixteen-byte scratch object.
`midbossx_dash_update()` and the four real near attack callbacks belong
to the independently accepted complete 440-byte original five-function
`extra_patterns.cpp` contribution.

The original near `_DATA` objects are exported by the source under
the canonical names and types already declared in `extra.hpp`:

| Original DS offset | Natural C++ initializer | Bytes |
| --- | --- | ---: |
| `147A` | `midbossx_pattern = midbossx_pattern_wait` | 2 |
| `147C` | `midbossx_patterns[3][2]` | 12 |
| `1488` | `midbossx_dash_angles[8]` | 8 |

The first two attack rows are genuinely
`{ spread, random }` and `{ decelerate, decelerate }`; the third row
holds two original null pointers, and is not selected by the real
0/1 `second_pattern_set` state. The eight physical dash headings are
`10,70,80,80,90,F0,00,00` in hexadecimal angle units, including the
two repeated 0x80 headings and the terminal zeros. These are ordinary
source-level near-C++ function addresses and direction selectors, not
copied code bytes, glyph pixels or a compiler switch table.

The symbol-only binder preserves the authentic `main_01`, SHARED and
`main_03` CODE frames, with real near callbacks at main_03 offsets
`1234,1246,12A7,12DE` derived independently from the full five-function
original MAP and actual machine-code function boundaries. It supplies
*no* callback body, angle data, pointer words, or candidate initialized
bytes. An initial isolated binder wrongly omitted the empty, genuine
`MAI_TEXT`, `GENERIC_BOSS_MAIN01_TEXT` and `BOSS_TEXT` source CODE groups,
causing Turbo Link to reject an oversized `MAIN_01` group. Restoring
those real outside segment declarations fixes the linker topology
without changing the 22-byte source initializer or introducing a
candidate-code ORG hole.

The two independent pinned Borland C++ builds in
`.analysis/unit-replays/gpt-web-extra-midboss-natural-schedule-c/receipt.json`
match all 22 original data bytes, true single initialized-DATA
OMF/LEDATA and MAP scope, and empty original ordered MZ fixups. The
compiled negative replaces the second callback in the first row with
the spread callback; this changes the real linked near address and is
rejected. The preceding single unknown byte `[21E49,21E4A)` and
following six unknown bytes `[21E60,21E66)` remain unowned. No
historical translation-unit identity is inferred from this scoped
proof, and no whole-program cold replay was executed.

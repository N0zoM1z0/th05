# TH05 frame-step debug state: first two MAIN initialized bytes

The first two bytes of the game's actual original `_DATA` contribution,
MAIN `[20A60,20A62)` (DS `209D:0090..0092`), are a signed one-byte
`debug_frame_step` and a one-byte `debug_frame_step_enabled` flag. The
original `th05_main.asm` starts the DATA segment with two explicit `db 0`
declarations; the real retained TASM object has a complete ordinary first
LEDATA containing both zeros, not an unwritten BSS reservation.

The native accepted frame loop reads the enable flag at DS:0091 and uses
DS:0090 for the signed step values `FE`, `FF`, `00` and `01` when Q toggles
single-frame advancement. The separately accepted 803-byte stage-session
initializer explicitly writes `1` to DS:0091 when debug mode is enabled.
These consumers establish the roles and byte widths despite the generic
names attached to the original two source `db` declarations.

`debug_frame_initial.cpp` naturally defines those two distinct scalar C++
objects in their original order. Two genuine Borland/TLINK producers matched
the complete two-byte `_DATA` extent, original MAP/OMF placement and empty
ordered MZ relocation stream. The compiled mutation enabling frame stepping
at startup was rejected. Focused evidence:
`.analysis/unit-replays/gpt-web-main-debug-frame-steps-20261112-a/receipt.json`.
This adds **two original game-authored initialized DATA bytes**, without
rebuilding the already accepted gameplay loop or stage initializer. The
following pause-action glyph and eyecatch resources retain separate owners.

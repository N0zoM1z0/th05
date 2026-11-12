# Exact initial score-extension and high-score-popup flags

The original MAIN bytes `[21D42,21D44)` at DS `209D:1372` are two distinct
adjacent mutable one-byte states. Their original source is pinned ReC98
`th04/score[data].asm`, which explicitly declares:

- `extends_gained`: initialized to zero; point-item extend logic increments
  it and compares its next threshold, while the Stage All Clear bonus resets
  it to the canonical story extension value.
- `hiscore_popup_shown`: initialized to zero; score rendering latches it after
  the first new high-score popup, and the reset controller clears it.

The actual accepted MAIN item-family, Stage All Clear, HUD score and score
reset routines independently read or write exactly those two native DS byte
addresses. The source `score_extend_initial.cpp` emits a complete two-byte
ordinary C++ `_DATA` contribution using the canonical unsigned-byte types.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-score-extend-flags-20261112-a/receipt.json`.
Two genuine original Borland/TLINK producers match both bytes, actual MAP/OMF
scope and empty original ordered loader relocations. The compiled mutation
starts `extends_gained` at 1 instead of 0 and is rejected. This adds two
source-authored initialized DATA bytes; surrounding independently accepted
HUD tables remain separate.

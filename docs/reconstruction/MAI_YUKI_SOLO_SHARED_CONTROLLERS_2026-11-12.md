# Mai/Yuki: one native solo-wave protocol across two complete Boss controllers

The separately accepted Mai (786-byte) and Yuki (826-byte) ten-stage solo
Boss controllers contain the same genuine three-statement reposition
completion: reset the phase clock, advance attack mode and increment the
pattern counter. Both also have the same first/middle-wave shot gate, with a
switch-exiting `break` for a miss and a character-specific hit score.

`src/main/boss/mai_yuki/solo_wave_common.hpp` now supplies two source-only
protocols. `MY_SOLO_NEXT_PATTERN()` preserves the three original writes and
their order in all six call sites. `MY_SOLO_HIT_BONUS_OR_BREAK(score_bonus)`
retains the actual outer-switch break, original shot test, and different
Mai/Yuki bonus constants at four call sites. The header adds no executable
helper, runtime storage, allocation or synthetic compiler barrier. Both
controllers keep their own native shadow movement, HP gates, laser cycles,
animations and defeat handling.

The focused dependency plan selected **both complete affected owners**.
Independent original Borland/TLINK producer rounds reproduce every one of
their **1,612 combined original CODE bytes**, each original compiler switch
table and all original ordered MZ relocations; the compiled semantic negative
is rejected. Final accepted scoped receipt:
`.analysis/unit-replays/gpt-web-mai-yuki-shared-protocol-format-final-20261112-b/receipt.json`.
The original 786/826 CODE was already accepted; this adds no duplicate
source-authored CODE credit and requires no full cold replay.

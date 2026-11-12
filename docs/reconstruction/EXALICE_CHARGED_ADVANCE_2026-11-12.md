# EX-Alice: regular and charged HP ladder handoffs

The complete natural 1,060-byte EX-Alice controller now expresses the first
three charged attack handoffs using `EXALICE_CHARGED_ADVANCE`. Each handoff
advances the real Boss HP threshold, performs its distinct explosion type
and installs the next attack callback. The fourth charged wave deliberately
uses only `exalice_phase_next()` before the terminal fan phase, preserving
its original special behavior and background changes.

The existing `EXALICE_REGULAR_ADVANCE` remains responsible for the separate
four ordinary-wave transitions. Neither the charged nor the regular rule
changes combat timers, sprite palette logic, hit scoring or the callback
order. The complete shared near/far compiler context still includes the
33-byte shot gate and 78-byte phase helper.

Focused replay:
`.analysis/unit-replays/gpt-web-exalice-charged-advance-20261112-a/receipt.json`.
Two genuine Turbo C++/TLINK producers reproduced **1,060 original bytes**,
all three original switch tables and ordered MZ relocations `[198,161]`,
while the compiled initial-HP negative was rejected. This updates the
already accepted large Boss source, with no duplicated CODE credit.

# Alice puppet motion: full two-function source

The two original puppet callbacks are accepted as a 643-byte C++ CODE
contribution. `alice_puppets_update()` now shares the genuine fractional
X/Y pursuit rule through `ALICE_PUPPET_SETTLE_AXIS(axis)`: each coordinate
first moves by half the 16-subpixel unit, then by one quarter of the residual,
then snaps to its previous position when both truncated increments are zero.
X still updates before Y. No new function call, state, or divide approximation
was introduced, and damage, sprite selection, death and recovery are unchanged.

The complete scope was recompiled by two Turbo C++/TLINK producers and matches
all 643 original bytes and ordered relocations. The existing compiled
negative was rejected. Evidence:
`.analysis/unit-replays/gpt-web-alice-xy-settle-20261112-a/receipt.json`.
This refreshes the already accepted owner without double-counting CODE bytes.

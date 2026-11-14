
## 2026-11-14: full attack-cycle regression coverage

The Stage 5 update's movement and attack subphase are now pinned together in
`tests/test_midboss5_lifecycle.py`. The four-step flight selector is
**left/right/right/left**, each dash runs 32 frames, and the three near
callbacks remain ordered blue spread, green randomized ring, aimed stacks.
Blue and green attacks both fire on every fourth frame from 32 through 96
(inclusive): 17 volleys each. Blue emits 13-way spreads at speed5.5 and angle
step7; green emits 16-shot rings at speed2 with two independent random position
offsets in `[-32,+32)` and a separately randomized angle. The aimed callback
fires only once at frame32, emitting one five-layer aimed spread stack and a
32-shot aimed ring stack before completing at frame64.

The callback table is a true three-entry near-pointer DATA object, not an
inline switch. Starting from the initial blue callback and incrementing the
completed count before indexing `patterns_done % 3`, the sixteen executed
attacks are **6 blue, 5 green, 5 aimed**. The sixteenth movement completion
selects green and advances the subphase, but the budget check jumps to the
explosion before the selected pattern or the normal shot-hit/reward tail runs.
Actual HP defeat instead sets bullet zap, awards30 score units and drops a
1UP. The tests also pin the 192-frame entrance, 32-frame movement truth,
charge/sprite keyframes, scratch bytes13/14/15 and the shared defeat return.

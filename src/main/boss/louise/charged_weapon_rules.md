# Louise complete charged weapons, mirrored fans and laser sweep

The original stage-four Louise attack family has three complete early
functions (429 machine bytes) and four distinct later functions
(603 machine bytes), all compiled from natural C++ against the same
16-byte Louise Boss scratch record. `charged_weapon_rules.hpp` names
the real source-level schedules, sprite angles, per-rank stack widths
and sounds without adding runtime storage or replacing a callback.

**The shared charge leaf** begins collecting visual circles at phase
frame 16 (colors 9/8, sound 8), advances the Boss to the charge sprite
and returns the original one-byte `INITIALIZE` result at frame 32.
It then returns `FIRE` until its attack-specific ending frame,
followed by `FINISH`. Blue spreads finish at frame 64 and red stacks
at frame 96. The blue volley fires every two frames, always emitting
both the selected side and its 0x80 mirrored partner. Its packed
five-projectile, six-angle-step spread, 0x20/0x60 side selection,
0x87/0x79 rotation, speed increment 4 and cap 0x24 all remain
original. Red stacks have rank-dependent counts 10/12/12/14 and
speed steps .3125/.3125/.375/.375, an initial negative 0x40 angle
and original two-frame, eight-angle-step emission with sound 15.

**Later fans** use an independent 32-frame cadence and alternate on
64-frame boundaries between 0x24 and 0x64 start angles. Each of the
eight original subvolleys emits four reflected shots at mirrored
0x40/0xC0 axes with decreasing speed step .3125. **Sweeping lasers**
finish charging at frame 128, use the real six-pixel width, color 8,
-16 start angle, 30-frame moveout, 6.5-pixel shootout, and turn by ten
on every four-frame event until their wraparound stop range. The
separate turning ring retains its 24×8 spread, five-stack speed step
.5625 and randomized ±0x20 turn. The aimed pellet routine fires
32-shot linear spreads every 32 frames with opposite ±0x1f aiming
on alternating 64-frame periods. All real bullet-template writes,
bit-sized states and C++ calling conventions remain unchanged.

Two independent pinned Borland compiler rounds reproduce all **429 +
603 original CODE bytes**, original OMF/MAP extents and literally ordered
MZ fixups; their actual compiled semantic negatives are rejected:
`.analysis/unit-replays/gpt-web-louise-charged-weapon-a/receipt.json`.
The existing entire **582-byte Louise Boss state machine** and its
**122-byte movement leaf** were also selectively compiled twice, with
full raw and fixup equality and their compiled negatives rejected:
`.analysis/unit-replays/gpt-web-louise-charged-boss-consumers-a/receipt.json`.
No previously accepted CODE is credited twice; no whole-game cold replay
or machine-code padding was performed.

# Sara stage-one attack projectiles and Boss entrance clocks

The maintained complete **1,824-byte, twelve-function** Sara C++ source now
uses `combat_wave_settings.hpp` to expose the real stage-one blue/red
projectile shapes and source-level entrance choreography. The compiler
constants cover the 1.5-pixel blue volley, aimed red spread/stack group
`(5,0x10,5,0.4375)`, the independent red 8-stack (step 0.375), its
backward 0x80 angle offset and the original sound 15. All real
`bullet_template` fields, near callback calls and existing 16-byte
Boss scratch union remain unchanged.

The second wave's pellet arc uses two independently randomized angles,
computed from the existing phase clock using a two-times/0x40 center
mapping. Its special linear three-shot spread uses a 3-unit angle
step and velocities 1.0–3.0 px/frame; its following blue ball uses
1.5–3.5 px/frame. The third wave's independent red ring speed remains
2 px/frame and its original shared Boss phase still accumulates speed
for the clockwise/counterclockwise spirals. The final corridor keeps
the real 5/6/7/8 rank-dependent spread counts, speed 2 for the linear
spreads and 1 for the random blue balls, and the existing stage-frame
modulo-16 firing gate. No missing projectile or new difficulty mode is
inferred.

The first-stage Boss entrance initializes HP once at frame 1, starts
its gather 96 frames after `HUD_HP_FILL_FRAMES`, continues for 32
frames and refreshes the visual ring on the true modulo-8 masked
frames. It uses 32 ring points, angular step 3 and screen half-width,
then switches to the original eight-point Boss-width ring at the
same phase boundary. The two later HP thresholds and 1,300-frame
laser-corridor timeout are retained in the already maintained
controller, not duplicated in fresh global state.

These are natural preprocessor constants, preserving the *exact*
Borland source expression types and byte-lvalue operations. The
complete original Sara far-Pascal controller, near attack helpers,
one checked alignment zero, 10-byte compiler switch table and
original ordered relocations were rebuilt by two independent pinned
Borland producers. The existing meaningful red-stack count mutation
from five to four was compiled and rejected. Full focused receipt:
`.analysis/unit-replays/gpt-web-sara-raster-and-burst-b/receipt.json`.
All 1,824 owned CODE bytes were already accepted; this pass adds
real source semantics, not duplicate byte ownership or a whole-game
cold replay.

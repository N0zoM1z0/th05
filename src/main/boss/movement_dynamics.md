# MAIN Boss random-flight and exact-target motion, with real initialized clamp

The original **398-byte** two-function near-Pascal Boss movement owner
is `boss_flystep_random()` followed by `boss_flystep_towards()`.
Their actual 24-byte Boss, two-byte directional sprite selectors,
vertical turn-control state and full `LRTB<Subpixel,Subpixel>` are
reused, not duplicated or reduced to alternate scratch structures.
The new `movement_dynamics.hpp` contains *only compile-time* game rules.

On frame zero, random movement selects its actual initial angle
based on the Boss X coordinate: near the left edge it samples the
signed range [-0x30,+0x30), near the right edge it uses the
original **bitwise-AND random** selection from [+0x30,+0x91), and
elsewhere it draws a full random direction. The non-power-of-two
right-side range is intentionally not changed to a mathematically
unbiased modulo selection; doing so would alter real gameplay and
compiler branch shapes. The existing Y_UP/Y_DOWN direction latch then
reflects the angle across its native 0x80 vertical split when
necessary. The source resets this latch to Y_ANY before movement.

The near `vector2_near()` call gets the original velocity magnitude
`to_sp(4.0f) - frame*2`, i.e. **64 subpixels minus two subpixels per
frame**. The helper advances the true current X/Y subpixel positions
before clamping each dimension to the live four-sided rectangle, then
returns true only at the original **28-frame** boundary. The separate
`boss_flystep_towards()` uses the original signed-distance 1/16
coarse step, then its narrower **X×4** and **Y×8** fine steps, finally
snapping the coordinate exactly when its signed displacement divides
to zero. The true stop condition requires **both dimensions** to
reach their destination and reselects the original idle sprite.

The independently accepted **eight-byte** default rectangle now also
uses the same source-level `BMD_SUBPIXEL_SHIFT = 4` as the movement
translation unit. Its genuine initial boundaries are X [32,352] and
Y [24,128], stored as four little-endian 16-bit Q12.4 values at
`209D:1436`. The EX-Alice original setup dynamically replaces those
with its narrower [64,320]×[48,96] fight arena; this is an update to
the *same* global, not a second initialized object. Both complete
source owners were changed and their two independent pinned Borland
producer runs match every byte, OMF/MAP owner and literal ordered
fixup; their compiled movement fraction 16→8 and top edge 24→25
negative controls were rejected. Scoped receipt:
`.analysis/unit-replays/gpt-web-boss-motion-clamp-closure-a/receipt.json`.

As a cross-source confidence check, the unchanged complete **1,060-byte
EX-Alice** and **959-byte Shinki** far-Pascal Boss controllers were
also independently rebuilt twice with their own meaningful compiled
negatives; both remained byte- and relocation-exact under
`.analysis/unit-replays/gpt-web-boss-motion-large-callers-a/receipt.json`.
The two large controllers earn **no duplicate CODE credit**, nor does
the already accepted clamp gain a second eight-byte ownership claim.
No whole MAIN cold replay or instruction-level optimizer padding was
performed.

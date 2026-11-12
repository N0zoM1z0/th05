# Stage-five midboss: complete five-pattern source and full controller

The original near-C++ movement/pattern owner `[16724,168F2)` is a
**462-byte, five-function** natural C++ contribution. It contains a
68-byte horizontal dash, a 133-byte charge/pattern selector, and three
concrete callbacks: 68-byte blue spread, 105-byte green randomized ring,
and 88-byte mixed aimed stack. The independent original Stage-five
state machine is the complete **318-byte** far-Pascal
`midboss5_update()` immediately following at `[168F2,16A30)`.
Their canonical `Stage5Scratch` and 22-byte `midboss` state are reused
without allocating another record or overwriting unused scratch fields.

The now shared compile-time-only `stage5_attack_rules.hpp` exposes the
true **32-frame** dash/charging boundary, directional two-pixel
horizontal movement, cyclic four-step direction index and original
midboss sprite states. The charge helper displays circles at frame 16
in colors **3 and 2**, updates the sprite at frames **20/24/28**,
sets its existing player-aimed angle and starts each selected callback
only at frame 32. It preserves the original four-frame animation
cadence, physical near function-pointer slot and phase reset behavior.

At each fourth phase frame, the blue callback fires a genuine 13-shot
spread, angular step 7, blue V patnum and speed **5.5 pixels/frame**,
ending at frame 96. The green callback emits a 16-shot ring at speed
**2**, with two independent 64-pixel RNG offsets centered by -32,
ending at frame 96. The aimed callback fires *once* at frame 32:
its first aimed spread stack has five shots/angle step 10, five speed
layers/step .375; the second aimed ring stack uses 32 shots and a
.25-pixel speed step. It finishes at frame 64. All original bullet
RNG calls, tuning and emitted shot order remain in the source.

The complete Boss controller stays invulnerable during its original
192-frame entrance and then transitions to its real two-substate
attack/flystep loop. It updates the original 0/1 subphase and
`patterns_done` byte, selecting the next pattern by
**`patterns_done % 3`** from the independent, genuinely linked
**six-byte** `MIDBOSS5_PATTERNS` DATA object at `209D:1490`.
The remaining lifecycle includes the original 24-pixel midboss hitbox,
score bonus 30, one-up drop, eight-pixel explosion radius, 48 sparks
and explosion sound 12. There are no new callback tables, synthetic
branch contexts or changed game difficulty values.

The actual affected C++ source scopes were replayed together in a
**single bounded native Borland batch**, not by cold-replaying MAIN:
`.analysis/unit-replays/gpt-web-stage5-source-closure-b/receipt.json`.
Two independent producers match all **462 + 318 + 6** original bytes,
the original OMF/MAP CODE and DATA scopes, the complete original
ordered MZ fixup streams and all *three* compiled semantic negatives.
The separately accepted six-byte data object remains counted once;
these source-level improvements do not recredit the 780 previously
accepted CODE bytes. This also resolves a transient duplicate unit
proposal and preserves the original accepted Stage-five unit ID.

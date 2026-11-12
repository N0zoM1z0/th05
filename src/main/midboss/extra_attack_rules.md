# Extra midboss: exact five-function attack family and 22-byte callback DATA

The MAIN Extra midboss comprises an accepted **440-byte five-function**
movement/attack owner at `[163FE,165B6)`, a complete **366-byte**
far-Pascal shared Boss updater at `[165B6,16724)`, and an independently
accepted **22-byte initialized near-DATA** contribution at
`[21E4A,21E60)`. The maintained `extra_attack_rules.hpp` now gives
these *three real source owners* a common compile-time-only vocabulary.
It does not invent an additional midboss state, borrow a native opcode,
copy target pointer words, or change the existing sixteen-byte scratch
union and 22-byte `midboss` layout.

**Actual dash motion:** the callback prepares with sprite 221, then
uses a four-pixel starting velocity reduced by twice the dash frame.
The original `frame *= 2` and the **bitwise OR** of the early/late
swing-animation conditions are preserved; its two sprint sprites are
222 and 223. The first attack starts only after the real 30-frame
dash and ten-frame anticipation, with sound 8 during the dash and
sound 15 at the start of the attack. Its initial wait leaf completes
at the original frame 112.

**Real attack shapes:** the rotating ring randomizes a signed ±1
rotation at frame 94, then emits an accelerating 18-bullet ring with
16-unit angle spacing through frame 114, ending its attack at frame
128. The random variant emits a twelve-shot random-angle/speed group
with ten-unit angle spacing and only when the true display page is
nonzero. The decelerating two-sided attack fires every sixteen frames
with the original `5UL | (8UL<<8) | (4UL<<16) | (16UL<<24)`
32-bit packed spread/stack state. It fires two real attacks at angles
0x80 and 0 with opposite ±0x38 single-use deceleration/turn orders;
it does not combine them into a synthetic helper.

**Complete Boss controller and DATA:** the first, invulnerable entrance
has its own 24-pixel hitbox and sound 10; the active dash has sound 4.
When remaining HP first falls *strictly below 1000*, the original
second attack set activates with a ten-unit bonus and 20-frame minimum
bullet clear, without adding another local phase. The saved
`patterns_done & 7` indexes the genuine eight-angle heading array,
and the active mode uses the original independent `3×2` near-function
callback bank. It grants a 30-unit bonus and a 1UP only on genuine
HP defeat before the twenty-dash timeout, then uses sprite 4, eight-
pixel explosion radius, 48 sparks and sound 12. The initial/current
near callbacks and all eight source-level headings remain true
compiler-generated DATA, not hard-coded target offsets.

After changing all three physically related sources, only their
bounded accepted units were replayed. Two independent pinned native
Borland C++ producers exactly match all **440 + 366 CODE bytes and 22
DATA bytes**, actual OMF/MAP boundaries and original ordered fixups.
All three compiled semantic negatives were rejected, including the
original ring speed 8→9, active HP gate 1000→1001, and replacing the
first row's random callback with its spread callback. Receipt:
`.analysis/unit-replays/gpt-web-extra-midboss-source-closure-b/receipt.json`.
The 22 DATA bytes and all 806 original CODE bytes were previously
accepted; source improvements here earn no second credit, and no
whole-program cold replay was executed.

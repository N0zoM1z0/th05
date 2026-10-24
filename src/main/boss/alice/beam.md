# Alice puppet-beam natural C++ candidate

This single complete algorithm occupies original MAIN
`[1E602,1E764)`:354 instruction bytes,102 instructions and four near-cdecl
returns. It has no compiler table, padding, initialized DATA or BSS.
The actual ordered loader-fixup offsets are `[350,235,219,133]`.
All local direct branches land at reviewed instruction starts.

The function waits until both puppets stop moving, charges their beam,
contracts the gather circles, changes the beam animation state, performs
shot/player collisions and emits periodic aimed bullet stacks. The unsigned
beam timer/window and signed Boss frame modulo operations remain distinct.
Shot collision uses a56-by8-pixel radius around the beam center; player
collision retains the different half-open horizontal/vertical bounds and
16-bit unsigned wraparound. No gameplay correction or cap is added to the
original growing burst window.

The complete26-byte puppet overlay retains both flags, full motion, phase
frame, radius union, pattern, HP, word damage and the genuine final unused
word. Puppets occupy slots0 and1 of the existing canonical26-byte custom
pool. Boss24, BulletTemplate14, Player motion and four-byte points are reused
without changing an accepted definition. Whole coordinate objects have no
padding, so their32-bit storage comparison expresses both coordinate equality
tests directly. The stack assignment combines the two actual adjacent count
and speed fields; it supplies no opaque data or instruction array.

ReC98 `th05_main.asm`, lines11708..11830, supplies candidate semantic evidence
under the old `sub_19CB0` name. The cached calibration routes the same complete
102-instruction shape at19CB0..19E12, relative to the independently anchored
Alice callback. Calibration addresses and donor acceptance do not transfer.
The private packet contains the actual original hashes, branch/return checks,
helpers, globals and source identities.

One important observed interface is the shot-hitbox consumer. It is a real
far entry at`0AE1:8A02`, taking no stack arguments and returning damage in AX;
the original caller stores that result in a word local and tests it. The old
reference also declares it FAR. It remains foreign, with no supplied helper
body. Sound is the real far Pascal entry at`14AB:0232`; regular bullets are
near-cdecl at17204. The two-byte tuning callback is the actual near Pascal
pointer at DS41DE. Near code uses frame1527 and globals use DS209D.

The independent binder contains symbol addresses and outside-function context
only. Its empty foreign CODE segments retain their actual group frames;
DATA/BSS remain word-aligned, no ORG exceeds64KiB, and no stack, instruction,
initialized value or inside-function hole is supplied. Source and options
follow the existing MAIN large-model compiler contract.

Proposed owner: `main-alice-puppet-beam`, wrapper`th05/a_beam.cpp`,
`B4_UPDATE_TEXT/main_03`. The meaningful negative changes the shot collision
horizontal radius from56 to55 pixels in the staged source. Details are in
`.analysis/alice-beam-boundary-review.json`. No compiler has been executed
for this preparation. Two fresh deterministic producers, actual OMF/EXTDEF
checks, complete raw bytes, original ordered fixups and compiled negative
rejection remain required before any exact-source acceptance.


Accepted in `main-alice-puppet-beam-a/receipt.json`: both independent fresh deterministic
producers reproduce all354 raw bytes and all four original ordered fixups.
The compiled beam width56→55 mutation is rejected.
Credit is1 complete function(s) and354 authored instruction bytes;
there is no owned table, padding, DATA or BSS. No previously accepted source
or ABI header was changed to obtain this result.

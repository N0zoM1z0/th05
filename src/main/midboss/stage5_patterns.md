# Stage-five midboss movement and pattern prefix

The original MAIN prefix is **16724..168F2**, **462 bytes / five complete
functions**, immediately preceding the accepted Stage5 callback. Native
instructions cover every byte; there are no compiler tables or padding after
any return. All direct branches stay on verified instruction boundaries.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| movement step / completion | 16724..16768 | 68 |
| gather, animation and selected-pattern update | 16768..167ED | 133 |
| blue 13-way spread | 167ED..16831 | 68 |
| green randomized rings | 16831..1689A | 105 |
| aimed spread/ring stacks | 1689A..168F2 | 88 |

Their 149 instructions end at actual near RETs, and the following byte is the
accepted Stage5 callback's PUSH BP. The original ordered relative loader
fixups are **[444,356,251,106]**, one for each far sound call in the last four
functions. The source slot includes all bytes and all five function boundaries.
No parent callback, external dispatch DATA or helper body is copied into it.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains these functions as
`sub_1F6AD`, `sub_1F6F1`, `sub_1F776`, `sub_1F7BA` and `sub_1F823` in
`th05_main.asm`. The new owner expresses their behavior in natural C++, using
the frozen accepted Stage5 header's full midboss, bullet, gather and near
callback interfaces. That accepted header and all other accepted sources are
unchanged. There are no pseudo-register loops, instruction macros, inline
assembly, emitted bytes, optimization barriers or source/flag variants.

Movement chooses horizontal speed -2 or +2 pixels on its first frame, updates
the two-bit direction state, calls the genuine motion updater and explicitly
returns byte truth when 32 frames are reached. The pattern updater charges for
32 frames, calls the real three-stack gather helper with frame-16 and colors
**3 then 2**, plays SE8 at frame16, animates at20/24/28 and aims toward the
player. Pascal argument order was checked against packed PUSH00030002: the
high word3 is pushed first, then low word2. Later frames animate through
sprite219, call the real selected near pattern and, on completion, reset the
timer, pattern phase and charge sprite.

All three firing patterns use ordinary semantic BulletTemplate fields. The
blue spread emits13 shots with angle delta7, speed5.5 and the true blue V
patnum116 every fourth frame until96. The green ring emits16 green D shots
with speed2 and randomized origins within +/-32 pixels, obtains an independent
random angle, and completes at96. The aimed pattern at32 emits spread stacks
(5 shots/delta10,5 layers/delta0.375), then ring stacks (32 shots/delta0.25),
with speed2, and completes at64. The genuine reference setters combine adjacent
semantic fields into typed16/32-bit writes, as in the accepted Sara owner;
this is neither opaque target data nor a manual compiler instruction body.

The comparison-return patterns produce truth expressions compatible with the
existing byte-bool callback interface; original bodies compute0/1 in AX and
their actual indirect consumer tests AL. Movement explicitly returns AL truth.
The true two-byte callback at DS3788 remains external, as does the three-entry
semantic near-function table at DS1490. No table values or DATA/BSS are emitted
or credited by this owner.

Foreign near calls retain real CS1527: motion1527C, RNG1529C/mod152C0,
gather1705D, player-angle171CC and bullet-add17204. Sound is genuine C Pascal
far14AB:0232, with exact uppercase Pascal publics in the symbol-only binder.
Foreign globals are current callback DS3788, bullet_template577E (14),
midboss5AA4 (22) and boss_statebyteC682 (16). The binder contains only addresses
and outside-contribution holes, with a separate paragraph context at16900
following the full original end168F2; it has no helper code, initialized values,
inside-function padding or `.stack`. Every ORG is below64KiB.

`.analysis/midboss-stage5-patterns-boundary-review.json` records original hashes,
complete per-function calls/branches/returns and ordered fixups.
`.analysis/midboss-stage5-patterns-candidate.json` proposes the valid DOS8.3
module `th05/mb5pat.cpp`, MAIN_036_TEXT/main_03 and one compiled negative
changing blue spread13→12. Native closure/classification and unique-mutation
checks pass. Preparation ran no compiler or Wine. Actual two-cold raw/ordered
verification and negative rejection remain necessary before any exact claim.


Accepted in `main-midboss5-extra-patterns-a/receipt.json`: all462 raw bytes,
original ordered fixups and two independent fresh deterministic producers
agree. This complete owner has5 functions and462 authored instruction
bytes, without table, padding, DATA or BSS credit. Its own meaningful compiled
source mutation is rejected. No accepted update source or ABI was modified.

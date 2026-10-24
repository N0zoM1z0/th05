# Louise remaining patterns

The original MAIN interval **1DAE5..1DD40** contains **603 bytes / four complete
functions**, immediately before the actual Louise update callback at1DD40.
Native decoding covers all603 bytes with206 instructions. Every direct branch
lands on an instruction start inside its own function. Each function ends in
real near RET; there is no compiler table, zero or gap between functions.

| Complete function | Original interval | Bytes |
| --- | --- | ---: |
| alternating four-way mirrored fans | 1DAE5..1DBC3 | 222 |
| sweeping shoot-out lasers | 1DBC3..1DC62 | 159 |
| decelerating turning rings | 1DC62..1DCE8 | 134 |
| alternating aimed pellet spreads | 1DCE8..1DD40 | 88 |

Original ordered relative MZ fixups are **[599,490]**, the actual far sound
calls. None of the four functions is a partial slice, and no padding is added.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` retains these algorithms as
`sub_18DDF`, `sub_18EBD`, `sub_18F5C` and `sub_18FE2` in `th05_main.asm`.
This owner expresses their behavior in ordinary C++, reusing the accepted
Louise header's canonical Boss24, BulletTemplate14, gather and real charging
state interface. The accepted24-byte Laser declaration is included read-only.
The two one-byte special-motion unions include every canonical member from
`bullet/update.hpp`, without pulling in that owner's unrelated entity enums.
All accepted sources and shared headers remain unchanged. There are no inline
ASM statements, pseudo-register loops, emitted opcodes, inert barriers,
opaque arrays or source/flag variants.

The fan pattern runs every32 frames. It configures backwards-cloud single
pellets, invokes the true tuner, then starts at speed3. Alternating64-frame
halves select initial angle24 or64 hex and reflect across40 orC0 hex. Each
of eight iterations saves the real byte angle across foreign bullet calls,
emits four mirrored directions, restores the angle, decreases speed by0.3125
and advances angle8. Ordinary loops and semantic byte fields express these
mirrored shots; no register behavior or instruction order is encoded manually.

The laser pattern consumes the proven foreign charge helper with duration128.
Initialization copies the Boss position into the actual laser template, sets
width6, color8, angle-16, move-out age30 and speed6.5, then selects one of two
sweep directions through the real random-AND helper. Initialization falls
through to firing. Every fourth frame while the wrapped angle is in-16..128,
it launches a real shoot-out laser; one direction mirrors the angle around80
hex and restores it after the spawn. Angle then advances10. Completion resets
mode0, frame0 and sprite180 through the ordinary real state machine.

The turning-ring pattern charges for64 frames, configures aimed ring stacks
with24 shots, delta8, five layers/delta0.5625 and the true decelerate-then-turn
motion. It preserves the original state speed progression, sets one allowed
turn, randomly chooses+20/-20 hex, invokes the actual tuner and SE15, and adds
special bullets. Its finish state resets the same real Boss fields. The last
pattern fires every32 frames: aimed32-shot pellet spreads with delta2, speed2
and exact-linear motion, alternating angular offset+1F/-1F hex every64 frames,
then special-add and SE3. Full semantic packed setters follow the actual
BulletTemplate interface, with no copied payload or DATA contribution.

Foreign near helpers retain CS1527: random AND152AA, regular/special bullet
add17204/17218, shoot-out laser spawn1A66E and proven charge1D938. Capstone's
linear near-call display252AA wraps within the16-bit CS to real152AA; that
display is not a separate helper. Sound is genuine C Pascal far14AB:0232.
The binding context uses the exact foreign LASER_SC_TEXT segment name so its
empty compiler contribution merges at the real main03 prefix. It supplies only
addresses and outside-function holes, ending the real source slot at1DD40 and
then reserving external code to DS209D. No initialized values, helper bodies,
inside-function holes or `.stack` are present; every ORG is below64KiB.

Foreign state is bullet_special DS3F94(1), bullet_template_special_angle3F95(1),
true near Pascal tune callback41DE(2), bullet_template577E(14),
laser_template5A8C(24), boss5ABA(24) and boss_statebyteC682(16). The owner
supplies no DATA or BSS. Original external callback tables remain foreign.

`.analysis/louise-later-patterns-boundary-review.json` pins target/extent hashes,
all function boundaries and full branch/call/return/fixup evidence.
`.analysis/louise-later-patterns-candidate.json` proposes valid DOS8.3 module
`th05/louisel.cpp`, B4_UPDATE_TEXT/main_03, the meaningful fan-angle24→25
negative and four optional complete-function scopes with independent controls.
Native closure, classification and unique-mutation checks pass. Preparation
ran no compiler or Wine; two actual cold producers, full raw/ordered comparison
and compiled-negative rejection remain required before acceptance.


## First retained producer: no acceptance

`main-louise-later-patterns-a` linked one actual597-byte contribution against
the603-byte target. The size gate stopped before a second positive or compiled
negative. The first mirrored-fan function is216 versus222 bytes: both speed
decrements compile as5-byte `SUB byte [speed],5`, whereas the original uses
8-byte `MOV AL,[speed]; ADD AL,-5; MOV [speed],AL`. These two equivalent byte
arithmetic lowerings account for all six missing bytes. No factual semantic,
ABI or type error was found; the canonical reference SubpixelBase subtraction
operator also subtracts the same unsigned-byte quantity. No source expression,
flags, dummy side effects or instruction templates were changed to force the
longer form.

The following complete functions retain their real159/134/88-byte lengths and
ordered relative fixups[]/[109]/[84]. Their actual MAP starts1DBBD/1DC5C/1DCE2
are each six bytes early. Their only raw differences are genuine external near
CALL displacements (four/three/one differing low bytes), so **none currently
passes strict raw comparison**. Far calls, real CS1527, DS209D, state operands
and all aligned semantic instructions agree. A diagnostic alignment that
ignores control displacements is not raw exact evidence and grants no credit.

`.analysis/louise-later-patterns-a-forensic.json` pins the original actual
MZ/MAP/OMF files, per-function real scopes, unchanged fixup order, the two
concrete instruction-lowering differences and the independent negative anchors.
CPP, ABI header and binder remain unchanged. Any future layout experiment
would need real new producer evidence; this review neither shifts retained
bytes nor inserts a gap into a function.


## Accepted typed byte arithmetic

The original fan updates use a loaded byte plus a wrapped negative5 delta.
The initial compound assignment emitted597 rather than603 bytes. A normal
value assignment recovered the intended603-byte extent but retained SUB rather
than the original ADD encoding. Passing a negative float to `louise_speed`
was rejected: that helper converts floating point directly to unsigned byte,
so this argument is outside its valid range and did not yield negative5.

The final source quantizes the positive magnitude through the unchanged helper,
negates that integral value and converts it to the real unsigned byte domain
before addition. This defined modulo256 adjustment equals subtraction5 for
all256 input byte values. It introduces no extra game work, register template,
barrier, fake helper or compiler flag. Only these two ordinary arithmetic
expressions changed; accepted source and ABI headers remain frozen.

`main-louise-later-patterns-d` accepts all603 raw bytes, four complete functions
and both original ordered fixups in two fresh deterministic producers. The
fan-angle24→25 compiled mutation is rejected. Credit is603 instruction bytes,
with no tables, padding, DATA or BSS. Earlier failed receipts remain private.

# Shinki's late-wing attacks and full-controller shared phase protocol

The maintained `wing_attack_rules.hpp` describes three genuine C++ attack
functions after Shinki's six-laser wing preparation: the 182-byte blue
rain/aimed spread function, the 180-byte purple-wing transformation and
the 209-byte aimed B6-ball/symmetric red-spread function. These three
attacks coexist in `shinki.cpp` with the original 959-byte far-Pascal
`shinki_update()` controller. All symbols and actual state remain in
previously accepted Boss, bullet and custom-entity records; no new table,
resource bitmap, state object or helper implementation is introduced.

**Wing rain.** The phase suppresses volleys through frame 128, then
creates down-aimed blue B6 balls at an eight-frame cadence from random
horizontal positions. The vertical position is computed from the
original fractions 2/23 and 6/23 of the playfield height, and ball
speeds remain 3.0..5.0 pixels/frame. Every 24 frames it additionally
fires a five-bullet aimed spread from near the wings. The original
spread-angle deltas per difficulty are 16, 12, 10, and 8 angular units;
its speed remains 3 pixels/frame.

**Purple transformation.** Before phase frame 160 the callback returns
without effects. During 160..191, the boss alternates vertical movement
by ±2 pixels each frame. The original source contains an unreachable
`frame == 128` sound check *inside* that interval; this source retains
that historical condition rather than silently removing it or claiming
that sound actually plays. At frame 192 exactly 16 purple B6 balls are
spawned with angles in [0x20,0x60) and speeds 2..6 pixels/frame, then
the wing sprite, sound 15 and eight-frame screen shake are installed.
The transition returns true at phase frame 200.

**Symmetric red spreads.** The subsequent phase starts after frame 128,
initializes its existing state byte 15 at frame 129 using the actual
rank-specific B6-ball intervals 96/32/28/24, and creates aimed purple
balls at speed four. Independently, every four frames it creates two
symmetric three-bullet red spreads with speed 2.5, linear motion,
angle step two, and a 128-frame triangular angle cycle reflected around
0x80. All writebacks and external near/far calls retain their source
order.

**The real Boss controller.** Both late-wing shared phases still use
the same 3,000-frame timeout and their first-wave index 0. The large
controller keeps a named 3,000-valued *local enumerator*, defined using
the shared constant. This is a genuine Borland ABI/codegen requirement:
removing that member makes the compiler choose an eight-bit underlying
representation for the entire local enum (all remaining values fit a
byte). The original early-phase `patterns_seen & 1` then compiles to an
`AND DL,1` *before* zero-extending DH instead of the original `MOV DH,0`
then `AND DX,1`. This diagnostic emitted exactly five wrong bytes while
preserving size and all four ordered update relocations. Restoring the
natural 16-bit timeout enumerator re-establishes the exact original
code, without a synthetic compiler barrier or altered condition.

Two independent Borland native producers for **all eleven affected
Shinki accepted units** reproduce full original code, OMF/MAP scopes,
all original ordered fixups and the compiled meaningful update negative:
`.analysis/unit-replays/gpt-web-shinki-wing-attack-cohort-c/receipt.json`.
The first failed source variant is retained privately as diagnostic
`gpt-web-shinki-wing-attack-cohort-a`; it is **not** an acceptance.
Original compiler switch tables and checked zeros remain verified, and
no already accepted CODE byte is credited again. No whole-game replay
was performed.

The late symmetric B6-ball attack's rank-selected interval is the named
byte-15 member of the complete shared scratch overlay, not a newly allocated
clock. Its relationship to the wing animation and other byte-14/15 roles is
recorded in [Shinki scratch-byte lifetimes](scratch.md).

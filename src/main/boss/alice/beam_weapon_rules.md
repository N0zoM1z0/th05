# Alice two-puppet beam: physical charge, collision and burst protocol

The source-backed **354-byte** `alice_puppet_beam_pattern()` is a
single complete original MAIN near-C++ function. Its actor readiness
condition compares both four-byte puppet coordinates, so any change in
X or Y postpones the beam clock. The source now names all real
animation/collision settings in the compile-time-only
`beam_weapon_rules.hpp`, shared with the separately accepted **939-byte**
Alice far-Pascal Boss controller. It introduces no new scratch bytes,
callback, table, font asset or generated machine instructions.

The beam's own clock begins its charging circles at frame **16** with
radius 64 and sprite offset -60. At that event the original burst-window
counter increases by **32**. Frames 32..63 contract both circles at
`(64 - beam_frame) * 2` pixels. Frame 64 enters beam sprites (sound
8), with sprite updates at **71** and **79**, and actual firing from
frame **80**. The entire Boss first installs the existing **160-frame**
burst window when the puppets appear, and transitions away from the
beam after its authentic **600-frame Boss phase**; the 5-unit hit bonus
and existing puppet-phase reset are unaltered. Naming both sides of
this protocol makes the real division of responsibility explicit.

During firing, the original beam shot template is a forward/no-decel
single shot with speed **24 subpixels**. The large beam uses the
separately initialized **56×8-pixel shot collision radii**, centered
64 pixels right of puppet 0, with sound 9 on collision. The player-hit
rectangle is different: its horizontal width is **128 pixels**, its
vertical height **8 pixels** with a 4-pixel lead. Both unsigned 16-bit
comparisons retain the original inclusive-left/exclusive-right and
wraparound behavior. The bullet-stack subpattern fires every **16**
Boss frames while `boss.phase_frame % 256` lies within the actual
mutable burst window; the stack still carries the packed source-level
**8 bullet / speed-step 6** fields and its true -8-pixel Y offset.

The ABI/provenance-sensitive far shot-hit helper and its AX return,
original `reinterpret_cast<uint16_t&>` packed template assignment,
and physical byte/state offsets are untouched. This is not a source
claim about the original historical TU grouping. The native bounded
replay at
`.analysis/unit-replays/gpt-web-alice-beam-weapon-contract-a/receipt.json`
recompiles exactly the two affected accepted scopes under two pinned
Borland producers, verifying all **354 + 939 original bytes**, the
whole controller's real 30-byte compiler switch table, its one
checked uncredited alignment zero and all original ordered MZ fixups.
The compiled collision-radius mutation **56→55** is rejected. No
already accepted CODE is counted twice and no full cold replay runs.

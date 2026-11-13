# Later EX-Alice patterns

Three complete callbacks cover original MAIN `199D5..19C2D`, directly after
the accepted first cohort. This600-byte contribution contains199 instructions,
no padding, compiler tables or owned DATA/BSS.

| Function | Original extent | Bytes | Ordered fixups |
|---|---|---:|---|
| `exalice_pattern_firewave_fans` | `199D5..19B13` | 318 | `[291]` |
| `exalice_pattern_gravity_stacks` | `19B13..19BC2` | 175 | `[90]` |
| `exalice_pattern_diamond_rings` | `19BC2..19C2D` | 107 | `[88]` |

The first emits mirrored oscillating aimed fans, periodically chooses a
persisted aimed origin, overlays single cloud bullets, creates alternating
firewaves and moves the boss. The second combines random upward gravity
bullets with aimed stacks from random offsets. The third alternates rotating
22-way diamond rings. Signed frame modulo, quantized speeds, actual sprite
IDs and the state-byte angle arithmetic retain their original semantics.
All speeds converted from floating constants are positive.

The frozen `patterns.hpp` supplies the canonical full Boss24, BulletTemplate14,
one-byte BulletSpecialState union and near callback interfaces. It remains
unchanged. The broad bullet-update header is not included: its HUD surface
has a conflicting `to_sp` definition. The player header supplies the actual
near Pascal angle interface with two real Subpixel values and a byte angle.
The firewave producer takes a signed16-bit pixel amplitude and a byte bool
using Pascal cleanup. All near helpers share frame1527; sound is far Pascal
14AB:0232. The persistent shot origin is a real four-byte point at DS4A8A;
pellet color is the real separate word at DSC33E, corroborated by
`th05/main/bullet/pellet_r[bss].asm`.

The independent binder supplies only foreign labels and outside-contribution
holes. Its real paragraph tail starts at19C30 and ends at209D0. There are no
instructions, initialized values, stack or holes inside the600-byte owner.
The complete original ordered relocation stream is `[581,408,291]`, with no
sorting or normalization.

ReC98 `th05_main.asm` lines17801..18045 supplies the semantic reference.
The local original-minus-calibration displacement is `-503F`; all three
complete instruction shapes agree. Original complete returns, local branches
and ordered fixups were reviewed directly against the pinned MAIN image.
Neither routing equality nor source presence establishes source exactness.

Private integration metadata is `.analysis/exalice-later-boundary-review.json`,
with the whole-unit proposal and optional complete-function scopes. The
unique staged negative reduces the real mirrored-fan speed5 to4 and belongs
to the first callback. No compiler was executed during initial preparation; the focused results
below establish acceptance.

`main-exalice-later-patterns-a` passes two fresh deterministic complete
600-byte raw comparisons and the original ordered fixups[581,408,291].
The actual first-fan speed5→4 control is compiled and rejected for the whole
owner. All three complete functions and600 instruction bytes are accepted;
no DATA, BSS, tables or padding receive credit.

## 2026-11-13: shared firewave/spiral scratch-byte lifecycle

The later firewave and spiral/gather attacks use the same physical Boss bytes
13 and 14, but with different byte-14 roles. The typed
`ExAliceLaterPatternState` view makes that lifetime explicit: byte 13 is the
`turn_phase` selector in both attacks; byte 14 is `firewave.angle` in the
firewave callback and `spiral.acceleration_step` in the spiral callback. Each
pattern initializes its own pair at its original entry frame, so neither
pattern inherits the previous attack's value. Byte 15 remains the separate
`ExAlicePatternByte15` overlay for each pattern's independent angle offset.

Compile-time size and absolute-offset assertions pin the later-pattern view
inside the original 16-byte `boss_statebyte` object: byte 13 remains offset 13
and both byte-14 views remain offset 14. The raw `boss_statebyte[13]` and
`[14]` accesses are removed from both source bodies; byte 11 and byte 12 are
retained without invented semantics. The 600-byte later-pattern cohort and
all other seven accepted consumers of the shared header were replayed in two
independent Borland/TLINK producers; their original bytes and ordered fixups
remain exact and the compiled negative is rejected. The 334-byte spiral
owner was separately replayed through its TCC-S/TASM32 pipeline, retaining
its original ordered fixups and rejecting its compiled radius negative. The
complete 1,060-byte EX-Alice controller was included in the header-closure
replay and remains exact. No duplicate CODE credit is added.

Receipts:
`.analysis/unit-replays/gpt-web-exalice-typed-later-pattern-state-20261113/receipt.json`
and
`.analysis/unit-replays/gpt-web-exalice-typed-later-pattern-state-spiral-20261113/receipt.json`.

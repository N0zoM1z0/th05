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

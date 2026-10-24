# EX-Alice bouncing and laser patterns

Four complete callbacks cover original MAIN `19C2D..19EB2`:645 instruction
bytes and209 instructions, with no padding, compiler tables or owned DATA/BSS.

| Function | Original extent | Bytes | Ordered fixups |
|---|---|---:|---|
| `exalice_pattern_bouncing_rings` | `19C2D..19C95` | 104 | `[98]` |
| `exalice_pattern_fixed_laser_fan` | `19C95..19D82` | 237 | none |
| `exalice_pattern_speedup_fans` | `19D82..19DF0` | 110 | `[81]` |
| `exalice_pattern_sweeping_lasers` | `19DF0..19EB2` | 194 | none |

The callbacks emit increasingly dense bouncing rings, alternating aimed fixed
lasers with a green ring, accelerating aimed fans while moving, and sweeping
shootout lasers with later green rings. Signed boss-frame modulo and all
unsigned byte angle wrap remain explicit. The fixed-laser pattern acts on the
first16 slots of the full canonical32-slot array, without shortening storage.
Its real cyclic slot counter at DS1998 remains a signed16-bit object.

The frozen `patterns.hpp` and `laser.hpp` provide canonical Boss24,
BulletTemplate14, BulletSpecialState1 and Laser24 types. All laser fields,
the complete flag enum, byte width union, grow/shrink ages and shootout speed
retain their actual roles. The target checks LF_FIXED_WAIT_TO_GROW=2 and
uses a24-byte stride. The negative aiming offset is an explicit integral
byte conversion of minus48; floating speed constants are positive.
No accepted header or previous source owner is edited.

All code calls except sound are near in frame1527. Fixed spawn is Pascal
at1A6EF; shootout creation is cdecl at1A66E. Player aiming takes the actual
two Subpixel values and byte angle. Sound is far Pascal14AB:0232. DS is209D.
The symbol-only binder starts the foreign LASER_SC_TEXT tail immediately
after the645-byte contribution at19EB2, anchors its real helpers, and ends
at209D0. All holes are outside compiled functions. It supplies no instructions,
initialized data, stack, alignment bytes or inside-function holes.

The original complete relocation stream is `[422,98]`, retained in order.
ReC98 `th05_main.asm` lines18052..18319 supplies semantic evidence. The local
original-minus-calibration displacement remains `-503F`, and all four complete
instruction shapes agree. All original returns, local branch destinations
and ordered fixups were checked natively. This native review alone does not establish source exactness.

Private `.analysis/exalice-laser-patterns-boundary-review.json` contains the
whole-unit proposal and optional complete-function scopes. The unique staged
negative changes the real fixed-laser grow age47 to48 and belongs to the
second callback. No compiler was executed during initial preparation; focused acceptance
results follow.

`main-exalice-laser-patterns-a` passes two fresh deterministic full645-byte
raw comparisons and the original ordered fixups[422,98]. The actual second
function's fixed-laser grow age47→48 mutation is compiled and rejected.
All four complete functions and645 instruction bytes are accepted, with no
compiler tables, padding, initialized DATA or BSS credit.

# Staff orb and opening camera helpers

This accepted owner recovers four contiguous complete MAINE procedures, independently
of the preceding, parked particle updater. `maine-staff-orb-opening-a` passes both fresh deterministic producers,
all483 raw bytes, original ordered fixups and the compiled spark-speed control.
The reference is `ReC98/th05_maine.asm` lines 4077–4335; reference names and
semantics were checked against the pinned decoded original, rather than treated
as an exact producer.

| Procedure | Original load interval | Size |
| --- | --- | ---: |
| `staff_orb_spark_add()` | `D853..D8B6` | 99 |
| `staff_orb_trail_update()` | `D8B6..D8F5` | 63 |
| `staff_orb_particles_age()` | `D8F5..D931` | 60 |
| `staff_orb_opening_update()` | `D931..DA36` | 261 |

All four functions return near in frame `0A54`. The original 483-byte extent
contains no instruction NOPs, padding, switch tables or initialized DATA. Its
original ordered MZ fixup offsets are **[62, 27]**, both within spark creation;
this order is preserved. The opening procedure returns a full `int` in AX,
including zero before the window transition and one from frame 512 onward.

The complete canonical `orb_particle_t` is 20 bytes, with signed 32-bit center
components, signed 16-bit velocity/speed/gather state and byte angle/radius.
Its real array has 64 particles followed by the large orb. The existing
`lifecycle.hpp` supplies these declarations and the separate trail array;
this source supplies no replacement storage or shortened ABI. Signed narrowing
of the orb center feeds the real five-word Pascal `vector2_at` interface,
which writes a near `SPPoint` output rather than returning an aggregate.

The trail procedure shifts seven actual point entries backward and then stores
the orb's low-word center. Particle aging uses signed remainder by eight and
stops at pattern five. Orb growth and part of camera acceleration intentionally
reuse the canonical `staff_back_page` byte, which alternates between zero and
one in the real rendering loop; no second alias or fictitious growth global is
introduced. The camera then accelerates, oscillates around 11 pixels/frame,
changes the clipping window and finally scrolls the orb left.

The new state names identify real DS `1011` objects: spark cursor `173C`,
opening frame `173E` and acceleration phase `1740`. Existing state and arrays
retain their canonical names and addresses. Far helpers are `IRAND` at
`0000:1DF8` and `VECTOR2_AT` at `0E80:04A0`; `space_window_set` is the accepted
near Pascal provider at load `D31F`. The binder contains only external symbol
labels and holes outside the complete compiled contribution. The preceding
`D5E1..D853` updater remains unaccepted, and no bytes from its hole receive
credit. Empty foreign source segments retain their actual group context.

The compiled whole-owner negative changes the real spark speed from three to
four pixels/frame. It belongs to the first function and tests the shared
four-function oracle; no separately compiled mutation is claimed for the other
three functions. Native review and a replayable bounded inspection script are
private under `.analysis/maine-staff-orb-opening/`. The complete compiler contribution, raw bytes, actual inputs/tools and the
original ordered fixup stream are verified for both actual fresh producers.

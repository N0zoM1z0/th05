# Staff particle and star lifecycle candidate

`maine-staff-lifecycle-prefix-b` accepts the complete602-byte prefix through
two fresh producers, all original bytes and ordered fixups, and its rejected
speed10→11 control. It adds four functions. The626-byte original updater is
still unaccepted; both full1228-byte attempts retain their failed verdicts.

The original natural staff family has five consecutive MAINE state functions
at `D387..D853`, frame `0A54`, group offset `2E47`. The current accepted owner
contains the first four complete functions, `D387..D5E1`, 602 bytes. The updater
is retained separately in unaccepted `lifecycle_update.cpp`.

| Function | Complete load extent | Bytes |
| --- | --- | ---: |
| `staff_particles_init` | D387..D49D | 278 |
| `staff_particles_gather` | D49D..D509 | 108 |
| `staff_particles_clear` | D509..D531 | 40 |
| `staff_particles_scatter` | D531..D5E1 | 176 |
| `staff_particles_update` | D5E1..D853 | 626 |

All 1228 bytes decode as instructions, without NOPs, switch tables or padding.
Every direct branch lands on an instruction boundary in its complete function.
The original ordered MZ relocation stream has 17 entries. No compiler,
assembler or linker has run for this candidate, so its sizes and record phase
remain unproved by a maintained-source producer.

The initialization creates 64 drifting particles, clears eight orb-trail
centers, and distributes 48 stars in the real window. The array's 65th particle
is the large orb. Gathering points the particles toward the origin; clearing
marks them absent and enables decay. Scattering retains the original initial
polar calculations before their genuine random replacements, then places the
particles around the orb. Updating applies camera movement, wrapping,
speed-dependent cel changes, alternating star parallax, orb gravity and trail
sampling. No register, FLAGS or instruction-template API implements these loops.

The sentinel is the original signed subpixel value `-999 * 16`, not an integer
minimum. Particle centers are full signed 32-bit subpixel coordinates. Velocity
and trail/star coordinates are signed words. The complete 20-byte
`orb_particle_t` definition is identical to the accepted local staff state TU:
wide center at0, velocity8, pattern12, speed14, gather frame16, angle18 and the
actual radius/direction union19. This owner declares existing arrays externally;
it defines no initialized DATA, BSS or asset contents. The accepted
`staff.cpp` and `staff.hpp` are unchanged.

## Real interfaces and storage

All five procedures are ordinary no-argument near C++ functions with RET.
`space_window_set(int,int,int,int)` is the existing near Pascal provider at
`0A54:2DDF`. Its actual accepted OMF public is
`@SPACE_WINDOW_SET$QIIII`. It must remain in the preceding `SCORE_TEXT` context.

`vector2_at(SPPoint near&,int,int,int,int)` is the real far Pascal provider at
`0E80:04A0`, with a two-byte near output reference and RETF10. It is not an
AX/DX point-return function. `IRAND`, `IATAN2` and `IHYPOT` retain their real
C far Pascal signatures and signed word values at `0000:1DF8`, `0000:1A8C`
and `0000:1AF8`. The actual MASTER header corroborates these declarations.

The two foreign trail routines are complete ordinary near procedures at
`D853..D8B6` and `D8B6..D8F5`. Their real bodies return with RET, read no stack
arguments and preserve the ordinary callee-saved state. They respectively emit
one orb spark and shift the eight trail samples. Neither supplies a CF result.
They remain symbol bindings with no imported body or new credit.

Actual DS is `1011`. The shared source declarations bind the real window
width/height at `50CE/50D0`, scratch point `50D2`, camera velocity `50DA`,
decay word `50DE`, frame word `50E2`, and back-page byte `173A`. Existing
particle/trail/star arrays begin at `50E4/55F8/5618`. The binder reserves their
complete foreign staff extent through `C4D8` without duplicating values or
adding a stack. Every origin hole lies outside the five compiled functions.

## Producer scope and evidence

The first four real state functions supply 602 bytes before the update.
This is the beginning of the actual staff state contribution in the retained
calibration, not an arbitrary prefix chosen for parity. The isolated update's
target relocation order is `[278,421]`; a standalone one-record C++ producer
could disagree. The complete natural five-function owner preserves the genuine
source context, but the new compiler's actual LEDATA/FIXUPP order still must be
checked without sorting or normalization.

`lifecycle.proposal.toml` suggests a whole-contribution unit with DOS8.3 module
`th05/stflife.cpp`, `STAFF_LIFE_TEXT/group_01` and the independent symbol-only
binder. Its shared negative changes the initialized particle speed from10 to11
subpixel units. It modifies the staged CPP source, not a type, ABI or target
byte. No configuration or acceptance ledger is edited by this preparation.

Pinned ReC98 `th05_maine.asm` lines3499..4070 and the original native bytes
provide behavioral evidence; they are not recovered historical C++ text.
The canonical particle state comes from maintained `src/maine/staff/staff.cpp`
and the pinned `th05/staff.cpp` declarations. Private
`.analysis/maine-staff-lifecycle-boundary-review.json` records complete native
bounds, branches, calls, original fixups and foreign ABI observations.
`.analysis/maine-staff-lifecycle-freeze.json` pins both the new inputs and the
unchanged accepted staff files. Two fresh exact producers, source/tool identity
and the compiled negative remain required before any acceptance.

## First retained producer and bounded class-API recovery

`maine-staff-lifecycle-a` stops at its first-positive size gate: 1225 bytes
instead of1228, before a second producer or negative. Its first four complete
functions reproduce all602 bytes and original ordered fixups. Update is623
instead of626. Native comparison identifies one missing three-byte reload of
the trail pointer after the sentinel test, plus different stack slots for the
counter and trail pointer. No field width, signedness or foreign ABI error was
found. Shared frame `0E80` and DS `1011` are correct; the foreign trail labels'
three-byte displacement follows the shorter contribution.

The next candidate changes only `trail_center->x.v != STAFF_CENTER_NONE` to
`trail_center->x != STAFF_CENTER_NONE`. This uses the existing canonical
`SubpixelBase` conversion rather than bypassing the actual class with direct
member access. It adds no helper, side effect, volatile access, barrier, local
reordering or flag option. The source's inverse one-expression change restores
the first producer's CPP bytes exactly. Header, binder and all other functional
inputs stay frozen. Whether the genuine conversion reproduces the original
lowering remains for the next actual producer; no exactness is asserted.

The first source and its freeze manifest are archived under
`.analysis/failed-staff-lifecycle-a-source/`; native mismatch evidence is
`.analysis/maine-staff-lifecycle-a-forensic.json`, and the exact source delta
is pinned by `.analysis/maine-staff-lifecycle-b-source-proof.json`.

The single class-API recovery in `maine-staff-lifecycle-b` still emits1225
bytes. It does not recover the updater's original626-byte extent, and no
further updater source/flag variants are proposed. Both failed whole-family
producers remain intact and unaccepted.

The current prefix factor moves the updater body verbatim into
`lifecycle_update.cpp`; the first four algorithm bodies are unchanged. The
header remains identical. The binder now reserves the whole original626-byte
updater as a foreign hole after the602-byte contribution, before the real
trail providers at `D853/D8B6`. There is no hole inside an owned function. The
accepted ID is `maine-staff-lifecycle-prefix`, with four functions and the
same meaningful initialized-speed negative. Its own fresh positive pair and
compiled negative remain required. This is a new complete cohort, not a
successful relabelling of either failed1228-byte request. Both source variants,
the original proposal and old binder are archived in
`.analysis/failed-staff-lifecycle-full/`; the inverse source-factor proof is
`.analysis/maine-staff-prefix-factor-proof.json`.

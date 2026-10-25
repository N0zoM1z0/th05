# Staff rain transition

This accepted natural C++ source covers two complete contiguous MAINE procedures:
`staff_rain_spawn()` at `DA36..DAD7` (161 bytes) and
`staff_rain_update()` at `DAD7..DBE6` (271 bytes). Both are near in frame `0A54`.
The second returns a full `int` in AX. `maine-staff-rain-scopes-b` accepts both
complete functions from two actual deterministic producers, with zero further
compiler invocations. Each function's literal original relocation order matches.

The candidate reference is `ReC98/th05_maine.asm` lines 4342–4542. Native review
against the pinned decoded original checks complete instruction coverage,
function-final RETs, internal branch destinations and actual helper operands.
The 432-byte extent contains no NOP instructions, padding, switch tables or
initialized DATA. Original ordered MZ fixups are **[156, 80, 66, 49, 32, 424,
350]**, or [156, 80, 66, 49, 32] and [263, 189] within the respective functions.
They remain in their original collection order.

Spawn selects the current 20-byte particle, advances the real signed cursor
at DS `1742`, and initializes it only while the advanced cursor is below 64.
That original last-index behavior is preserved. Speed and pattern use signed
random remainders; angle is a byte. The complete canonical particle type and
65-element storage declaration come from the unchanged `lifecycle.hpp`.
Its signed 32-bit centers are assigned from the real signed 16-bit window
arithmetic. `vector2_at` writes the real near velocity output with five Pascal
word arguments; it has no invented aggregate-return interface.

The update first damps horizontal camera motion using the existing alternating
`staff_back_page`. Its signed frame at DS `1744` controls vertical deceleration,
then moves the window right and releases the rain. Every eighth frame it spawns
and updates all 64 particle directions, bouncing unsigned byte angles between
`20h` and `60h`. The long-running counter wraps back by eight before signed
word overflow. Completion is reported only when the window's right edge reaches
630; earlier frames may increase the background blue component every fourth
frame. The blue component is an unsigned byte, not a word or a detached alias.

The palette interface repeats the complete canonical RGB/Palette template
definitions used by the accepted Boss owners and `ReC98/pc98.h`: three-byte RGB8
colors, 16-color Palette8, 48 bytes total. It references the real C-linkage
`Palettes` object at DS `1D9A`, whose first blue component is at `1D9C`.
`PALETTE_SHOW` is a real far Pascal helper at `0000:1B8A`. The other helpers
are `IRAND` at `0000:1DF8`, `VECTOR2_AT` at `0E80:04A0`, and the accepted
near Pascal window setter at load `D31F`. No palette storage or fake provider
is defined by this owner.

The symbol-only scaffold places each empty foreign CODE segment in its actual
group context. All origin holes are outside the complete compiled contribution.
It does not incorporate or claim the parked updater at `D5E1..D853`, or transfer
credit from the accepted opening helpers at `D853..DA36`. The following
text-wipe procedure at `DBE6` is excluded entirely.

The compiled shared oracle control changes the real spawn speed bias from eight
to nine subpixels. Its owner is the first function; no separately compiled
negative is claimed for the update function. Bounded native review, original
hashes, full branch/call evidence and the unit/control proposal are private under
`.analysis/maine-staff-rain/`.

Attempt a stopped after the first producer's size gate:431 rather than432.
Its only spawn difference was a memory comparison instead of consuming the
incremented cursor value. Combining the increment with its natural condition,
`if(++staff_rain_cursor < ORB_PARTICLE_COUNT)`, restores the complete161-byte
function; the old cursor still selects the particle before incrementing.

Attempt b has two fresh whole432-byte raw-exact producers and a rejected
speed-bias8-to-9 compiled mutation, but its aggregate relocation order fails:
original `[156,80,66,49,32,424,350]` versus actual
`[424,350,156,80,66,49,32]`. That failed aggregate receipt remains unchanged
and is never imported as a whole. Existing `review_saved_scopes.py` revalidates
the intact MZ/MAP/OMF evidence and projects the two complete functions. Within
those complete boundaries, both original ordered streams match exactly; no
sorting, masking, OMF rewriting or new producer is involved. The negative
belongs to spawn and is one shared CODE control, not two independent controls.

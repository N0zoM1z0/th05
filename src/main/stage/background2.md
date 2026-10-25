# Stage-two particle background candidate

This natural C++ owner covers the adjacent particle reinitialization helper
at load offsets `[11700,118EC)` (492 bytes) and the complete stage-two update
at `[118EC,11B79)` (653 bytes). Both use `main_01`, frame `0AE1`; DS is `209D`.
The source is an uncompiled candidate and has no accepted exact credit yet.

The initialization chooses one of eight regions of the repeating 4096-frame
spawn path, assigns an angle and fixed-point X position, adds the real signed
`IRand() % 8` jitter, resets the zoom and Y coordinate, and obtains velocity
from the real far Pascal `vector2` API. The update handles the entrance palette
and tile transition, restores scrolling, spawns the 64 particles, advances their
real motion, reinitializes escaped particles, draws their zoom cels, and pulses
palette color zero.

`s2particle_t` is the complete 26-byte type from
`th05/main/stage/s2part.hpp`: flag, byte angle, full 12-byte `PlayfieldMotion`,
word zoom, and the five original unused words. It overlays the existing complete
64-slot `custom_entities` pool; it does not replace the unrelated 16-byte boss
particle type. The owner uses the canonical full Boss, geometry, RGB/Palette and
custom-entity layouts. It creates no initialized DATA, BSS or asset arrays.

The tile ring retains all 25 rows and 32 columns. Values stored in it are VRAM
source offsets, derived from the real 640-pixel row width and tile-source area;
they are not copied image data. Palette component stores operate on the full
48-byte palette object. State is bound to the actual DS offsets documented in
the private review, including the separate byte at `4A84` that selects whether
the pulse level is rising or falling.

The existing renderer wrapper is a genuine PC-98 hardware interface: AX is the
VRAM Y coordinate, CX is X, ES is the blue VRAM plane `A800`, and the pattern
number is a Pascal stack argument. These hardware assignments do not force
ordinary C++ register allocation. GRCG mode/color and `outportb(0x7C, 0)` use
the existing real graphics interfaces. Motion uses the actual near-this Pascal
method returning the complete four-byte point in DX:AX. `vector2` has two far
references, a byte angle in its physical word stack slot, and a signed word
length; the stack cleanup is 12 bytes.

Native review found 186 and 214 instructions, respectively, with every direct
branch targeting an instruction within its complete function. Both ranges end
at their actual RET/RET2 and contain no switch tables or padding. The complete
original relocation collection order is `[933,918,717,484,441]`; the per-function
orders are `[484,441]` and `[441,426,225]`. Neither order may be normalized.
Calibration provides routing only: its extra midboss renderer after the update
is absent at this point of the original MAIN. The next actual original function
begins at `11B79`, immediately after the update's return.

The independent symbol-only binder reserves the whole 1,145-byte contribution
and places only foreign labels and gaps outside it. A private proposal registers
the complete pair, with the meaningful source mutation `particle.zoom = 8;` to
`9;`. If complete-function scopes are needed, the second function has a separate
pulse-cap mutation from `0x3F` to `0x3E`; actual demangled MAP names must be used.

Private evidence and the native review command are
`.analysis/stage2-background-boundary-review.json`,
`.analysis/stage2-background-unit-proposal.json`, and
`python3 .analysis/stage2-background-review.py`. Acceptance still requires the
root's focused two fresh producers, full raw and original ordered-fixup checks,
actual OMF/MAP/dependency verification, and rejected natural negative control.

The first linked producer (`main-stage2-background-b`) emitted 1,162 bytes:
498 for initialization and 664 for update. Native comparison isolated the
initializer's six extra bytes to a named X temporary spilled and reloaded at
the common destination store. Its four `frame *= 8` expressions also emitted
same-size signed multiplication instead of the original shift. The corrected
candidate directly assigns the real particle X destination in each branch and
uses `frame <<= 3` for the nonnegative path offset. It changes no ABI or flags.
The update's extra eleven bytes come from storing its named returned point
before the four bounds comparisons; this remains an honest typed candidate,
with no register workaround. The current private proposal requests only the
complete 492-byte initializer, bounded by the actual MAP public
`stage2_update()`. The full update is parked and receives no exact credit.
The binder's outside tail accounts for the real unchanged 664-byte update;
with the corrected 492-byte initializer, the expected compiler extent is
1,156 bytes. This actual CODE size must be checked before linking; the original
1,145-byte target extent must not be used to move the foreign SHARED/DS frames.

The focused initializer replay (`main-stage2-particle-init-a`) then emitted
476 bytes instead of the complete original 492. Its boundary gate correctly
stopped before a second producer or negative control. Direct field assignment
allowed additional compiler optimization, so the dataflow correction did not
recover the original body. Both functions remain unaccepted, with no claim that
either failed candidate's outside-layout expectation matches its emitted size.
The source and saved producers are retained for evidence; no further speculative
context or optimizer probes are proposed.

The independently built complete update653 and initializer492 are now
accepted by `main-stage2-update-abi-a` and `main-stage2-particle-initializer-a`.
The actual init476 comparison proved that the entire16-byte difference was
four in-place shifts; ordinary rvalue multiplication assignments restore the
original dataflow. No named-X spill, branch padding, physical register alias
or shared-header change was needed. The combined source includes the same
canonical bodies. Its legacy outside-only binder now reflects492+653 and the
canonical scrolling C symbol, but no new whole-combined replay is claimed.

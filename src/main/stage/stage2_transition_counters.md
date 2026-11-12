# MAIN Stage 2 transition: particle count and color-ramp state

The complete decoded MAIN `[22364,22368)` original initialized-DATA
interval is now a natural four-byte C contribution with three genuine
near state objects: `stage2_particles_spawned` (two-byte signed int at
DGROUP `209D:1994`), `stage2_palette_level` (one unsigned byte at
`1996`) and `stage2_tone_offset` (one unsigned byte at `1997`). Their
exact positions and types are independently confirmed by the original
Stage 2 compiler/linker public symbols in the accepted
`stage2_update_bindings.asm`; the complete 653-byte `stage2_update()`
uses the same three variables.

The original Stage 2 transition first runs its scrolling/wipe effect,
then zeros the three sources when activating the particle backdrop.
`stage2_particles_spawned` counts actual 26-byte Stage 2 particles up
to the physical `S2PARTICLE_COUNT` cap of 64, spawning on the original
even-frame cadence. `stage2_palette_level` ramps the live palette
between 0x20 and 0x3f under the direction latch stored elsewhere;
`stage2_tone_offset` controls the separate 100-based palette tone
before decaying back to zero. These are mutable gameplay state, not
an opaque zero buffer, static text, or authored sprite pixels.

The native C source exports all three independently addressable real
publics with asserted word/byte widths; the compiler creates the
original four zero bytes. The source-free binder contributes only
existing MAIN CODE frame declarations and the outside DATA prefix,
never contents or original game code. The preceding original zero
`[22363,22364)` is an uncredited alignment byte. The next unclassified
zero state `[22368,2236C)` is also **not** absorbed into this
contribution.

The focused pinned native receipt
`.analysis/unit-replays/gpt-web-stage2-transition-counters-a/receipt.json`
proves two independent Borland C producers, complete raw and OMF/MAP
four-byte DATA equality, the empty original ordered MZ fixups and a
rejected compiled mutation of the tone-offset initial value from zero
to one. This adds four new authored initialized-DATA bytes without
claiming new CODE or rerunning the whole executable. The complete
Stage 2 C++ consumer is subsequently validated separately.

## Exact Stage 2 native C/C++ state and movement consumer closure (2026-11-12)

The original 653-byte `stage2_update()` now imports the genuine
C-linkage previous-DATA publics using the source-level
`stage2_transition_counters.h` **before** its existing canonical
`background2.hpp`. The three original direct `extern` references in that
older header are redeclarations of the same symbols and their real
one-word/two-byte types. This does not introduce runtime aliases,
foreign initialization code, or changed DOS register semantics.

Its `stage2_transition_rules.hpp` names the original pre-scroll fade at
stage frame 256, tile/source wipe at 304, and resumed scrolling at
306. The authentic 303-frame remaining fade, 25-row tile writeback,
24-column clear, 100-based tone, and exact palette-pulse range
0x20..0x3f remain unchanged. During active Stage 2, one of the real
64 particles spawns every other frame until the source-owned 16-bit
count reaches the genuine cap. The 1-byte pulse brightness and
1-byte tone offset are still *different* mutable C publics; the
palette direction latch remains foreign and is not miscredited.

The same animation contract also names the actual eight cyclic
particle tracks and their milestone frames 1000, 1128, 2000, 2128,
3000, 3128, and 3968, on a 4096-frame phase clock. The complete
492-byte independently accepted particle initializer preserves its
original native random-angle and exact Q12.4 integer calculations.
The separate 51-byte invalidate leaf uses its real 8-by-8
background footprint and the original near-Pascal redraw interface.

The whole affected CODE cohort was recompiled twice with the pinned
Borland native toolchain, including all **653+492+51** original CODE
bytes, exact OMF/MAP and original ordered MZ fixups. Each of the three
compiled meaningful controls was rejected (palette ceiling 0x3f→0x3e,
initial particle zoom 8→9, and invalidate footprint 8→9). The four-byte
C DATA object was recompiled independently with its zero→one tone
mutation rejected. Receipts:

- `.analysis/unit-replays/gpt-web-stage2-bg-three-code-scopes-a/receipt.json`
- `.analysis/unit-replays/gpt-web-stage2-transition-c-public-a/receipt.json`

The compiler/ABI source is also used by the original Stage 2 combined
context; no source identity or new code ownership is falsely claimed for
its separately unaccepted body. Reviewed ASM inputs are untouched.
No cold replay of MAIN or unrelated artifacts was performed.

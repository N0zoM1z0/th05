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

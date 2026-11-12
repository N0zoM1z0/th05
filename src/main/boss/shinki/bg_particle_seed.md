# Shinki background: genuine initialized 16-bit particle-count sentinel

The decoded original MAIN interval `[2235A,2235C)` contains the full
native 16-bit initialized object `_shinki_bg_type_a_particles_alive`.
The original assembly `th05_main.asm` declares its value as
`dw (-1 and 255)`, an **unsigned-positive 255** count sentinel; the
accepted background's actual `shinki_bg_type_a_update_part1()` compares
the signed two-byte C++ count with `PARTICLES_UNINITIALIZED` (also
`-1 & 0xFF`). When it matches, the code initializes the two line sets,
clears the real particle pool and writes the live counter to zero
before gradually spawning up to `BOSS_PARTICLE_COUNT` particles.
This is a state protocol, not a sprite bitmap or arbitrary zero area.

The source exports its real C public as a writable near `int`, whose
16-bit width is asserted. The initial value is expressed by the actual
`(-1 & 0xff)` compiler expression rather than a copied word from the
target. The outside-only native binder preserves the code group frames
and DGROUP address `209D:198A`, supplying neither candidate bytes nor
any surrounding state. In particular, both zero-initialized
`shinki_bg_linesets_zoomed_out` and the following `type_b_initialized`
state remain **unowned**, rather than being merged into an opaque
12-byte aggregate with no callable historical symbols.

Two pinned Borland C producers in
`.analysis/unit-replays/gpt-web-shinki-bg-particle-seed-a/receipt.json`
match all two initialized bytes, the complete original OMF/MAP DATA
scope and empty ordered fixups. The compiled mutation `(-1 & 0xff)`
to `(-2 & 0xff)` changes the genuine sentinel and is rejected. The
semantic C++ consumer will be validated separately under its complete
function owner; this DATA unit grants no CODE credit and requires no
whole-game cold replay.

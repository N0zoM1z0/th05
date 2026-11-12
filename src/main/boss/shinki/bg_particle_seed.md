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

## Actual large-background C++ consumers (2026-11-12)

The complete `background.cpp` now imports the genuine initialized
`shinki_bg_type_a_particles_alive` C symbol from
`background_rules.h`, removing the independent unqualified external
C++ declaration. The two source owners share the same 255 initial
sentinel and signed near-word type. The 17 actually affected background
CODE units and the refreshed C DATA unit were all verified together,
with real native compiler outputs and compiled negative rejected.
See `background_rules.md` and
`.analysis/unit-replays/gpt-web-bg-particles-seed-shinki-a/receipt.json`.
The surrounding zero-initialized or alignment bytes remain unowned.

## All adjacent source-defined background state (2026-11-12)

The real consumer now obtains all the original separately initialized
Shinki state flags and counters from the same `background_rules.h`
C-linkage interface, while EX-Alice's hexagram byte retains its
one-byte enum semantics. The original two-byte 255 particle sentinel
still has its own native compiler proof and is not recredited;
its refreshed producer receipt is
`.analysis/unit-replays/gpt-web-bg-abi-seed-b/receipt.json`.

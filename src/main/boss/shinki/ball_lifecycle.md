# B6-ball generation, cloud fade, collision and four-cel decay

The independently accepted 81-byte `b6balls_add()` and complete 220-byte
`b6balls_update()` are a real source-level producer/consumer pair. The
former allocates one of 63 original 26-byte custom-entity slots, gives it
a velocity derived by the original near vector helper and the rank-tuned
spawn speed, and initializes a **48-pixel cloud radius**. The latter
shrinks the cloud by **2 pixels per frame** until it is *strictly below*
the original 32×32 ball's 16-pixel half-width. It then maintains the
original position, active hitbox and player-hit checks, using the same
near-Pascal collision path and true cloud/active/decay/free flag values.

The shared `b6ball_t` and `b6ball_template_t` overlays also now spell out
the original signed storage widths: the unused entity bytes are signed
8-bit fields, and the template's reserved words are signed 16-bit slots.
The original `b6ball_t::age` comment is restored as well: the word is unused
and broken because the original update never resets it. These declarations
match ReC98 `th05/main/bullet/b6ball.hpp` and were checked by replaying all
17 accepted functions that include `shinki.hpp`; the two build paths used by
the wing owner both remained exact.

The original accepted source still applies bullet clearing before the
movement/collision test, halves both signed velocity components upon
entering decay, and advances the decay cel every **four frames** through
the existing sprite range 204–207 before freeing the slot. The
`ball_lifecycle.hpp` interface now names these five physical game
constants, without adding entity state, changing two's-complement
rounding, replacing the true `playfield_encloses()` expression or
moving the two original optimizer-structural leaf calls. The source
still runs age increment and segment-3 position update in the exact
original order.

The real shared `balls_update_body.inl` and the `shinki.cpp` generator
were both edited, so ten original-source accepted units were rebuilt
in a **bounded** native batch. The receipt
`.analysis/unit-replays/gpt-web-shinki-ball-lifecycle-full-b/receipt.json`
records two independent original Borland producers, full original raw
CODE and ordered MZ relocations for **all ten** accepted units,
including all 81 generation bytes, all 220 lifecycle bytes, and their
surrounding pattern/float functions. The existing compiled semantic
`age++`→`age += 2` negative is rejected. All bytes were already
accepted; this improves source-level lifecycle meaning without
claiming new code credit or rerunning the entire game.

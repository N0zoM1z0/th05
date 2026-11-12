# Shinki background A/B/C/D controllers and the original C seed interface

The genuine MAIN stage-six background system is a contiguous family of
source-defined near and Pascal functions, not an independent renderer.
Its physical particle counter is now a separate, initialized, **two-byte
C public** `shinki_bg_type_a_particles_alive`, shared by the C++
background source through the C-linkage declaration in
`background_rules.h`. The actual original DGROUP seed is word 255 at
`209D:198A`, and the C++ type-A initialization compares against the
same `(-1 & 0xFF)` semantic sentinel. The code does not replace or
allocate the original `boss_particles`, `linesets` or other phase-state
objects. It does not claim any of the neighboring zero-initialized
background flags as authored DATA.

The real *A-type* background creates two opposite-facing line sets,
initializes the true particle pool with the offscreen `-999`-pixel
sentinel, then starts at most one new particle **every four Boss frames**
at the playfield center. The original speed range is 2–6 pixels per
frame, and the initial line angle is 0x40 with opposite 0x80 turn.
Once the linesets zoom out to radius 224, the existing byte-count
latch advances. Its two near helpers continue to grow lines and render
particles, rather than being merged into the large controller.

The *B-type* background sets initial line radius 256, horizontal
initial centers at 1/6 and 5/6 of the playfield, and drives the
original falling particles and vertical line velocities toward -14.
The *C-type* reverses the vertical motion and changes the particle
velocity bound to -10, with its distinct upward-line 14-pixel speed
limit. The *D-type* reuses the original particle buffer as rising
smoke, initialized at -1 pixel velocity and indexed into existing
64-pixel vertical bands. The separate `shinki_bg_render()` preserves
its true Boss-phase classification at 4, 8 and 12 and its original
GRCG/direct-color page operations. These phase values are source
constants only; no new Boss state machine or image data was copied.

The source edit touched the shared `background.cpp` that also compiles
Sara, Louise, Alice, Mai/Yuki, Yumeko and EX-Alice backdrop functions.
Every one of the **17 complete accepted background CODE scopes**, plus
the independently accepted two-byte C seed contributor, was therefore
replayed in one focused native batch. The two independent pinned
Borland producers match all original raw bytes, OMF/MAP boundaries,
ordered relocations and their compiled negative controls, including
the original 306-byte A-type initialization, 224-byte B-type part1,
281-byte B-type update, 332-byte C-type update, and 173-byte final
Shinki background router. Receipt:
`.analysis/unit-replays/gpt-web-bg-particles-seed-shinki-a/receipt.json`.
The source paths are semantic improvements to already accepted CODE,
not new CODE byte credit. No other source owner or full-game cold replay
was run.

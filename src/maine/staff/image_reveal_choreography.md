# Staff image reveal A/B: exact source-visible five-stage wipe protocol

Both independently accepted **376-byte** near-Pascal image reveal
procedures operate on distinct original MAINE image-phase, wipe-extent
and frame counters and on separate two-space C image-cover strings.
The source now includes one compile-time-only
`image_reveal_choreography.hpp` from the original canonical `*.inl`
bodies. This names the preparation phases 0..1, covering phases 2..3,
uncover phase 4, and the real screen text geometry (16-pixel image cells,
8-pixel byte columns, 80 text columns). No BSS, new state, sprite
bitmaps, fake device routines or alternate callback bodies are created.

On the first image draw, the real wipe extent is picture width in
16-pixel cells plus **seven lead cells**. The existing code places the
picture and erases every other 16-pixel text cell by passing each
source-owned blank string to the original reverse-black `text_putsa()`.
On the next phases, the extent changes **once per four frames** and
advances only on the real `staff_text_wipe()` covered/uncovered result
values **1/2**. The final cleanup uses the authentic 128-cell extent,
restores phase zero and sets the existing `staff_text_clear_requested`
byte. The two underlying update implementations intentionally preserve
their original distinct increment expression shapes; only the literal
protocol values have readable source names.

`full.cpp` and `staff_complete_context.cpp` include these two genuine
bodies alongside the complete original Staff and 991-byte controller
context. Thirteen accepted units depend on this source: the two image
updates, clipping, image wipe, particles, scene render, bitmap functions
and final controller. All thirteen were rebuilt in a **single bounded
native replay**, with two deterministic Borland producers, full raw
bytes, original OMF/MAP boundaries, actual ordered relocations, and a
rejected compiled semantic mutation changing the second reveal's wipe
headstart from seven to eight cells:
`.analysis/unit-replays/gpt-web-staff-image-reveal-choreography-b/receipt.json`.

A first diagnostic stopped at the negative-control stage because its
old mutation anchor referred to `pixel_w / 16 + 7`. The anchor was
updated to the same expression with named constants and the *real*
producer/negative were rerun successfully; no failed receipt was
imported. The independently accepted six-byte C image-cover DATA and
prior 376-byte functions retain their original byte credit only.
The original `image_phase.hpp` and reviewed CDG ASM source inputs are
unchanged in this commit, so no unrelated ASM refresh was required.

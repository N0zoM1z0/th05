# Reimu and Yuuka bomb draw candidates

These are two independent complete natural C++ owners. Reimu occupies
`[FD17,FD6B)` (84 bytes, 28 instructions); Yuuka occupies `[102F9,10371)`
(120 bytes, 42 instructions). Both use near `main_01` frame `0AE1`, shared
graphics/sound frame `14AB`, and DS `209D`. Native review includes both early
and final returns and every branch destination. Neither has a table, padding,
initialized DATA, BSS or asset array.

The shared new header imports the unchanged complete 480-byte BombAnimation
surface. The functions dispatch the real star/heart animation and character
backdrop consumers, which remain foreign implementations with their actual
near ABI. They draw the CDG background at the true coordinates, select circle
color 9 and apply the entrance tone formula `196 - ((bomb_frame - 32) * 3)`.
The byte frame promotes to signed int for the arithmetic.

Reimu plays sound 9 only through frame 112 on the real `stage_frame_mod4`
cadence. Yuuka retains the two signed promoted-byte `% 4` tests: remainder zero
plays the sound and selects tone 150; remainder two selects tone 100; other
frames do not call `palette_show`. The changed branches share the actual far
Pascal palette call. Deferred entrance updates and immediate later flashing
remain separate behaviors.

The original ordered fixups are `[80,14]` for Reimu and `[116,81,14]` for Yuuka.
Their primary master/TH04-family CDG, sound, circle-color and palette interfaces
agree with existing maintained bomb owners. Calibration confirms a unique full
instruction-shape route for each body; neither calibration bytes nor its fixup
collection order is accepted evidence for the originals.

Separate symbol-only binders retain authentic helpers before and after each
complete contribution and the actual DS fields. All ORG holes lie outside the
compiled function, with individual extents below 64 KiB. The fixed tails are
valid only after actual OMF confirms 84 and 120 bytes. No assembly, emits,
physical-register hints, dummy helpers or copied assets are present.

Private `.analysis/reimu-bomb-draw-boundary-review.json` and
`.analysis/yuuka-bomb-draw-boundary-review.json` contain native boundaries,
branches, calls, original ordered fixups, hashes and ABI evidence. Their separate
`*-unit-proposal.json` files register one complete owner each; the combined
`.analysis/character-bomb-draw-unit-proposals.json` is an integration convenience,
not a contiguous target extent. The meaningful negatives change Reimu's initial
tone constant 196 to 195 and Yuuka's later bright flash 150 to 149.
`python3 .analysis/character-bomb-draw-review.py` repeats the native checks.
Both candidates remain uncompiled and unaccepted pending focused two-producer
raw/original-ordered-fixup comparisons, OMF/MAP/dependency gates and own controls.

The first focused replays `main-reimu-bomb-draw-a` and
`main-yuuka-bomb-draw-a` both passed two fresh complete producers, full raw
bytes, each original ordered fixup stream and their own palette negatives
(196 to 195 for Reimu, 150 to 149 for Yuuka). The root imported the complete
84-byte and 120-byte owners. Their sources, shared `bomb_draw.hpp` and separate
binders are now frozen accepted inputs.

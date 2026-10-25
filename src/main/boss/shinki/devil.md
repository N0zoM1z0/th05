# Shinki devil pattern

This accepted producer restores the complete natural `pattern_devil()` function at
MAIN load offsets `[0x1B244, 0x1B566)`: 802 bytes, one near C++ function in the
original `1527` code frame. Native decoding covers the entire extent through
its final `RET`; there are no instruction NOPs, switch tables or padding bytes.
The original ordered MZ relocation offsets are `[790, 582, 160]`.

The retained full Shinki object already contains the natural 802-byte body.
Its strict OMF link reconstruction agrees with the retained executable, and
its three function-relative relocations agree with the original target in
that same order. The retained raw differences are foreign-call displacements
and the call to the earlier, independently accepted `b6balls_add()` provider.
That is evidence for trying a genuine standalone translation unit; it does not
establish standalone exactness before actual producers exist.

`devil.inl` is the current function body verbatim. The complete HP enum and the
two existing inline wing-coordinate calculations are shared through `hp.inl`
and `wing_coordinates.inl`. Expanding those three new includes in
`shinki.cpp` restores its exact pre-factor bytes, SHA-256
`5e68bf65ebfa90b1587b38ad423aaaa9e9cf4f61e97bf80e14e83a360305cd93`.
The existing Cheeto include remains in that restored file. The canonical full
Shinki header, `phase23.cpp`, and Cheeto wrapper/header/body are unchanged.
No shortened Boss, laser, bullet, entity or HP view is introduced.

The independent wrapper keeps near `b6balls_add()` foreign at `1527:580E`
(load `0x1AA7E`). Its other near providers are the genuine rank-independent
bullet spawner, player-angle calculation, random-ring modulo, laser spawn/grow,
and small explosion functions. The far rank selector remains `0AE1:21A2`,
and the far sound entry remains `14AB:0232`; their first declarations retain
those actual code contexts. The symbol-only binder reserves only foreign
extents outside the complete compiler contribution, with DS at `209D`.
It supplies no function instructions, target bytes, internal holes or stack.

The compiled negative changes only the staged canonical body:
`boss.phase_frame >= 2500` becomes `>= 2501`, changing the fast-laser transition
threshold. It has exactly one source match. The DOS module alias is
`th05/b6devil.cpp`.

The nine existing accepted units whose source is `shinki.cpp` require their
necessary affected-closure refresh after this second canonical factor. Their
old records remain intact until fresh evidence is imported. The standalone
Cheeto owner and the separate phase helper have unchanged source closures.
Wing preparation, the 220-byte ball updater and the main Shinki update remain
parked; this candidate makes no claim for them.

Private reproducible evidence is recorded in
`.analysis/shinki-devil-factor-baseline/`,
`.analysis/shinki-devil-factor-proof.json`,
`.analysis/shinki-devil-boundary-review.json`, and
`.analysis/shinki-devil-freeze.json`. Preparation used only native reads,
disassembly and hashes, with no compiler execution. No new acceptance or
progress credit is claimed here.

`main-shinki-devil-a` passes two fresh deterministic producers, all802 raw
bytes, the original ordered fixups and its rejected2500→2501 control.
`main-shinki-canonical-refresh-b` replaces the nine affected old records after
both body factors; no unrelated unit was cold-replayed. The family now has
13 accepted functions /2559 instruction bytes. Its remaining220/386/959-byte
functions stay unaccepted, including the final update's table and padding.

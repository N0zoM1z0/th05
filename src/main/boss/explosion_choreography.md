# Boss explosions: original small/big rings and real native 16-bit frame

The accepted complete **452-byte two-function** original MAIN Boss
explosion renderer now imports the independently accepted
`explosion_big_frame` near C public from
`src/main/boss/explosion_frame.h`. Its original word resides at
DGROUP `209D:18E4`, rather than the bonus counters at `1A62/1A63`.
This source-level linkage restores a genuine original address and
semantics, not an extra frame or replacement Boss explosion structure.

The small explosion loops over its two real `Explosion16` slots and
renders **64** tiny 16×16 sprites around each original circular ring,
rotating through the original 256-angle-coordinate system. Both the
small and large explosions advance their actual radii, age and alive
state. The 32-frame lifetime remains the original source expression.
The large explosion uses **16** sprites, with the intentionally
original **64×64 clip assumption** even though the physical pattern
is smaller; that historical display behavior is not corrected here.

The large explosion increments its live signed-word frame exactly once
per active update and drives the original palette protocol: before
frame 8, only *odd* frames flash tone **150**; from frames 8 through
15, the fade tone follows `100 + 16×6 − frame×6`; all remaining
frames use tone **100**. On the first inactive update the same C state
resets to zero. The animation, exact direct PC-98 VRAM drawing, and
all near/far graphics calls keep their original code order and ABI.

The canonical source now uses `explosion_choreography.hpp` names for
ring counts, lifetimes, clipping and tones. The original compiled
semantic negative changes the real 32-frame expiry to 33; it is
compiled and rejected. The complete 452-byte two-function CODE unit
and the separately source-defined two-byte frame DATA were both
replayed with two pinned native Borland producers, all complete raw
bytes, OMF/MAP scopes and original ordered MZ fixups:

- `.analysis/unit-replays/gpt-web-boss-explosion-native-choreography-a/receipt.json`
- `.analysis/unit-replays/gpt-web-boss-explosion-own-c-data-b/receipt.json`

As an independent address-integrity check, the complete 561-/579-byte
Stage Clear and All Clear functions were also recompiled from their
original source and checked with the previous Miss/Bomb C DATA at the
correct DGROUP `1A62` address:

- `.analysis/unit-replays/gpt-web-bonus-real-address-calls-b/receipt.json`
- `.analysis/unit-replays/gpt-web-bonus-real-address-data-b/receipt.json`

All 452+561+579 CODE bytes were already accepted and are not counted
again; the corrected initialized-DATA ownership was committed
separately. No full cold replay or guessed in-function bytes were used.

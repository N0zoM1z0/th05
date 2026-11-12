# Yumeko's two exact counterrotating and mirrored bullet spreads

The original independent **518-byte two-function** MAIN C++ contribution
contains `yumeko_pattern_counterrotating_spreads()` and
`yumeko_pattern_mirrored_spreads()`. Both are genuine near-callbacks
selected by the complete 884-byte Yumeko Boss state machine, not
copies of the already accepted 283-byte Sword update ASM.
`spread_choreography.hpp` now gives their original gameplay timings
and angles source-level names without allocating new state or changing
Turbo C++ expression widths.

Both patterns gather circles through frame **16**, using two original
colors **7/6** with a one-frame age lead, and charge their bullet
template at frame **4** (charge sound 8). They retain the original
**56-subpixel** base projectile speed (`3×16 + 8`) and fire on every
eighth phase frame starting after the charge. Counterrotating spreads
initialize angles 0x60/0x40 and use the real packed **5 bullets / 2
angular-step** byte/word template. Each subsequent volley fires the
original symmetric 0x80 reflected blue ball and pellet shots from
**48-pixel** and **32-pixel** radii, then decays the angles by **8** and
**6** respectively. Exactly at frame **256** it resets its own phase
clock and returns control to the pre-existing Boss reposition mode.

The separately retained mirrored spread initializes an aimed green
projectile with angle step **20** and turns around the true 0x80
reflection axis, emitting five and four shots from separate player-
relative origins. Its rotation proceeds +8 per volley, and at frame
**192** resets its clock and the existing reposition mode. It does not
change RNG order or the original sound effects.

The complete actual two-function source is recompiled under two native
pinned Borland C++ producers and matches **all 518 original raw bytes**,
original OMF/MAP context, and the literal ordered original MZ fixups.
Its compiled negative changes the counterrotating termination frame
from 256 to 257, and is rejected:
`.analysis/unit-replays/gpt-web-yumeko-counterrotating-and-mirror-spreads-a/receipt.json`.
The source's two existing scratch-byte aliases still refer to original
`boss_statebyte[14]/[15]`. No new or duplicated CODE/DATA is credited;
no full cold replay was performed.

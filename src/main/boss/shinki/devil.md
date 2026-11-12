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

## Exact Devil laser/bullet state transitions

The complete Devil attacker now gives semantic names to the true timing and
angle limits, without changing their numeric values or the original eight-bit
state overlay. Its spread bullets start after a **192-frame** staging delay
and fire every four frames. Lasers are normally enabled by the HP gate, or
forced after frame **1800**. The four fixed lasers begin a 64-frame growth
counter, grow once when that counter reaches 64, and enter the turn phase at
counter 65. The outer spread angle reaching `0x30` first establishes the
`lasers_active` latch; the following 8-frame turns use inner laser reversal
angles `0x38` and `0x41`, and accelerate the six-ball pattern at the original
HP/frame fast-stage gate. This is not an unconditional cross-phase reset:
Shinki's main controller later reads that same physical byte 10 as the
late-wave selector.

These timing names are local C++ enum constants, preserving Borland's original
integer-width comparisons, modulo operations and ordinary control flow. The
standalone 802-byte `pattern_devil()` and every other owner compiling its
shared source context were replayed **together: 12 original units**, including
the 959-byte complete Shinki controller, with two original-byte exact
Borland/TLINK producers and the original ordered relocations. The existing
compiled `2500 → 2501` laser-fast-stage negative was rejected. Evidence:
`.analysis/unit-replays/gpt-web-shinki-devil-attack-timing-20261111/receipt.json`.
No additional executable bytes are claimed by this refinement.

## Four-column Devil projectiles and rank-specific firing periods (2026-11-12)

The full 802-byte Devil attacker now uses `devil_ballistics.hpp` for the
actual four independently addressed lasers, their width 6, red/blue
laser color 14, initial 0x40 direction, the 0x80 left/right reflection,
prelude-to-full bullet count 1→3, spread angle 0x30 and 7-pixel-per-frame
red volley. The four lasers are created and grown in distinct calls
using the **same original slot numbers** later stopped by the accepted
959-byte Shinki Boss controller. The decorative pellet and random
purple B6-ball retain their original separate sprite selectors, aiming
algorithm, and speed 3.75. No drawing asset, new state object, changing
call order or source-ASM instruction injection is introduced.

Both actual rank-specific B6-ball intervals are separately named: the
initial ramp uses easy/normal/hard/lunatic **64/40/32/28** frames; the
later fast pattern uses **52/20/16/12**. A diagnostic uncovered a real
Borland 4.02 preprocessor identifier-significance limit. Long macros
sharing the first 31 identifier characters caused all four arguments
passed to `select_for_rank()` to fold to the **Lunatic** value. That
first genuine compiler candidate matched 796/802 positional bytes and
all three ordered relocation sites, but failed the original six
immediates. No credit was accepted from that candidate. Distinct
shorter `DEVIL_BALL_START_*` and `DEVIL_BALL_FAST_*` identifiers fully
recover the four original values without changing expressions or using
compiler barriers.

The **complete twelve-unit Shinki source-change cohort**, not just the
standalone pattern, was then rebuilt twice with the pinned native
Borland toolchain:
`.analysis/unit-replays/gpt-web-shinki-devil-ballistics-full-c/receipt.json`.
All twelve complete original CODE extents and original ordered MZ
fixups are exact, including the 802-byte Devil attacker and the entire
959-byte Shinki update with its 26-byte compiler dispatch table and
checked alignment zero. The compiled laser fast-stage 2500→2501
mutation was rejected. Previously accepted CODE earns no duplicate
source-byte credit; no whole MAIN or ZUN executable was replayed.

## Separate physical C laser-delay and floating-direction publics (2026-11-12)

The full 802-byte Devil leaf now obtains its actual native `int near`
`shinki_devil_laser_grow_delay` through the same `extern "C"` header
used by the independently accepted two-byte C initialized DATA.
The original byte-type float direction similarly links the complete
Shinki main Boss controller to the separately accepted one-byte C
initializer. Two-source consumer and producer receipts are detailed
in `devil_float_data.md` and preserve every original byte, relocation
and compiled negative. There is no new laser state allocation.

## Seven symmetric firing sites, with original first-decoration ordering

The complete 802-byte `pattern_devil()` now spells the repeated fixed-speed
bullet emission through `DEVIL_FIRE_COL(angle)`, used for four regular red
columns and three of the four decorative mirrored columns. The first
decorative shot deliberately remains explicit: its original instruction order
sets the angle *before* moving the origin back to the rightmost column. An
initial trial incorrectly moved first and changed 13 source-generated bytes
while preserving size/fixups; it was rejected. Restoring that order gives the
original 802/802 bytes and ordered fixups `[790, 582, 160]`.

Because the actual body resides in shared `devil.inl` (not the six-line
`devil.cpp` wrapper), the accepted replay covers all **12 dependent Shinki
units**, including the complete 959-byte Shinki state machine. Two genuine
Borland/TLINK producers and the existing compiled 2500-to-2501 threshold
negative passed for the entire closure. The receipt is
`.analysis/unit-replays/gpt-web-shinki-devil-seven-columns-closure-20261112-d/receipt.json`.
This is an exact natural-source refinement, with no duplicate code credit.

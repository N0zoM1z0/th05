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

## Remaining angle and fast-stage protocol (2026-11-13)

The Devil's opening four-column volley now names its remaining source-level
constants: the 2,500-frame forced fast-stage gate, three decorative pellets,
the zero-angle origin for negative mirrored columns, the prelude's outer/inner
increments of 4/2, and the later outer turn step of 2. The four laser directions
use the same 0x80 half-turn already used by the mirrored bullet columns. The
prelude advances every four frames until the outer angle reaches 0x40; the
full pattern then turns clockwise to 0x30 and back counterclockwise to 0x40,
while the inner angle moves by one per volley. The 2,500-frame gate can select
the fast B6-ball cadence even before the HP threshold is reached.

A first naming pass used `+= 1` / `-= 1` for the inner unit turn. Turbo C++
4.02 expanded those into AL load/add/store sequences instead of the original
single-byte memory INC/DEC, growing the complete function by eight bytes.
Restoring the original postfix `++` / `--` expressions preserved the direct
memory opcodes; the remaining names then produced the exact original 802-byte
function. The complete twelve-unit Shinki source closure, including the 959-byte
controller and all shared `shinki.cpp` consumers, passed two native Borland /
TLINK producers with original bytes and ordered fixups; the existing compiled
2500-to-2501 fast-stage negative was rejected. Receipt:
`.analysis/unit-replays/gpt-web-shinki-devil-state-protocol-c-20261113/receipt.json`.


## 2026-11-14: byte-10 Devil latch, HP safety margin and laser teardown

The Devil attack's `lasers_active` is not an independent boolean. It aliases
`phase_relative` at `boss_statebyte[10]`, the one-byte selector used by the
shared phase-9/phase-10 controller. The phase-9 exit calls
`boss_phase_next(ET_SW_NE, HP_PHASE_10_END)`: the helper first copies the old
`phase_end_hp` (the `HP_PHASE_9_END` value **8600**) into `boss.hp`, then installs
phase-10's **2800** HP end threshold. The controller increments byte 10 to 1
and installs `pattern_devil`. At Devil frame **192**, its bullet startup
initializes the angle protocol and deliberately clears the same byte to zero.
The final phase-10 controller branch is selected only after the Devil leaf
restores that byte to 1.

The four-column bullet prelude fires every **4 frames**. It begins at frame
192 with outer angle `0x00`, adds `0x04` per volley, and reaches `0x40` after
16 prelude volleys. Frame **256** observes `0x40`, sets `bullet_intro_done`,
and immediately begins the full three-way spread and clockwise `-0x02` turn.
The outer angle reaches its low boundary `0x30` at frame **284**, then alternates
back to `0x40` at 316 and to `0x30` at 348. The low boundary therefore recurs
every **64 frames**. The rank-specific first B6 ball can fire on frame 256 for
Easy/Hard or frame 280 for Normal/Lunatic; the initial intervals are 64/40/32/28.

Laser creation is triggered by `boss.hp <= 5600` or the forced frame **1800**.
On trigger frame T the leaf creates four `LF_FIXED_WAIT_TO_GROW` lasers and
increments `laser_grow_delay` from zero to one; the bottom of that same callback
increments it to two. It reaches 64 on T+62 and calls `laser_manual_grow()` on
T+63, changing the delay to 65. Only from T+64 does the leaf test the outer
`0x30` boundary for the shared byte. If the boundary was reached on T+63, the
grow branch takes precedence and misses it; the next boundary is no later than
T+127. The shared byte is therefore restored within **127 updates** of the
laser trigger, regardless of which four-frame bullet-angle cycle was current.

The laser's physical state is separate from this phase latch. `fixed_init()`
starts each manual laser at width 1 and age 0. Because the global loop runs
`lasers_update()` before `boss_update()`, the grow callback at T+63 sees age 63;
laser widths then grow on odd ages 63, 65 and 67. They reach width 7 and enter
`LF_FIXED_ACTIVE` on T+68, with their first actual laser hit-test on T+69. Thus
all four beams can already be collidable before byte 10 is restored. This is
why the HP separation is a real gameplay invariant, not just a convenient
scratch-byte convention.

The 128-frame startup window is protected by the original **2800 HP** gap
between the Devil laser trigger (5600) and phase end (2800). The player shot
clock is an 18-frame cycle; `shot_func_init()` consumes the six shot-time
values 18/15/12/9/6/3. The fixed-power-level model uses the exact cycle damage
and maximum single-shot damage from all ten initialized levels. Its maximum
same-level 128-frame upper bounds are:

| Character | Worst fixed-level budget | Power level | Stage 6 Boss multiplier |
|---|---:|---:|---:|
| Reimu | 2270 | 9 | 5/4 |
| Marisa | 1652 | 7 | 4/5 |
| Mima | 1818 | 9 | 4/5 |
| Yuuka | 2570 | 9 | 5/4 |

Each bound assumes that all **64** live shots and eight complete 18-frame shot
cycles hit for their full damage, before the Stage 6 multiplier. The real
`shots_hittest()` path divides successive hit damage by the hit count and clamps
each share to one, so for a fixed power level its sum cannot exceed this
full-damage model. The worst fixed-level case is Yuuka level 9 at 2570 HP,
leaving **230 HP** below the 2800 threshold. Allowing bomb frames to add one HP
and defer `phase_done` raises the worst fixed-level mixed-window bound to 2571,
leaving **229 HP**.

This calculation deliberately pairs the live-shot pool and future shot cycles
at one power level. A power-level change during the 128-frame window would mix
shots created by different levels in the live pool; proving that case requires
the actual lifetime/turnover of those 64 shot slots, not just their static
capacity. The original source comment asserts the HP separation as the safety
invariant; this replay pins the exact fixed-level budgets and does not claim a
separate mixed-power lifetime proof. If the laser trigger is the forced frame
1800 rather than the 5600 HP crossing, the remaining HP gap is larger. During
bombs the controller rewrites effective damage to one and forces
`phase_done=false`, so the phase cannot exit while the alias is still zero.

Laser-angle motion begins only after byte 10 has been restored. It updates on
phase frames divisible by **8**. The fast B6 interval switch is gated by HP
`<= 3800` or frame `>= 2500`, and is checked only on those laser-turn updates.
If the time gate is the first trigger, frame 2500 is not a turn (`2500 % 8 = 4`),
so frame **2504** is the first eligible update. The B6 spawn check occurs
before the fast interval switch in the same callback, meaning a ball on that
frame still uses the old interval; the new rank interval (52/20/16/12) starts
on the following callback. The post-increment comparison against
`DEVIL_FAST_DELAY_SENTINEL` (65) is a one-shot explosion/switch gate, not a
phase-frame threshold. The underlying
`shinki_devil_laser_grow_delay` is a 16-bit `int`, not a byte: manual growth
leaves it at 65, and even a full 3,000-frame phase can add at most 375
8-frame-turn increments. It therefore cannot wrap back to 65 and retrigger.

The four laser slots must be stopped by the phase controller, not by the
looping leaf. The controller runs `wing_pattern()`, performs the HP/timeout
decision, advances the phase, and only then calls `laser_stop()` for slots A-D.
The global loop has already run `lasers_update()` before that controller call.
`laser_stop()` sends an active fixed laser to `LF_FIXED_SHRINK`, but immediately
frees a laser still waiting or growing. An active beam therefore renders at
its current full width on the phase-exit tick and starts shrinking on the next
laser update. Moving this cleanup into `pattern_devil()` would change the
last-frame hit/render order and would not know whether the controller had
actually accepted an HP or timeout exit.

`tests/test_shinki_devil_lifecycle.py` pins the shared byte, the 192/256/284
angle milestones, the 127-frame latch-restoration bound, the all-character
shot-damage safety margin, the rank-specific B6 intervals, the fast-switch
call order, bomb suppression, and controller-owned laser teardown.


## Four-column geometry and the laser's independent sweep clock

The Devil uses the 256-pixel wing width as one shared horizontal coordinate
system. The first column is offset by `256/2 - 256/8 = 96` pixels from the
Boss center, and each following column subtracts one quarter of the wing width
(**64 pixels**). The four origins are therefore **+96, +32, -32, -96** pixels
for slots A-D. The laser setup and red spread both walk these columns from
right to left. The decorative spread deliberately starts at the opposite
edge of the just-finished red volley: after the red volley leaves the template
origin at -96, its first decorative shot adds `3*64` and returns to +96.

The red volley uses angles `(outer, inner, 0x80-inner, 0x80-outer)` at those
four positions. Before the prelude completes each column fires a single red
bullet; after the outer angle first reaches `0x40`, each fires a three-bullet
spread with the same `0x30` arc. The decorative volley uses
`(0x80+outer, 0x80+inner, 0x00-inner, 0x00-outer)` and also fires three-way
spreads. Its first angle is selected before the origin is shifted back to the
right edge; the three remaining calls shift left before assigning their angle.

The four laser angles are assigned in A/B/C/D order as
`(outer, inner, 0x80-inner, 0x80-outer)`. Only after all four writes does the
leaf advance its two scratch angles. This is important at the reversal points:
the visible beams use the pre-step endpoint for that turn, and the next
8-frame update begins travelling in the opposite direction. The outer and
inner angles start at `0x40`; while clockwise, outer increments and inner
decrements by one. The inner value `0x38` flips direction. Counterclockwise,
outer decrements and inner increments by one until inner reaches `0x41`, which
flips direction back. The first 18 turn states are pinned by
`tests/test_shinki_devil_geometry.py`: turn 8 is `(0x48,0x38)` and turn 17 is
`(0x3F,0x41)`, with the full angle/direction state returning to its initial
state after 18 turns (**144 frames**).

The laser sweep has a separate 8-frame clock from the 4-frame bullet spread
clock. The shared latch can only be restored at outer-angle low-boundary
frames `284 + 64*n`, all of which are `4 mod 8`. Because the leaf's
`!lasers_active` branch takes precedence over its angle-turn branch, the
first laser-angle write is four frames later, at frame `288 + 64*n`. This
separates the last bullet-angle transition from the first beam-angle update
without resetting either clock. The geometry test pins all four origins,
red/decorative angle order, mirror-write order, both reversal thresholds, and
the first post-latch turn frame.


The controller deliberately retains the byte-10 `phase_relative` comparison
when deciding whether the shared wing phase advances into Devil or exits to
phase 12. Substituting `boss.phase == SHINKI_PHASE_SYMMETRIC_SPREADS` looks
behaviorally simpler, but the focused original-target replay changes the
959-byte update-context contribution. The byte comparison is therefore part
of the exact source reconstruction, not merely a leftover phase counter.

# Complete Yuki solo update candidate

The complete C far Pascal callback `YUKI_UPDATE` covers original MAIN
`18A05..18D3F`,826 bytes. Its228 instructions occupy806 bytes and contain
two genuine RETF exits. The final20 bytes are the complete10-entry compiler
switch table, with no alignment byte. All table destinations and direct local
branches land on original instruction starts. Ordered fixups are `[256,140]`.

The state machine fills HP, reveals Yuki, initializes custom bullets, approaches
waypoints, cycles through real near callbacks, advances HP thresholds and
performs defeat cleanup. The default defeat path returns before custom-bullet
and HUD updates, preserving the second full return path. The phase counter's
byte promotion to signed16-bit modulo5 and the explicit minus8 byte state
initialization retain their actual widths and semantics.

The frozen `b4ball.hpp` provides the complete canonical custom26/B4Ball26 and
B4BallTemplate25 storage, including real unused fields and bool16 revenge.
The owner writes only the real origin and tiny-pattern-base216 template fields.
Both Boss records remain the complete24-byte canonical type; the second record
at DS5AD2 is used as the real waypoint storage. The complete canonical16-bit
explosion enum is reused without importing generic.hpp, whose broader constant
names conflict with the frozen Mai/Yuki macros. No accepted header is edited.

The existing two2-entry and one5-entry pattern-selector tables at DS1964,
1968 and196C are declared semantically without defining their pointer entries.
No initialized DATA, BSS, asset, instruction array or helper body is supplied.
The accepted shared callback pointer remains at DS4438.

Near game code uses frame1527. BG rendering, B4Ball rendering and the null
callback belong to main01/AE1; the growing circle is far Pascal AE1:347A.
Sound is far C Pascal14AB:0232. Custom-ball reset/update are the actual C near
Pascal entries at183D5 and18459. The update's original C Pascal linkage agrees
with the independent shared Mai/Yuki caller. DS is209D. The symbol-only binder
places all foreign segments in their actual groups, follows the full826-byte
contribution with an outside byte tail, and ends it at209D0. It defines no
instructions, initialized values, stack or hole within compiled functions.

ReC98 `th05_main.asm` lines14675..14976 supplies semantic evidence. The native
prologue and complete point-initialization sequence uniquely locate the actual
original callback. All228 complete instruction shapes then agree with cached
calibration at1B9F2, a local displacement of `-2FED`. Routing evidence and source
presence remain separate from source acceptance.

Private `.analysis/yuki-update-boundary-review.json` contains the whole-unit
proposal, complete table metadata and a unique staged negative changing
end-HP4600 to4500. Two fresh focused producers, full826-byte comparison,
original ordered fixups and compiled rejection remain required. This packet
was prepared with native/static tools only and executes no compiler.

`main-yuki-update-c` passes two fresh deterministic complete826-byte raw
comparisons and original ordered fixups[256,140]. The actual phase threshold
4600→4500 control is compiled and rejected for this whole callback. Authored
credit is826 bytes (806 instructions plus20 semantic switch-table bytes),
one complete function, with no padding, DATA or BSS. All table bytes and
both complete RETF paths remain in the verified extent.

Source integration now uses `boss_solo_pattern_current` for the genuine
DS4438 callback slot shared by both survivor states. This is distinct from
the shared-fight Yuki callback at4430 and the internal Mai void callback
at443A. Only this826-byte accepted owner required replay for that rename;
its final c receipt preserves the complete original raw bytes and fixups.

## Solo Boss phase and pattern-count meaning

The complete Yuki controller now names the original ten phases through the
final snow-cross wave. Its three normal attack-wave dispatches distinguish
reposition from active pattern callbacks; the first, second and final waves
exhaust after 12, 24 and 36 completed patterns respectively. The intervening
movement, rapid-fire and final arrival phases retain their original order.
The stage's defeat transition remains phase 253 and the native switch table
still holds 0–9 as ten genuine selector values.

The actual `main-yuki-update` scope was rebuilt and compared at **826/826
bytes**, including the 20-byte compiler switch table, two full return paths,
and original ordered relocations. A compiled end-HP negative was rejected.
The same focused receipt covers Mai and Yuki:
`.analysis/unit-replays/gpt-web-survivor-solo-phase-semantic-20261111/receipt.json`.

## Shared Yuki solo snow-state layout

The final Yuki approach seeds the original bytes at offsets 13, 14 and 15 with
`-8`, `8`, and `0x10`. Both the initial and later real solo pattern source
contexts use those same offsets through their `yuki_solo_snow_step`,
`yuki_solo_angle_step` and `yuki_solo_angle` aliases. The new
`YukiSoloScratch` view preserves all sixteen original physical bytes and
checks the three field offsets at compile time. It does not imply that earlier
waves preserve those values; the final approach explicitly reinitializes them.

The complete update and both pattern cohorts were replayed together with Mai's
related owners: five changed units, two deterministic exact native producers,
original ordered relocations, and a rejected compiled negative. See the same
focused local receipt at
`.analysis/unit-replays/gpt-web-survivor-solo-scratch-20261111/receipt.json`.
This improves source semantics without adding new target ownership.

## Yuki solo HP / sprite / final snow schedules (2026-11-12)

The complete 826-byte far-Pascal `yuki_update()` now describes all ten
Boss phases with a source-level choreography surface. Its true HP ladder
starts at 7,900, then installs 4,600, 3,200 and 1,200 as successive phase
end thresholds, before the 0-HP last ring. Its first 64 frames fill HP,
the next 64 frames finish the ready transition, and the second attack
stage has its own 2,000-frame timeout. The two mobile wave counters
terminate at 12 and 24, while the final counter ends at 36; those
existing phase limits are preserved.

Yuki's original idle trio (196, 197, 198), attack trio (204, 205, 206),
B4 ball base 216, arena center (192,96), 16-pixel moving-shadow offset,
64-pixel gather radius and two-angle/eight-point geometry are now named
at their real assignment sites. The first/second pair alternate via the
original parity index; the final five-entry callback table cycles using
`patterns_seen % 5` with the original eight-frame pause. The snow
pattern's initial step, angular origin and signed reverse step remain
8, 0x10 and -8, respectively. All foreign callbacks, actual scratch bytes
and full game ABI are unchanged.

The semantic edit does not invent a new physical field or shorten a
function. The focused native replay
`.analysis/unit-replays/gpt-web-yuki-solo-schedule-a/receipt.json`
compiles the edited large Boss controller in two deterministic Borland
rounds and matches **826/826 original CODE bytes**, including the genuine
20-byte compiler dispatch table and ordered relocations. Its updated
compiled negative lowers the real setup HP gate 4,600→4,500 and is
rejected. Only `main-yuki-update` was replayed; the new comments and
constants add no duplicate acceptance credit to already owned CODE.

## 2026-11-12: exact solo-wave advancement protocol

The full 826-byte Yuki controller now expresses the three repeated wave
reposition completions as `YUKI_NEXT_PATTERN()` (reset phase clock,
advance mode, increment pattern count). The first two attack waves also
share `YUKI_HIT_SCORE_OR_BREAK()`: an unsuccessful shot test exits the
outer Boss phase switch, while a hit awards the existing fixed score.
This preserves the separate first/second/final pattern limits, timeouts,
shadow-boss movements and final defeat logic.

Focused replay `main-yuki-update` at
`.analysis/unit-replays/gpt-web-yuki-solo-wave-protocol-20261112-a/receipt.json`
passed two fresh Borland/TLINK producers with the full **826 original
bytes**, 20-byte compiler switch table and ordered MZ fixups `[256,140]`;
its compiled HP-threshold mutation was rejected. This refreshes the
already accepted source owner, without a second CODE credit.

## 2026-11-13: independent wave clocks, defeat-bonus lifetime and terminal volleys

The three attack counters are **per-wave**, not cumulative. The first wave
starts with `yuki_solo_ring_sweep`, then selects the two-entry bank by the
post-reposition parity and ends at 12 completed attacks. Its
`boss_phase_next(ET_NW_SE, ...)` resets the real `phase_state.patterns_seen`
byte before the second wave begins. The second wave starts with
`yuki_solo_random_rings`, alternates the two-entry random-ring/snow-fan bank,
and ends at 24 completed attacks; its own `boss_phase_next(ET_SW_NE, ...)`
resets the counter again before the final approach. Thus the second wave is
24 patterns, not the 12 remaining values of a cumulative counter.

The final wave begins with one explicit `yuki_solo_snow_cross` callback and a
fresh zero counter. Each completed eight-frame reposition increments that
counter before selecting `yuki_solo_pattern_final[count % 5]`. The first
selection is therefore index 1 (`yuki_solo_vector_stacks`), not index 0; the
snow-cross entry is selected again at counts 5, 10, 15, 20, 25, 30 and 35.
Across the complete 36-pattern final wave this is **eight snow-crosses and
28 vector-stack attacks**, including the initial snow-cross. The final five
entry table's four repeated vector-stack pointers are intentional schedule
weights, not duplicate data to be deduplicated.

The count-timeout and HP-triggered defeats also have different bonus
semantics. `boss_stuff_t::phase_state` overlays `patterns_seen` and
`defeat_bonus` in the same byte at offset 21. On the 36th completed pattern,
the timeout path explicitly writes zero to `patterns_seen` and jumps to the
common defeat label before the HP-gate branch. That leaves `defeat_bonus`
false, so the shared defeat transition does not activate bullet-zap or award
the 50-unit Boss defeat bonus. Only a successful `boss_hittest_shots()` HP
gate reaches the later `defeat_bonus = true` write. The comments beside both
branches now call out this real byte-lifetime distinction; generated code is
unchanged.

The large callback's leaf schedules are now modeled separately as well:

- `yuki_solo_snow_cross` fires four quarter-turn balls at frames 32, 36, 40,
  44, 48, 52, 56, 60 and **64** (36 balls total); the frame-64 volley occurs
  before the signed snow step reverses and reposition begins.
- `yuki_solo_snow_fan` emits five B4 balls at each of frames 32, 64, 96, 128
  and 160 (25 balls total); frame 160 still fires before returning.
- `yuki_solo_vector_stacks` uses frame 24 for setup, then fires on frames
  26..64 every two frames (20 volleys); the terminal frame-64 volley precedes
  the angle-step reversal and reposition.
- The opening ring sweep fires on even frames 50..256 (104 volleys), reverses
  its angular step at frame 160, and still fires on frame 256 before finishing.
  The random-ring leaf fires on frames 16..160 every 16 frames (10 volleys).
  The random-spread leaf performs two fresh RNG draws per even frame 10..256
  (124 volleys); speed and spread are not cached between bullets.
- The speedup leaf is called before the 2,000-frame timeout check, so its
  frame-2,000 special volley is included before the phase transition.

`tests/test_yuki_solo_schedule.py` covers the ten phase selectors, HP ladder,
independent 12/24/36 wave budgets, exact callback sequences, the aliased
HP/time defeat flag, and the inclusive terminal volleys/RNG cadence of the
seven relevant leaf schedules. Run it with
`python3 -m unittest tests.test_yuki_solo_schedule -v`.

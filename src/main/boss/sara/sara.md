TH05 Sara update candidate
==========================

Natural-source provenance is nmlgc/ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`: `th05/boss_1.cpp`
includes `th05/main/boss/b1.cpp`. The complete natural stage-one boss logic
is maintained here: gathering/entrance timing, moving pattern selection,
blue curves, red spreads/stacks/rings, accelerating spirals, the final laser
corridor, HP thresholds, score bonuses, and defeat dispatch. No active ASM,
emits, opcode bodies, ghost helpers, or forced zero/barrier expressions occur.

Original location was found independently of calibration offsets. Eleven
initial function spans had unique masked diagnostic matches, then actual
original calls, the eight existing pattern callback words, and the stage-one
setup callback stores confirmed the entire function closure. Diagnostic
normalization grants no exact credit. The original stage-one setup at 145A7
and 145AD writes the real far update pointer `1527:83FF`, landing at 1D66F.

The complete original contribution is `[0x1D19E,0x1D8BE)`, 1824 bytes:

| Function | Start | Complete bytes |
|---|---:|---:|
| phase_2_with_pattern (static) | 1D19E | 86 |
| pattern_blue_curve_counterclockwise | 1D1F4 | 59 |
| pattern_blue_curve_clockwise | 1D22F | 59 |
| pattern_aimed_red_spread_stack | 1D26A | 60 |
| pattern_red_stacks | 1D2A6 | 78 |
| phase_3_with_pattern (static) | 1D2F4 | 186 |
| pattern_pellet_arcs_at_expanding_random_angles | 1D3AE | 136 |
| pattern_random_red_rings | 1D436 | 63 |
| pattern_accelerating_spirals_clockwise | 1D475 | 106 |
| pattern_accelerating_spirals_counterclockwise | 1D4DF | 106 |
| pattern_dense_spreads_and_random_balls_within_laser_walls | 1D549 | 294 |
| sara_update | 1D66F | 591 |

All complete returns and 73 direct branch destinations were independently
checked against original instructions. The final far-Pascal update ends its
instructions at 1D8B3; the byte there is genuine 00 word alignment. Its
five-word phase switch table is `[1D8B4,1D8BE)`, selected by the original
`CMP BX,4` and `JMP word ptr CS:[BX+8644]`. Each table entry was checked
against a real instruction boundary within the function. Classification is
1813 instruction bytes, 10 semantic compiler-generated CODE-data bytes, and
one uncredited alignment byte. Full raw comparison must include all 1824
bytes. The potential authored-code credit is 1823, conditional on acceptance.

The real owner segment is `B1_UPDATE_TEXT`, group `main_03`, original frame
`0x1527`, group offset `0x7F2E`. Calibration's contribution starts at 181E5
and does not supply original addresses. Near calls to RNG helpers wrap the
16-bit IP: actual offsets are `1527:002C`, `003A`, and `0050`, rather than
the unwrapped linear-looking 2529C/252AA/252C0 disassembly destinations.
The packet masks only the semantic IP to 16 bits when decoding these calls;
it never changes any compared target bytes or fixup order.

Accepted `movement.hpp`, `gather.hpp`, `template.hpp`, and the shared
geometry/resident headers are reused unchanged. Boss24, BulletTemplate14,
gather_template14 and SPPoint4 keep their complete actual definitions.
Missing `.set()` methods are expanded owner-locally into the same typed `.v`
assignments. The original packed spread/stack setters are expressed as
natural owner-local inline uint16/uint32 field bit assignments, over the
actual adjoining fields asserted by `template.hpp`; no replacement class or
byte array is introduced. Sprite constants preserve the actual word enum
domain through PAT_STAGE_last319, PAT_MAX320, and the 7FFF domain bound.

The new `Laser` declaration retains all 24 real bytes: byte flag/color,
10-byte coordinates, word shootout speed, age, grow/moveout age union,
shrink age, byte target width, and the original three-byte unused tail.
The tail exists explicitly in both `laser.hpp` and `lasers[bss].asm`; it is
not invented offset padding. The 32-slot array, template, every offset, and
the actual slot stride are preserved. The 16-byte Sara scratch-state union
likewise retains its original phase views, including genuinely unused
prefix fields, and assertions cover the phase-dependent members.

Source owns no DATA or BSS. Real DS is 209D; important foreign objects are:
the pattern table1F6E, background callback350A, homing SPPoint3F8A, tuning
callback41DE, stage_frame_mod165769, bullet template577E, lasers578C,
laser template5A8C, boss5ABA, gather template9EA6, selected pattern callback
C664, and boss scratch bytesC682. All addresses and actual field references
are in the private packet. The eight callback table words point to the
eight complete shooting functions above and remain foreign data. No score,
bullet, laser, callback table, or gameplay state is redefined by the owner.

Pattern callbacks are two-byte near-cdecl pointers; tuning/background
callbacks are two-byte near-Pascal pointers. `sara_update` is far-Pascal with
no arguments and an actual RETF. Boss, gather, and laser control functions
retain genuine near ABIs in main_03. The first declaration of
`sara_bg_render` is explicitly bound to `BOSS_BG_TEXT main_01`, preserving
its real near word5C07; laser declarations use `LASER_SC_TEXT main_03`.
The real far services are SND_SE_PLAY at `14AB:0232` and SELECT_FOR_RANK at
`0AE1:21A2`. All ten original segment relocations are recorded in order.

Private integration packet: `.analysis/main-sara-boundary-review.json` and
`.analysis/main_sara_bindings.asm`. The wrapper is `th05/boss_1.cpp`, defining
GAME5/BINARYM and including this owner with the usual optimized Borland
large-model MAIN flags. Source is ASCII-compatible UTF-8. The original
`#pragma option -a2` before the final function is retained for its real
semantic switch-table alignment; code segment/group options occur only at
the top of the owner. The context supplies only external labels and address
extents, with no `.stack`, original helper instructions, table contents,
gameplay data, or authored credit for the context.

A meaningful natural negative changes the aimed red spread's stack count
from five to four: `sara_set_spread_stack(5, 0x10, 5, 0.4375f)` to the
same call with a four as its third argument. No ABI or object layout changes.
This packet is source preparation and original boundary review only. Two
fresh focused builds, complete raw bytes, ordered relocation agreement,
OMF integrity, and compiled negative rejection remain required; complete
standalone executable reconstruction remains open.

## Accepted focused replay

`main-sara-a` passes both independent producers, the complete 1,824-byte
contribution, all ten original ordered fixups and the compiled five-to-four
stack-count negative. Accepted authored code is 1,823 bytes: 1,813 instruction
bytes and the ten-byte semantic phase table. The verified zero alignment byte
receives no credit. All twelve complete functions, including static shooting
helpers and the entire update dispatcher, are included. No DATA/BSS or whole
executable equality is claimed.

## Named full-controller phases and pattern dispatch

The original five-entry `sara_update` switch now identifies its three combat
phases as blue/red waves, spinning rings, and the final laser corridor. The
two pattern-wave dispatches retain their genuine random mode selection and
phase-indexed callback table. Named pattern limits (32 and 24), reset mode,
and the final 1,300-frame timeout preserve the observed numeric behavior
while making the full stage-one Boss controller easier to inspect.

## Staged duration and laser-corridor timing (2026-11-11)

The complete 12-function Sara compilation context now names the original
phase-two movement delay decay and phase-three pattern duration escalation.
They are **not clamped**: phase two starts with a 64-frame fly delay and
subtracts 12 while the current value is above 12, allowing its last step
from 16 to 4. Phase three starts with an 80-frame pattern and adds 24 while
below 180, so the final duration may advance from 176 to 200. Neither guard
is a minimum/maximum assignment. The four progressive spin-animation timing
windows have their original 64/96/128/160-frame boundaries.

The final laser corridor still creates its fixed lasers at frame 32 and
activates them at frame 64. Its four slowdown angle thresholds (80h, 60h,
58h and 50h) each advance the existing `laser_angle_interval` field in the
actual phase-four 16-byte scratch view. The random-ball count increases
once every 64 frames until the original count limit of eight. All frame,
angle, speed and phase-state values are preserved; only their source-level
meaning is made explicit.

A focused native replay of `main-sara` compiled the entire **1,824-byte**
original context twice, preserving all twelve complete functions, the
original compiler-generated five-word phase switch table, checked alignment
byte and literal ordered relocations. The existing compiled red-spread
semantic mutation was rejected. Receipt:
`.analysis/unit-replays/gpt-web-sara-flystep-laser-timing-20261111/receipt.json`.
This refines already accepted authored C++ rather than claiming new target
bytes or a whole-MAIN cold replay.

## Attack-cadence and compiler byte-write semantics (2026-11-12)

The complete **1,824-byte / 12-function** Sara Boss source now uses
`projectile_rules.hpp` for its first-wave blue shot clocks, the starting
clockwise/counterclockwise angles and ±10 turn steps, the red-stack
rotation, charge/fire sound events, spin animation frequencies, ring
volley periods, and the terminal laser corridor's color, geometry and
initial per-phase scratch states. The two moving directions are kept
separate from the existing five-way phase switch, rather than merging
independent patterns or changing the original 16-byte phase-state union.
The final corridor still creates its two fixed lasers with symmetric
initial angles and preserves the four named rotation slowdown thresholds.
Original score bonuses and the two original laser-stop slots are likewise
named. All of these constants are gameplay semantics; the actual compiler
emits no new DATA or helper function.

The first native diagnostic emitted **1,806**, not the original 1,824,
because Borland 4.02 changed some byte-wide writebacks when their
literal integer deltas were replaced with enumerator expressions.
Specifically, the clockwise/counterclockwise spiral angle updates
emitted direct memory `ADD` instead of the original AL load/add/store
sequence (three fewer bytes per function); the laser left/right
rotation and spread angle updates likewise lost essential register-form
instructions and changed the later function placements. This is a
compiler-expression/ABI finding, **not** evidence that the shorter
instructions belong to the original binary. Those five delicate
writebacks remain natural original source arithmetic with literal
small integer steps; surrounding timing, color and state semantics
stay named. No dummy operation, branch barrier, instruction payload,
or forced asm is inserted to restore code length.

The corrected scoped replay at
`.analysis/unit-replays/gpt-web-sara-projectile-rules-c/receipt.json`
uses two independent real Borland producers and verifies all
**1,824 original bytes**, including 1,813 instruction bytes, the
10-byte five-way compiler phase table, one checked alignment zero,
and the original literal ordered MZ relocation sites
`[919,813,723,660,382,338,260,36,1427,1157]`.
The compiled actual five-to-four red-spread stack mutation remains
rejected. All twelve source-defined functions share this one complete
accepted scope; no prior accepted bytes receive additional credit.
Yumeko's 283-byte sword updater now also has a fully natural C++ source that
reproduces its complete 2,139-byte original-order context twice; the existing
reviewed ASM owner remains the sole CODE credit.

## 2026-11-12: coherent mobile-wave hit scoring and reposition clocks

The original 1,824-byte twelve-function Sara source now names two shared
mobile-wave rules. `SARA_REPOSITION_AFTER_PATTERN()` resets Sara's current
phase clock and reselects reposition mode at the end of both wave pattern
helpers, while the spinning phase still restores Sara's idle sprite
separately. In the full phase controller,
`SARA_WAVE_HIT_SCORE_OR_BREAK()` retains the shared Boss hit test and
seven-unit pattern score bonus, including the original `break` target in
the outer phase switch. The two original HP-gate transitions, pattern
length evolution and explosion types remain distinct and unchanged.

The **complete 1,824 original bytes** were reproduced by two separate
Borland C++/TLINK producers at
`.analysis/unit-replays/gpt-web-sara-big-wave-arbitration-20261112-a/receipt.json`.
Both real objects preserve the original five-way compiler switch table,
its alignment classification and all ten ordered MZ relocation entries;
the previously accepted compiled red-spread-stack mutation is rejected.
The current acceptance ledger references this updated source, with no
second authored CODE credit or whole-game cold replay.

## Source factoring: native red cloud and fresh random angle draws

The complete original-order 1,824-byte Sara source now shares the genuine
red cloud spawn/sprite initialization between its aimed red spread-stack and
rotating red-stack patterns. The groups, angle calculations, stack geometry,
projectile tuning and sounds remain distinct. The expanding pellet and blue
ball volleys now use one `SARA_FRESH_PELLET_DIRECTION()` expression but still
perform **two separate RNG draws**, one at each original bullet construction
site. No cached/shared random result was introduced.

A focused two-producer Turbo C++/TLINK replay reproduces all 1,824 original
bytes, the real switch-table boundaries and original ordered relocations;
the existing compiled red-spread mutation is rejected. Evidence:
`.analysis/unit-replays/gpt-web-sara-red-cloud-and-angle-draws-b/receipt.json`.
This refreshes an already accepted 12-function Boss context, without
recrediting authored CODE.

## 2026-11-13: explicit phase-view byte overlays

The full 16-byte `sara_state_t` union now asserts every reused field offset,
not just the phase-two delay, phase-three ring speed and phase-four spread
angle. Bytes 9 and 10 are the shared phase-two/three wave clock and previous-
pattern selector. Byte 13 changes from the red-stack angle to the phase-three
ring speed and then the laser rotation interval; byte 14 changes from the
phase-two clockwise angle to the phase-three counterclockwise angle and then
the final random-ball count; byte 15 changes from the opposite phase-two/
phase-three angle roles to the final spread angle.

The complete `main-sara` replay recompiles all twelve functions and preserves
all **1,824 original bytes**, the ten ordered relocations and the five-entry
compiler phase table in two independent Borland/TLINK producers. Its existing
compiled red-stack mutation remains rejected. Receipt:
`.analysis/unit-replays/gpt-web-sara-scratch-offsets-20261113/receipt.json`.
This records the actual lifetime overlay without changing the 16-byte object,
phase transitions or previously accepted code-byte credit.

## 2026-11-13: pattern history crosses the phase-two/three boundary

Sara's `boss_statebyte[10]` is one previous-pattern selector shared by the
blue/red wave and spinning-ring wave views. The entrance transition initializes
it once to `0xFF`, allowing the first selection from the four modes `1..4`.
Every later reposition chooses a new mode from that same range until it differs
from the saved byte, then stores the choice before dispatching the corresponding
row of `SARA_PATTERNS_PHASE_2_3`.

The phase-two timeout does **not** reset this byte: it advances the Boss and
initializes only the phase-three pattern duration. Consequently the first
spinning-ring choice is also prevented from repeating the final blue/red-wave
mode. The two phase-specific `previous_pattern_mode` members are views of the
same physical byte at offset 10, not separate histories. The phase-three
reposition lead remains 16 frames; its four mode indices map to the same
four-column callback row. The final laser corridor reuses bytes 13..15 and does
not consume this prior-pattern value.

The source now names the full mode domain, its exclusive random upper bound,
the `0xFF` no-previous sentinel and the phase-three fly lead, and asserts that
the named four-mode domain matches the actual 2×4 callback table. The complete
12-function, 1,824-byte Sara contribution passed two fresh native Borland/TLINK
producers with every original byte and ordered relocation exact; its existing
five-to-four red-stack negative was rejected. Receipt:
`.analysis/unit-replays/gpt-web-sara-cross-wave-pattern-history-20261113/receipt.json`.
This refines the original attack-selection lifetime without changing its
16-byte Boss scratch arena or adding executable bytes.

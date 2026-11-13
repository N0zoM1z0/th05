# Shinki Boss scratch-byte lifetimes

The Boss owns one original 16-byte `boss_statebyte` arena. The named C++
structures in `scratch.hpp` are complete views of that same storage; they do
not allocate parallel state, reset it at phase boundaries, or imply that a
value survives beyond the callback that owns its lifetime. A phase switch is
not itself a scratch clear.

## Byte 10: wave index / Devil laser latch

The main controller's relative wave index and `pattern_devil()`'s
`devil_lasers_active` latch are the same byte. The Devil callback must leave
the nonzero latch in place so the main controller chooses the correct next
wave. This cross-callback handoff is represented by
`ShinkiWaveOrDevilLaserLatch` in both the phase and Devil views.

## Byte 14: inner-angle / wing-tone / Cheeto-period roles

| Role | Owner and lifetime | Exact source behavior |
| --- | --- | --- |
| Devil inner bullet angle | `pattern_devil()` | Inner symmetric bullet-column angle during the Devil attack |
| Final spiral pellet angle | `pattern_circles_and_alternating_spirals()` | Reinitialized to zero at the spiral arm frame, then advanced by the original pellet-ring step |
| Wing palette tone | `pattern_wing_preparation()` | Initialized to the base tone at wing preparation start, incremented on alternating global frames during the six-laser sweep, then used for the original palette flashes |
| Cheeto-wall interval | `pattern_cheetos_within_spread_walls()` | At frame 128 receives rank-selected 128/48/32/24 and controls the callback's modulo cadence |

These roles share `ShinkiSpiralOrDevilInnerAngle` at physical offset 14.
The wing and Cheeto callbacks use complete 16-byte overlay views with
compile-time offset checks; they do not create separate palette or timer
variables.

## Byte 15: outer-angle / attack-timing roles

| Role | Owner and lifetime | Exact source behavior |
| --- | --- | --- |
| Devil outer bullet angle | `pattern_devil()` | Outer symmetric bullet-column angle during the Devil attack |
| Final spiral red-ring angle | `pattern_circles_and_alternating_spirals()` | Reinitialized to zero with the pellet angle at the spiral arm frame, then advanced by the original red-ring step |
| Curved-ring turn delta | `pattern_curved_rings()` | At attack setup receives the original random positive/negative two-unit turn, then updates the template angle after each volley |
| Dual-speed ring interval | `pattern_dualspeed_rings()` | At attack setup receives rank-selected 16/12/8/4 and controls the two-speed ring cadence |
| Wing animation frame | `pattern_wing_preparation()` | Starts at the first wing frame, triggers the one-time white-wing release, advances the visible-wing animation, and ends after its original eight-frame visibility |
| Aimed B6-ball interval | `pattern_aimed_b6balls_and_symmetric_spreads()` | Initialized at frame 129 to rank-selected 96/32/28/24 and controls aimed-ball cadence |
| Cheeto-wall secondary value | `pattern_cheetos_within_spread_walls()` | At frame 128 stores rank-selected 32/40/48/56. The callback does not read this byte; the original write remains explicit rather than being mistaken for an interval |

All seven names share `ShinkiSpiralOrDevilOuterAngle` at physical offset 15.
The Cheeto secondary byte is intentionally named as an unused stored value;
it is not silently removed or repurposed. The Devil's separate B6-ball
interval remains byte 13 in `ShinkiDevilScratch`, not this byte-15 aimed-ball
interval.

## Other Devil-local bytes

The complete Devil overlay continues to name its own contiguous protocol:
laser direction at 7, inner/outer laser angles at 8/9, the byte-10 activation
latch, bullet direction at 11, bullet-intro flag at 12, and Devil B6-ball
interval at 13. The final two bytes then use the same angle unions described
above. No other physical field or state transition is changed by the overlays.

## Source and replay coverage

The source now uses named union members for all Shinki byte-14/15 roles in the
shared `shinki.cpp` owner, the standalone wing preparation, and the standalone
Cheeto-wall callback. The complete 959-byte far-Pascal Shinki controller, the
802-byte Devil pattern, 386-byte wing transition, 169-byte Cheeto-wall pattern,
and all adjacent accepted pattern/ball owners were replayed in the affected
closure. Thirteen ordinary C++ owners passed two fresh native Borland/TLINK
producers; the wing owner passed its required two-producer TCC `-S` → TASM32
recipe. Full original raw bytes and ordered fixups match, and each replay's
compiled negative is rejected. No already accepted CODE extent is credited
again, and no full MAIN cold replay was run.

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

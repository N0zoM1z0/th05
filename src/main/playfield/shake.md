# Playfield shake candidate

Natural-source provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/playfld.cpp` including
`th04/main/playfld.cpp` with GAME=5. The owner preserves the two inline
direction helpers, signed shake amounts, byte frame phases, two-frame redraw
request and the original GAME5 double left shift. It includes no assembly,
instruction emissions, target arrays, fake helpers or optimization barriers.
The shared canonical `pixel_t` remains unchanged.

The original MAIN range **`[C579,C68A)`**, **273 bytes**, is one complete
`playfield_shake_update_and_render` function, ending in its real near return.
All instructions decode contiguously and all local branches land on observed
instruction starts. There are no CODE-data tables or padding bytes.
Private `.analysis/playfield-shake-boundary-review.json` retains the target
hash, complete extent hash, instruction/branch counts, five ordered original
MZ fixups and original call/global operands. Calibration at load `10287` is
only routing evidence; its near helper address is not the original binding.

Wrapper: `th05/playfld.cpp`; segment `PLAYFLD_TEXT`, group `main_01`, frame
**`0AE1`** / load base **`AE10`**, unit group offset **`1769`**. DGROUP is
**`209D`**. The only near helper is `@tiles_invalidate_all$qv` at original
load **`BD38`**. All EGC helpers use their genuine C Pascal far ABI, five word
arguments and real zero frames:

| Raw symbol | Original frame:offset |
| --- | --- |
| `EGC_SHIFT_DOWN` | `0000:08AA` |
| `EGC_SHIFT_LEFT` | `0000:09B0` |
| `EGC_SHIFT_RIGHT` | `0000:0AB2` |
| `EGC_SHIFT_UP` | `0000:0BC2` |

The zero-valued original segment words still require all five loader fixups.
No helper implementation is supplied by the owner or binding scaffold.

| External object | DGROUP offset | Size |
| --- | --- | ---: |
| `playfield_shake_redraw_time` | `0F4A` | 1 |
| `scroll_line` | `3516` | 2 |
| `playfield_shake_x` | `351C` | 2 |
| `playfield_shake_y` | `351E` | 2 |
| `playfield_shake_anim_time` | `3520` | 2 |
| `stage_frame_mod2` | `5766` | 1 |
| `stage_frame_mod4` | `5767` | 1 |

The contribution owns no initialized DATA or BSS. Its independent symbol-only
scaffold places all origin holes outside the complete 273-byte source body,
preserving original main_01 and DS frames. No stack is allocated by it.

A natural negative control changes the unique `stage_frame_mod4 <= 1`
condition to `stage_frame_mod4 <= 0`, changing the vertical phase of the actual
shake animation. The candidate requires focused cold raw/fixup replay before
any source-current exact acceptance.

## Accepted focused replay

`main-playfield-shake-a` passes both independent producers, all 273 instruction
bytes, the five original ordered far-call fixups and the compiled stage-frame
phase negative. Double left shifting and scroll-dependent clipping match the
original; no helper, DATA or whole-executable credit is added.

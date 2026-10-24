# First-launch setup candidate

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/op/m_setup.cpp` with
GAME=5 and `th04/shiftjis/m_setup.hpp`, wrapper `th05/op_setup.cpp`.
Canonical files are UTF-8 and require explicit **`source_encoding='cp932'`**
staging. The 18 readable Japanese help entries independently match original
CP932-decoded text, including spacing and their shared final help sentence.

The source reuses accepted OP/resident/sound/enum declarations from `menu.hpp`
without editing them. It retains all window animation, selection, input and
palette operations as natural C++. The original unnamed two-word window now
has a local semantic type, preserving both fields and inline methods. The
unused original palette is represented as 16 real RGB triplets with channel
and array views, not an artificial offset spacer. All sizes and field offsets
are asserted. There are no instruction emissions, ASM, ghost helpers, opaque
target byte arrays or optimization barriers.

## Original boundaries

Packed OP SHA-256:
`c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb`.
The independently observed 77,798-byte decoded payload has SHA-256
`7c112a4a7dc4231e9be2d0f69555f0736f69165c80621a3fcd67324dad77ec47`.
All following addresses are decoded load-module offsets, not packed-file offsets.

The complete original range is **`[B077,B616)`**, **1439 bytes**, SHA-256
`7af2790f2c5df5416d7daf11ded1084384b3eae01035fbe1e44152ec30fe8c4c`.

| Function | Original half-open span | Instruction bytes |
| --- | --- | ---: |
| `window_dropdown_put` | `B077..B0F1` | 122 |
| `window_rollup_put` | `B0F1..B14A` | 89 |
| `dropdown` | `B14A..B1BA` | 112 |
| `singleline` | `B1BA..B234` | 122 |
| `rollup` | `B234..B270` | 60 |
| `bgm_choice_put` | `B270..B2BF` | 79 |
| `se_choice_put` | `B2BF..B310` | 81 |
| `bgm_help_put` | `B310..B33E` | 46 |
| `se_help_put` | `B33E..B36C` | 46 |
| `setup_bgm_menu` | `B36C..B489` | 285 |
| `setup_se_menu` | `B489..B5A6` | 285 |
| `setup_menu` | `B5A6..B616` | 112 |

All **512 instructions** decode contiguously through the original returns;
all **53** local branch destinations are instruction starts. The small semantic
switches compile as branches, with no embedded CODE tables or padding.
The original ordered code fixup list contains **45** far-call segment words.
Raw/fixup equality must cover the entire 1439-byte extent.

## Source-owned data and real frames

Use wrapper `th05/op_setup.cpp` including `src/op/setup/setup.cpp`, the OP
build context (`BINARY='O'`), `OP_SETUP_TEXT` / `op_01`. The original frame is
**`0A39`**, load base **`A390`**, contribution group offset **`0CE7`**.
This odd start is genuine; do not insert alignment before the compiler body.
DGROUP frame is **`0EFE`**. No additional `.stack` belongs in this bounded
context.

Initialized DATA is **DGROUP `[0AB6,0EE9)`**, **1075 bytes**, SHA-256
`a96eee90cdf88b7b51ec331b5fd4f06c8f8c10c3ebc9073018ca782917b267d4`.
It contains two real mutable nine-element far-pointer tables, `_BGM_HELP` at
`0AB6` and `_SE_HELP` at `0ADA` (**72 bytes**), and **1003 bytes** of 27 natural
terminated strings: 17 unique help lines, six choices, two captions and two
filenames. The final SE help line shares the existing BGM line via the
compiler's ordinary string pooling. Source data contains no manually copied
pointer values. Its **18** segment-word fixups must be checked independently.
There is no DATA padding in this extent.

Source-owned BSS is **DGROUP `[3F20,3F54)`**, **52 bytes**: the reference's
unused palette at `3F20` (48) and `_window` at `3F50` (4; signed tile width and
height words). There is no internal BSS alignment gap. Unused-palette origin is
reference-inferred; no BSS authored credit is requested. Do not provide any of
these compiler-owned objects in the binder.

The only external globals are `_resident` at DGROUP:`2DEC` (real far pointer,
4 bytes), `_key_det` at `3A92` (2) and `_PaletteTone` at `054E` (2).
All 15 external callees are far:

| Actual symbol | Original frame:offset |
| --- | --- |
| `@EGC_COPY_RECT_1_TO_0_16$QIIII` | `0D30:0FD8` |
| `SUPER_PUT` | `0000:292A` |
| `@FRAME_DELAY$QI` | `0D30:0E5E` |
| `GRAPH_PUTSA_FX` | `0D30:0136` |
| `@INPUT_WAIT_FOR_CHANGE$QI` | `0D30:0DA4` |
| `PALETTE_SHOW` | `0000:19F0` |
| `SUPER_ENTRY_BFNT` | `0000:2656` |
| `@PI_LOAD$QINXC` | `0D30:0AD8` |
| `@PI_PALETTE_APPLY$QI` | `0D30:0BBA` |
| `@PI_PUT_8$QIII` | `0D30:0B0A` |
| `@PI_FREE$QI` | `0D30:0BE0` |
| `GRAPH_COPY_PAGE` | `0000:1250` |
| `PALETTE_BLACK_IN` | `0000:0600` |
| `PALETTE_BLACK_OUT` | `0000:0644` |
| `SUPER_FREE` | `0000:24F2` |

They retain Pascal cleanup, original C/C++ linkage and actual return types.
All other calls are internal to this owner. Window animation callbacks are
genuine near Pascal pointers to local two-word functions, folded naturally by
the compiler at the known call sites.

Private `.analysis/op-setup-boundary-review.json` includes target/view hashes,
all function/call/global sites, pointer-table entries, semantic strings and
ordered code/DATA fixups. `.analysis/op_setup_bindings.asm` is a reviewable
symbol-only binder with no `.stack`, instructions, target string/data copies,
or labels inside source-owned extents. Both are unbuilt candidates.

A natural negative control changes the unique
`DROP_SPEED = (MSWIN_H / 2)` to `(MSWIN_H / 4)`, altering real animation speed.
No source-current exact acceptance or packed-container equality is claimed.

## Accepted focused replay

`op-setup-menu-a` passes two independent producers, all 1,439 CODE bytes /
12 complete functions, 45 ordered fixups, and the compiled animation mutation.
The separately observed 1,075 initialized DATA bytes / 18 fixups also match
both producers but add no progress credit. BSS remains layout evidence only.

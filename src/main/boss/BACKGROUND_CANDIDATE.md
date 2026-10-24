# Boss background reconstruction scopes

`background.cpp` adapts natural C++ from nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/boss/render.cpp` (wrapper `th05/boss_bg.cpp`). Its owner header
localizes the real rendering interfaces, particle/line layouts and semantic
entrance-transition macros. Existing `movement.hpp` supplies the single Boss
and geometry definitions. No accepted source or header is expanded or replaced.

The unavailable geometry convenience methods are expressed as their original
Q12.4 `.v` assignments and shifts. Screen conversion retains signed arithmetic
right shifts and the real playfield origin. The dead-particle sentinel remains
`-999 * 16`. All particle and line arrays describe actual program state; none
contains target bytes or instruction/table data.

There are no emitted instructions, handwritten compiler bodies, fabricated
external zero objects or optimization barriers. The one reference `keep_0(0)`
is replaced by **`static_cast<int>(0)`**. This is a candidate with a known
code-generation risk: original load offset `10D20` contains `CMP AX,0` for the
signed top clip, while ordinary zero optimizes to OR AX,AX. The complete source
is retained even if that function needs further legitimate investigation.

## Original extent

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The complete original contribution occupies **`[10A17,116CD)`**, **3254 bytes**,
SHA-256 `710d93b6d3c166eab778fee87b850df5ddad2132369c0bc04332facfaea3e4b4`.
All addresses here are hexadecimal MZ load-module offsets; the file header is
4032 bytes. A unique first-function diagnostic located it, followed by direct
inspection of original instruction widths, returns, call targets and branches.
Calibration symbols supply names, not exact-acceptance evidence.

| Function | Original half-open span | Bytes |
| --- | --- | ---: |
| `sara_bg_render` | `10A17..10A7F` | 104 |
| `louise_bg_render` | `10A7F..10B0B` | 140 |
| `alice_bg_render` | `10B0B..10B97` | 140 |
| `mai_yuki_bg_render` | `10B97..10C29` | 146 |
| `yumeko_bg_render` | `10C29..10CB2` | 137 |
| `shinki_bg_particles_render` | `10CB2..10D51` | 159 |
| `shinki_bg_type_a_update_part1` | `10D51..10E83` | 306 |
| `grcg_lineset_line_put` | `10E83..10F23` | 160 |
| `shinki_lineset_forward_copy` | `10F23..10F6D` | 74 |
| `shinki_bg_type_a_update_and_render` | `10F6D..1101F` | 178 |
| `shinki_bg_type_b_update_part1` | `1101F..110FF` | 224 |
| `shinki_bg_type_b_update_and_render` | `110FF..11218` | 281 |
| `shinki_bg_type_c_update_part1` | `11218..11264` | 76 |
| `shinki_bg_type_c_update_and_render` | `11264..113B0` | 332 |
| `shinki_bg_type_d_update` | `113B0..11411` | 97 |
| `shinki_bg_render` | `11411..114BE` | 173 |
| `exalice_grcg_hexagram_put` | `114BE..1158A` | 204 |
| `exalice_hexagrams_update_and_render` | `1158A..11666` | 220 |
| `exalice_bg_render` | `11666..116CD` | 103 |

All **1190 instructions / 3254 bytes** decode contiguously. Every function ends
with its true return; earlier branch returns remain inside its extent. All 157
local jump destinations land on observed instruction boundaries. There is no
embedded CODE-data, switch table, zero-padding or NOP-padding range in this
contribution. The original ordered MZ fixup list contains **21 segment words**
for far calls. Their positions and values are retained in private target-only
`.analysis/boss-background-boundary-review.json` alongside call sites and
function boundaries. This file is diagnostic, not an acceptance receipt.

## Build and call frames

Wrapper: `th05/boss_bg.cpp` includes `src/main/boss/background.cpp`. Use existing
MAIN flags `-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`. The owner sets
`BOSS_BG_TEXT` in `main_01`. Original main_01 frame: relative segment **`0AE1`**,
load base **`AE10`**; contribution group offset **`5C07`**. Original DGROUP frame:
relative segment **`209D`**. These are actual group frames, not per-function
segments or globally established layout ownership.

All owner helpers are near. The seven boss entry callbacks and
`grcg_lineset_line_put(lineset_t near&,int)`,
`shinki_lineset_forward_copy(lineset_t near&)`, and
`exalice_grcg_hexagram_put(int,int)` use Pascal order/cleanup. The other local
helpers use C++ C order. Particle/line pointers and references explicitly retain
their two-byte near representation. Register-bound blitting retains AX=top,
CX=left and ES=`A800`, with `<dos.h>` providing the genuine compiler registers.

| Near external symbol | Original load destination |
| --- | --- |
| `@BOSS_BACKDROP_RENDER$QIIUC` | `109F0` |
| `@TILES_BB_INVALIDATE_RAW$QI` | `F9EC` |
| `@TILES_REDRAW_INVALIDATED$QV` | `BDAE` |
| `@TILES_RENDER_ALL$QV` | `BBEC` |
| `@TILES_RENDER$QV` | `BD4E` |
| `@grcg_setmode_tdw$qv` | `C1FE` |
| `@grcg_setcolor_direct_raw$qv` | `C204` |
| `@LOUISE_BACKDROP_COLORFILL$QV` | `14AAA` |
| `@TILES_BB_PUT_RAW$QI` | `F968` |
| `@ALICE_BACKDROP_COLORFILL$QV` | `C41E` |
| `@MAI_YUKI_BACKDROP_COLORFILL$QV` | `BF24` |
| `@YUMEKO_BACKDROP_COLORFILL$QV` | `C42C` |
| `Z_SUPER_ROLL_PUT_16X16_MONO_RAW` | `C21E` |
| `@randring1_next16$qv` | `C700` |
| `@RANDRING1_NEXT16_AND$QUI` | `C70E` |
| `@grcg_setmode_rmw$qv` | `C1F8` |
| `@RANDRING1_NEXT16_MOD$QUI` | `C724` |
| `@boss_bg_fill_col_0$qv` | `C6A4` |
| `@shinki_bg_type_d_colorfill$qv` | `C6C6` |

The `MAI_YUKI` function has an alias at the same numeric destination in the
calibration MAP; its EXTDEF establishes the requested symbol spelling.

| Far external symbol | Original frame:offset | Load destination | ABI |
| --- | --- | --- | --- |
| `CDG_PUT_NOALPHA_8` | `14AB:01C0` | `14C70` | C Pascal far, 3 words |
| `VECTOR2_AT` | `14AB:03B0` | `14E60` | C Pascal far; first argument true SPPoint near reference, then 4 words |
| `GRCG_LINE` | `0000:1716` | `1716` | C Pascal far, 4 words |
| `GRCG_SETCOLOR` | `0000:1A88` | `1A88` | C Pascal far, 2 words |
| `GRCG_CIRCLE` | `0000:10AE` | `10AE` | C Pascal far, 3 words |

The frame words above are the original pre-load MZ values and require the
original fixups, including zero-valued frame words. Far return/cleanup and near
reference widths must remain real, even where a numeric load destination would
also fit a near call.

## Complete data ABI

`boss_particle_t` is 16 bytes: PlayfieldPoint position at 0, origin at 4,
SPPoint velocity at 8, signed age word at 12, byte angle at 14, byte sprite at
15. `lineset_t` is 142 bytes: 20 SPPoint centers at 0, Subpixel Y velocity at
80, 20 Subpixel radii at 82, 20 byte angles at 122. Owner assertions check every
field, complete sizes, near pointer widths and segment-only pointer width.
Existing assertions continue to check all 24 bytes of boss_stuff_t.

All offsets below are original **DGROUP-relative** offsets. Pointer globals
hold the real segment-only allocation handles, not far address substitutes.

| Data object | Offset | Size | Type |
| --- | --- | ---: | --- |
| `boss` | `5ABA` | 24 | existing boss_stuff_t; phase +15, phase_frame +16 |
| `boss_particles` | `4684` | 1024 | boss_particle_t[64] |
| `linesets` | `444C` | 568 | lineset_t[4] |
| `drawpoint` | `36FE` | 4 | PlayfieldPoint |
| `tri_point_1` | `443C` | 4 | SPPoint |
| `tri_point_2` | `4440` | 4 | SPPoint |
| `tiles_bb_col` | `4444` | 1 | unsigned char |
| `tiles_bb_seg` | `4448` | 2 | bb_tiles8_t __seg * |
| `bb_boss_seg` | `C692` | 2 | bb_tiles8_t __seg * |
| `shinki_bg_linesets_zoomed_out` | `1988` | 1 | unsigned char |
| `shinki_bg_type_a_particles_alive` | `198A` | 2 | int |
| `shinki_bg_type_b_initialized` | `198C` | 1 | bool / unsigned char |
| `shinki_bg_spinline_frame` | `198E` | 2 | unsigned int |
| `shinki_bg_type_c_initialized` | `1990` | 1 | bool / unsigned char |
| `shinki_bg_type_d_initialized` | `1991` | 1 | bool / unsigned char |
| `hexagrams_flag` | `1992` | 1 | local hexagrams_flag_t enum, size asserted |
| `stage_frame_mod2` | `5766` | 1 | unsigned char |
| `stage_frame_mod4` | `5767` | 1 | unsigned char |

Direct global operands and pointer immediates independently establish these
locations; scalar/field widths and array strides agree with the declared ABI.
This declares the complete source types without claiming those data bytes as
reconstructed ownership.

A natural negative-control candidate changes the unique
`static const int SHINKI_LINESET_COUNT = 2;` to 1, altering actual loop limits
and line-set behavior. For a smaller single-function control, change the
particle Y reset `particle->age = 0;` to 1 only within
`shinki_bg_particles_render` (the same text also occurs in type-A initialization,
so scope that mutation to the function).

## Accepted functions and exclusions

Seventeen complete functions, totaling **2891 instruction bytes**, pass two
fresh producers and the compiled entrance-timing mutation in
`.analysis/unit-replays/boss-background-functions-a`. Acceptance explicitly
selects the passing functions from the intact mixed-result receipt, retaining
its original aggregate-failure verdict and digest. Every saved producer,
function boundary, raw extent, ordered fixup list and source dependency is
independently rechecked. Unchanged earlier units are not rebuilt.

Two original complete functions remain unaccepted:

- `shinki_bg_particles_render`: original 159 bytes, natural C++ output 158.
  The signed-zero comparison emits OR AX,AX in place of CMP AX,0.
- `exalice_grcg_hexagram_put`: all 204 raw bytes match, but splitting the compiler
  contribution moves a LEDATA boundary through this function and changes the
  order of its seven MZ relocation sites. The strict oracle rejects it.

The owner uses two real compiler CODE contributions in the same `main_01`
group. `BOSS_BG_TEXT` contains the first five callbacks and the unaccepted
particle renderer: 825 actual compiler bytes at `[10A17,10D50)`.
`BOSS_BG_AFTER_TEXT` contains the remaining functions: 2428 actual compiler bytes
at `[10D51,116CD)`. A single ORG hole `[10D50,10D51)` belongs to symbol-only
link context, outside every compiler function. It receives no credit and does
not repair or accept the particle renderer. Every accepted function retains
its complete original position and ordered raw/fixup proof.

The earlier monolithic diagnostic `.analysis/compiler-probes/boss-bg-c` compiled
3253 natural bytes and found ten raw/fixup matches before the split. It is a
routing observation, not the current acceptance producer. The standalone
`diagnose_boss_background.py` intentionally handles that monolithic candidate
shape; the current split owner is replayed through `replay_units.py`.

Natural random-range helpers preserve separate float-to-subpixel and signed
range inline layers. Introducing local min/max temporaries prevented this
compiler from folding branches and grew one function by 46 bytes; restoring
the semantic helper layering removed that discrepancy. Redundant same-name
header segment pragmas are omitted so declarations do not create duplicate
compiler contributions. No accepted shared header is changed.

Whole-background and whole-program equality remain open.

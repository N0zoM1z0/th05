# MAIN HUD overlay candidate

This owner adapts the natural C++ implementation in nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/main/hud/overlay.cpp`,
selected for TH05. It contains no emitted instruction bytes, inline assembly,
fake linker-zero symbols or game asset arrays. Glyph strings, title buffers and
the resident are external declarations. `resident.hpp` declares the complete
128-byte TH05 resident layout; unread fields remain corroborated ABI hypotheses.
The producer accesses `demo_num` at byte 31 through the real far resident pointer.
Existing accepted source and shared geometry/ABI headers are unchanged.

Use wrapper `th05/hud_ovrl.cpp` including `src/main/hud/overlay.cpp`, with the
existing MAIN flags `-O -b- -3 -Z -d -DGAME=5 -ml -DBINARY='M'`. The source
selects segment `HUD_OVRL_TEXT`, group `main_01`. The only system headers are
the pinned compiler's `string.h` and `dos.h`.

## Target and boundaries

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Offsets here are relative to its MZ load module, whose file header is 4032 bytes.
The complete contribution is `[0x11D50,0x1245E)`, **1806 bytes**, with no NOP
exclusions. Its target extent SHA-256 is
`39912b57fc67d34a0f9929c456c4087f2e1590903d84fe9bde8cc46df88212ae`.

| Function | Target load offset | Complete bytes |
| --- | --- | ---: |
| `overlay_wipe` | `0x11D50` | 34 |
| `overlay_black` | `0x11D72` | 33 |
| `overlay_stage_enter_update_and_render` | `0x11D93` | 157 |
| `overlay_stage_leave_update_and_render` | `0x11E30` | 108 |
| `dissolve_put` | `0x11E9C` | 72 |
| `overlay_titles_invalidate` | `0x11EE4` | 73 |
| `overlay_titles_update_and_render` | `0x11F2D` | 525 |
| `overlay_boss_bgm_update_and_render` | `0x1213A` | 303 |
| `overlay_popup_update_and_render` | `0x12269` | 501 |

The masked routing survey identifies a unique shape; it is not exact evidence.
Independent reading of original bytes confirms the contiguous instruction
streams and final returns. Numeric references below are target observations;
symbol names and type roles are corroborated by candidate source.

## Link context

The original `main_01` frame is relative segment `0AE1` (load offset `AE10`).
This contribution starts at group offset `6F40`. Unlike a producer containing
only relative calls, this unit assigns its own function addresses to near
callbacks: the original `overlay_titles_update_and_render` value is `711D`.
A bounded scaffold must preserve these original group-relative offsets; raw
near-call displacements alone do not establish callback correctness or layout.
DS uses the previously observed DGROUP-relative segment `209D`.

| External function | Target destination | ABI |
| --- | --- | --- |
| `_strlen` | `0000:684D` | far C, real far string pointer |
| `GAIJI_PUTCA` | `0000:1D7A` | far Pascal, four words |
| `GAIJI_PUTSA` | `0000:1DBE` | far Pascal, two words + far pointer + word |
| `TEXT_PUTCA` | `0000:2540` | far Pascal, four words |
| `TEXT_PUTSA` | `0000:2598` | far Pascal, two words + far pointer + word |
| `@grcg_setmode_rmw$qv` | load `C1F8`, main_01:`13E8` | near C++ |
| `@grcg_setcolor_direct_raw$qv` | load `C204`, main_01:`13F4` | near C++; color in AH |
| `@bb_txt_put_8_raw$quiui` | load `E51A`, main_01:`370A` | near fastcall; sprite in CX |
| `NULLFUNC_NEAR` | load `C73E`, main_01:`192E` | near Pascal callback target |
| `SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1` | load `DF28`, main_01:`3118` | near Pascal, word parameter |
| `TILES_INVALIDATE_AROUND` | load `BAD2`, main_01:`0CC2` | near Pascal, Y then X words |
| `@HUD_POINTS_PUT$QUIUIUL` | `1527:0654`, load `158C4` | far Pascal, two words + unsigned long |

The function-pointer and data-pointer widths are deliberate ABI inputs. Do not
replace the near callbacks or far strings with host-model pointer defaults.

## External data bindings

All following values are DS-relative offsets, not owned data contributions.
Only external declarations are checked in; glyph/message bytes are not imported.

| Symbol | DS offset | View used by this producer |
| --- | --- | --- |
| `_resident` | `41FC` | far pointer to complete resident_t |
| `_tile_invalidate_box` | `3502` | two signed words |
| `_overlay1` | `4ABE` | near callback |
| `_overlay2` | `4AC0` | near callback |
| `_overlay_popup_id_new` | `4ABD` | byte enum |
| `_overlay_popup_bonus` | `4AC4` | unsigned long |
| `_stage_title` | `4AC8` | far string pointer |
| `_stage_bgm_title` | `4ACC` | far string pointer |
| `_boss_bgm_title` | `4AD0` | far string pointer |
| `_stage_id` | `576E` | byte |
| `_overlay_fade` | `19AC` | one-byte union |
| `_boss_bgm_frame` | `19AD` | byte |
| `_popup_frame` | `19AE` | byte |
| `_gStage_1` | `19B2` | eight byte glyph IDs |
| `_gFINAL_STAGE` | `19BA` | twelve byte glyph IDs |
| `_gEXTRA_STAGE` | `19C6` | twelve byte glyph IDs |
| `_POPUP_STRINGS` | `19FA` | array of real far glyph-string pointers |
| `_dissolve_sprite` | `1A0E` | byte |
| `_stage_title_len` | `4AA0` | signed word |
| `_stage_bgm_title_len` | `4AA2` | signed word |
| `_boss_bgm_title_len` | `4AA4` | signed word |
| `_titles_frame` | `4AC2` | byte |
| `_PLAYFIELD_BLANK_ROW` | `1A10` | far pointer to external string |
| `_gDEMO_PLAY` | `1A14` | ten byte glyph IDs |
| `_popup_gaiji_len` | `4AA6` | signed word |
| `_popup_id_cur` | `4AA8` | byte enum |
| `_popup_dest_reached` | `4AA9` | byte boolean |
| `_popup_shiftbuf` | `4AAA` | nine byte glyph IDs |
| `_popup_cur_tram_left` | `4AB8` | signed word |
| `_popup_dest_tram_left` | `4ABA` | signed word |

The original MZ relocation table yields this **ordered** relative site list:

```text
35A,343,32D,310,2B8,2A8,138,C8,83,38,17,
706,6EF,6D2,6AC,686,660,5E4,592,551,53E,4BD,4A6,47A
```

All values are hexadecimal. Sorting that list would discard a comparison
dimension. Source, compiler/OMF, full raw bytes, group/callback bindings and the
complete relocation list still require focused cold replay. No new exactness,
whole-game layout or external data ownership is asserted by this source packet.

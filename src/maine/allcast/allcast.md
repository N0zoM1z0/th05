# MAINE all-cast

Natural source is adapted from pinned nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/end/allcast.cpp`.
The owner preserves all three complete functions, their original definition
order, eight-slot screen count (including the reference's final null-filename
load quirk), page flips, picture masks, two-measure cues, fallback beat timing,
seven screen advances and final fades. Hardware page and GRCG mode writes use
the real DOS port intrinsics. There is no ASM, instruction emission, target
array, artificial zero object or substitute helper implementation.

The original decoded contribution is `[B273,B4D6)`, **611 instruction bytes**,
198 instructions, three complete functions and 23 ordered MZ segment fixups.
There are no compiler tables or padding bytes. Private
`.analysis/maine-allcast-boundary-review.json` records the original operand
sites, hashes, boundaries and ordered fixups. Reference calibration is routing
evidence only; no source-current compiler producer has run for this owner.

| Function | Original decoded span | Bytes | Actual reference MAP symbol |
| --- | --- | ---: | --- |
| `screen_fadeout_animate_and_advance` | `B273..B37C` | 265 | `screen_fadeout_animate_and_advan(int,int)` |
| `wait_flip_and_check_measure_target` | `B37C..B3CB` | 79 | `wait_flip_and_check_measure_targ()` |
| `allcast_animate` | `B3CB..B4D6` | 267 | `allcast_animate()` |

The long names are the actual compiler's identifier truncation, not renamed
source functions. A full contribution candidate uses wrapper `th05/allcast.cpp`,
segment `MAINE_01_TEXT`, `wrapper_options = "-zPgroup_01"`, MAINE binary E,
`target_start = 0xb273`, `size = 611`, `functions = 3`,
`alignment_offsets = []`, and the independent symbol-only
`probes/units/maine_allcast_bindings.asm`. Canonical source is UTF-8 and contains
no compiled Japanese literals; either the default raw staging or explicit
CP932 staging must retain its genuine producer identity consistently.

Original group frame is `0A54`, with this contribution at offset `0D33`.
The genuine external near `screen_line_next_animate()` is `0A54:0C75`.
All 13 far helpers use their actual original frames/offsets: master helpers
use frame zero, shared helpers use `0E80` (not calibration `0E7F`). The binder
contains labels and holes outside the complete compiler contribution only.
`ALLCAST_CODE_SIZE` defaults to the observed reference size 611; a diagnostic
may override it from an actual OMF CODE size before placing the foreign tail.
It must not pad or shorten a compiler-owned function to fit this expectation.

The source owns no initialized DATA. Its six genuine state objects occupy
**11 BSS bytes**, DGROUP `[4F0E,4F19)`: five signed words and the static byte
player-character index. Their touched original operands and the reference
OMF BSS contribution corroborate these positions. The binder places external
DS labels and the hole before this BSS; it does not duplicate those objects.
DS is the original `1011`, versus calibration `1010`. BSS is beyond stored
decoded payload bytes and receives no stored-byte acceptance claim. Foreign
filename/quarter arrays, current page, resident pointer and `EXED` string remain
external real objects, with no content copied into this owner or scaffold.

A prospective natural negative control can change `measure_target += 30;`
to `measure_target += 29;`, changing the real between-screen musical delay.
It must be applied only to a staged negative source, compiled and rejected by
the full contribution or the complete screen-fade function. No acceptance,
whole-executable layout or packed-file exactness is claimed here.

## Accepted focused replay

`maine-allcast-a` passes two independent producers, all 611 instruction bytes /
three functions and 23 ordered segment fixups. The compiled between-screen
measure-delay mutation from 30 to 29 is rejected. The BSS layout observation
and external arrays remain uncredited.

## Actual EXED music-provider linkage and ending tempo semantics (2026-11-12)

The complete **611-byte** three-function All Cast ending controller now
uses the **real exported C public** `EXED[5]` from its separately accepted
MAINE source-owned file-name object at `[115F9,115FE)`. `allcast.hpp`
declares it under the appropriate `extern "C"` context; the previous
function-local `extern const char EXED[]` placeholder was removed.
The original `snd_load(EXED, SND_LOAD_SONG)` call is unchanged. This
corrects source-level cross-translation-unit ownership rather than
inserting a replacement song, provider code or encoded pointer bytes.

The same controller names its actual two-measure introductory wait,
original two-frame page-flipping delay, and 22-half-frame fallback
measure divisor, preserving the existing ZUN-specific tempo quirk and
the between-screen 30-measure advance. The original graphics page
order, four-stage PI masked transitions, palette fade and resident
selection remain in exactly the same order and ABI; no extra BSS or
runtime timer is allocated. The short strings and symbol definitions
are not embedded into the controller's CODE scope.

Changing the shared header affects both `maine-allcast` (**611 bytes**)
and `maine-allcast-line` (**190 bytes**), so each was independently
replayed with two native Borland/TLINK producers and its own compiled
semantic negative. Full original bytes, true MAP/OMF extents and
ordered MZ fixups remain exact:

- `.analysis/unit-replays/gpt-web-maine-allcast-music-consumer-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-allcast-line-after-song-a/receipt.json`

These functions were already accepted; neither CODE extent is
recredited, and no unrelated MAINE or full executable replay was run.

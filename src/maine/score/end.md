TH05 MAINE score file lifecycle candidate
=========================================

Natural-source provenance is nmlgc/ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`: `th05/hi_end.cpp` selects
`th04/hiscore/end.cpp`, composed of the score recreation, load-for-character,
and save implementations. TH04's maintained `src/maine/score/scoregen.inl`,
`load_for.inl`, and `hisave.inl` were consulted for semantic reuse. Their
TH04-specific row count, section size, character count, and separate seek
logic do not transfer to TH05. This owner selects the genuine GAME5/BINARYE
branches and preserves TH05's actual algorithms and file behavior.

The three original complete functions are:

| Function | Decoded load interval | Size |
|---|---|---:|
| scoredat_recreate | B590..B646 | 182 |
| hiscore_scoredat_load_for(int) | B646..B6A3 | 93 |
| hiscore_scoredat_save | B6A3..B730 | 141 |

The full `[0xB590,0xB730)` contribution is 416 instruction bytes with 16
original segment relocations, no switch tables, and no padding. All terminal
returns and fourteen direct branch targets were checked against original
instructions. Real near-code frame is `0xA54`, group offset `0x1050`, segment
`SCORE_TEXT`, group `GROUP_01`. Module wrapper is `th05/hi_end.cpp`, using
GAME5/BINARYE and the accepted optimized Borland large-model MAINE flags.
Only the initial owner option pragma occurs before includes.

The existing TH05 `scoredat_t` and `scoredat_section_t` definitions are reused
read-only from `src/op/hiscore/view.hpp`, together with the actual canonical
resident types and complete rank/player-character enum domains. Their data
ABI is shared across the two binaries: five nine-byte names at payload 0,
five eight-byte scores at 45, stage bytes at 85, clear flag at 90, real unused
byte at 91; a section adds two byte keys and the word checksum, totaling 96.
The canonical assertions cover every member offset and physical size. The
MAINE load argument is genuinely `playchar2` (a word `int`), despite the
global player-character enum occupying one byte. Its bool return is one byte
and the near-Pascal function removes its two-byte argument. The other two
own functions are near-cdecl with no arguments.

Recreation fills five default rows, uses the TH05 score digit position six,
and preserves the original decreasing stage sequence `gb_6 - i`, including
its Extra Stage quirk. It writes twenty sections (five ranks times four
characters). The load helper reads one section at
`((playchar * RANK_COUNT) + rank) * sizeof(scoredat_section_t)`, checks it,
and recreates defaults on missing/corrupt input. Save writes the selected
section and then re-keys all twenty sections through the genuine codec APIs.

This owner defines no initialized DATA or BSS. The real foreign score section
`hi` is at DS `0x4F1A`, rank at `0x5077`, player character at `0x5078`.
These are logical BSS addresses beyond the stored decoded payload; original
operands anchor the addresses and fields, without a BSS-content claim.
Four distinct foreign const arrays, rather than pointer aliases or local
coalesced literals, supply the filename: `SCOREDAT_FN` at DS `0x1524`,
`SCOREDAT_FN_0` at `0x152F`, `SCOREDAT_FN_1` at `0x153A`, and
`SCOREDAT_FN_2` at `0x1545`. Each contains `GENSOU.SCR` including its
terminator, eleven bytes, independently checked in the original payload.
The OP literal macro is undefined locally so all four genuine array symbols
are retained. The binder supplies their addresses without defining values.

The original DGROUP frame is **0x1011**, proved by these immediate offsets
and their actual stored filename locations. Calibration uses 0x1010 and is
only routing evidence; its DS must not be transferred. File helpers are
external C far-Pascal at their actual frame-zero destinations.

The two codecs remain foreign and uncredited: decode is the complete
86-byte function `[0xB4D6,0xB52C)`, `0xA54:0x0F96`; encode is the
100-byte function `[0xB52C,0xB590)`, `0xA54:0x0FEC`. Their real ABI is
no-argument near-Pascal, returning a checksum-delta byte for decode and void
for encode. Both pinned reference and maintained TH04 implementations use
an active byte-ROR assembly primitive, visible in the original at B4EA and
B580. No codec assembly body or substitute helper is supplied here.

The actual TC4 `stdlib.h` does declare `_crotr`; API availability alone does
not prove intrinsic code generation. Root's retained diagnostic
`.analysis/compiler-probes/byte-rotate-a/rotate.asm` shows a far library call
for `_crotr(value, 3)`, and MOV/SAR/SHL/OR for the ordinary shift/or expression.
Neither is an observed exact pure C++ replacement for the original byte ROR.
The codec functions therefore stay outside this candidate's authored claim.

Private packet: `.analysis/maine-score-end-boundary-review.json` and
`.analysis/maine_score_end_bindings.asm`. The context contains external labels
and address extents only, with no `.stack`, codec/file helper bodies, score
data, or filename values. New owner files are ASCII-compatible UTF-8;
explicit CP932 staging is recommended because the reused canonical header
transitively includes readable Japanese OP macro definitions.

A natural negative control changes default stages from `gb_6 - i` to
`gb_5 - i` in `scoredat_recreate`. This changes a real default score-record
value without any ABI or layout change. No heavy build, reconstruction
raw-byte comparison, acceptance, or standalone-game claim is performed by
this packet; two fresh focused builds, ordered fixups, OMF validation, and
compiled negative rejection remain necessary.

## Accepted focused replay

`maine-score-end-b` passes two independent CP932-staged producers, all 416
instruction bytes / three functions and 16 ordered fixups. The compiled default
stage mutation from `gb_6-i` to `gb_5-i` changes real recreated scores and is
rejected. The first diagnostic compile lacked the actual `file_append` API
declaration; adding its genuine far Pascal declaration preceded the successful
replay. The codec functions remain external and uncredited.

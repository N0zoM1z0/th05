# Game-adapted color tiny renderers

These two complete MAIN procedures remain distinct from the accepted
monochrome 16x16 worker at C21E and the Cheeto mask worker at DE72.

| Procedure | Complete load scope | Compared | Instructions | Alignment offsets |
| --- | --- | ---: | ---: | --- |
| `Z_SUPER_ROLL_PUT_TINY_32X32_RAW` | BF62..C07C | 282 | 278 | 85, 131, 173, 223 |
| `Z_SUPER_ROLL_PUT_TINY_16X16_RAW` | C07C..C180 | 260 | 257 | 51, 119, 223 |

Both original ordered MZ fixup lists are empty. There are no tables or owned
DATA/BSS. Every alignment NOP compares normally with zero authored credit.
The sources use EVEN, with no opcode emission, pixel payload or inserted NOP.

## Native language and ancestry

Both kernels use an actual hybrid near Pascal interface: left in AX, ring top
in DX and one stack WORD pattern number, ending with RET2. They capture SP
before saving DS/SI/DI and load the pattern's segment through the foreign
512-entry handle table at DS268C. The packed CH/CL row/phase state, string
operations, per-color GRCG port programming and alignment-specific row paths
support original handwritten assembly. The 32x32 row helpers additionally
return DEC CH's ZF directly to the calling row driver. This inference is
independent of any failed C++ build and does not transfer to ordinary callers.

Candidate semantics come from pinned ReC98 b6ba5b0a
th04/formats/z_super_roll_put_tiny.asm. Master ancestry is positively known:
the identity-checked primary Master 0.23 SUPERRPT.ASM contains the original
16x16 tiny format, row/rotation loops and GRCG color expansion. The game changes
the all-stack library entry to AX/DX plus one stack word, keeps ES/GRCG mode
under caller control, omits the library's interrupt/mode setup and shutdown,
and skips an empty even-path third byte. The 32x32 adaptation adds dword rows,
private flag-return helpers and the saved destination coordinate.

These are adapted game procedures rather than the unchanged public Master
routine. The reconstruction is attributed to Koizuka/Master and ZUN through
the candidate reference; it does not claim independent invention, exclusion
of library ancestry, literal historical source or original assembler identity.
Reviewed ASM counts remain separate from C/C++ and verified vendor bodies;
the unreviewed global authored denominator is unchanged.

## Preserved interfaces and behavior

CS is AE1 and incoming DS is 209D; ES already selects video memory and the
caller has selected GRCG mode. DS/SI/DI/BP/ES and IF/DF are preserved; working
registers and arithmetic flags are scratch. Clear DF and valid ring/screen
coordinates are caller preconditions. No clipping, error handling, top
normalization or graphics-state repair is introduced. The 32x32 path needs
386 dword operations despite the older library's V30 description.

Each color begins with a WORD whose low byte is 80h and high byte supplies the
four plane color bits. It is followed by 16 two-byte rows or 32 four-byte rows.
A later header with a different low byte terminates the sprite. Four writes
to port 7Eh expand the color bits; the kernels leave the final tile color and
GRCG mode in place. Raster contents and segment handles remain foreign.

Both paths wrap DI at 32000 while source SI continues through the same color.
The 32x32 path skips zero words and zero edge bytes. The 16x16 even path always
writes its word and skips only an empty carry byte; its odd path always writes
the leading byte and following word. Zero writes are not broadly removed.
The named semantic macros preserve these different write rules.

The 32x32 kernel writes and rereads the actual CODE word at BF60..BF62 to
restore the destination for each color. That word precedes the complete
procedure, stays outside its source contribution and remains unknown ownership.
The binder supplies its address without an initial value. Its original shared
state behavior is retained. No credit is given to the coordinate, handle table,
sprite data, neighboring kernels or already accepted C++ callers.

Native origin/boundary proofs are retained at
`.analysis/tiny32-native-review.json` and `.analysis/tiny16-native-review.json`.
Their SHA-256 values, in that order, are
`c432ce5891534b50a40a94ca3948bf95b2581e036d5b870fb5e9c9bd59ac0224`
and `d41591a48f4c959b30daae8637b9cb9212cec9991d529ab4b8bb0468b586d101`.

## Complete replay and explicit adoption

Both final sources pass the unchanged normal ASM gate: two fresh producers
per kernel, complete ordinary CODE/LEDATA contributions, native CS/DS frames,
actual groups/publics, all raw bytes and original empty ordered fixup lists.
Normalized OMF, MAP and whole MZ outputs are deterministic within each replay.
Dependency metadata normalization never changes instructions or relocations.
Each own negative changes the real pixel phase mask from 7 to 6, retains the
complete extent/publics/fixup list and is rejected by the raw comparison.

The first 32x32 replay also passed. Its source comment incorrectly described
zero bytes inside nonzero word writes; the comment was corrected without any
instruction or ABI change. The final 32x32 replay below pins the final source
and is the only adopted 32x32 receipt. The earlier packet remains historical.
No source producer failed, and no unrelated accepted unit was replayed.
Installed tool execution evidence was reused after dependency identity checks.
No additional semantic model, exhaustive tests or full CI was required.

| Unit | Receipt under `.analysis/asm-replays/` | Receipt SHA-256 |
| --- | --- | --- |
| 32x32 | `main-tiny32-b/receipt.json` | `320e07c0e282f670b57e50027c8a552b0b832133d88ba76d7a314a1faa28e43d` |
| 16x16 | `main-tiny16-a/receipt.json` | `d68d061b9891f9aa6cdf64d847fc057acacd3e764527da40391d29d45f8ec5e0` |

The explicit ownership decision adopts 535 reviewed ASM instruction bytes
from 542 compared bytes; seven checked alignment bytes receive zero credit.
C/C++ counters, the external coordinate word, handles, sprites, neighboring
procedures and whole-executable acceptance are unchanged.

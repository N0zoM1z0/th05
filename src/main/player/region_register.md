# TH05 player invalidation and movement dispatch: complete native-source recovery

MAIN `[C9BA,CAD2)` contains the near `player_invalidate()` body
(`[C9BA,CA4B)`, 145 bytes), its single `EVEN` NOP at `CA4B`, and the
near-Pascal `player_move(unsigned int)` body (`[CA4C,CAD2)`, 134 bytes).
Movement includes 94 instruction bytes and a 20-word CODE jump table at
`[CAAA,CAD2)`. The table entries are derived entirely from named handler
labels and remain in the original `main_01` CS offset domain. The one
original module relocation at family offset 60 is the far `vector2_at`
call to the genuine SHARED `14AB:03B0` interface; the tile invalidator is
the true near callee at `BAD2`.

The first routine invalidates the live player and option sprites with their
actual dirty-box geometry, or paints eight explosion locations after a miss.
It keeps the angle in AL, the remaining-count in AH, and the unsigned radius
in DI. It saves DI only on the miss path, halves the radius after four
explosion locations, and restores AX across the real `vector2_at` call.
Native clipping uses the signed playfield bounds with the original unchecked
wrap behavior. The input-motion routine masks the native low and high input
bits separately before dispatch, preloads aligned/diagonal speeds in DX/CX,
and returns 0, 1 or 2 through AL with the original near-Pascal `RET 2`.
Unmapped or unsupported button combinations return invalid, without a new
defensive branch in the jump-table dispatcher.

## Source origin and compiler comparison

Pinned ReC98 `th05/player.asm` contains the corresponding original-register
reconstruction. It is not a historical original file by itself, and its
language classification is therefore inferred from independently inspected
native behavior: path-conditional DI preservation, BX/SS stack argument
retrieval, tightly packed AH/AL explosion counters, and a manually indexed
switch table with no redundant post-normalization bounds check. These forms
are substantially different from ordinary Borland-generated C++ register
allocation. The earlier natural C++ candidates are still present at
`src/main/player/{invalidate,move}.cpp`; their initial full producers emitted
176/174 bytes and failed. New private register-based C++ experiments narrowed
the respective full sizes to 147/140 bytes but retained unconditional DI
saving and the extra movement switch guard. No C++ exactness is transferred
from this ASM source, and the literal historical producer remains unknown.

The semantic source uses named player-record offsets, event thresholds and
input movement cases, not copied target bytes. The four-byte real point
arguments and the full `player_pos` motion layout are foreign. The symbol-only
binder defines neither player state nor the external helper bodies. All
register, table, loop and return boundaries were compared against the locally
attested original MAIN image, not inferred from the reference listing alone.

## Complete native acceptance

The focused receipt
`.analysis/asm-replays/gpt-web-main-player-register-family-a/receipt.json`
passes two independent true TASM32/TLINK producers, complete 280-byte raw
identity, original ordered far-call fixup `[60]`, real MAP/OMF CODE/DS
frames, all 20 computed dispatch destinations, and a rejected source mutation
that changes the pre-explosion radius by one subpixel. The native instruction,
table and source-origin evidence is
`.analysis/gpt-web-player-register-family-native-review.json`.

Explicit reviewed original-register ASM adoption credits **239 instruction
bytes and 40 CODE-dispatch table bytes**; the intervening `EVEN` NOP is checked
but uncredited. The former natural C++ candidates and accepted neighboring
functions are unchanged and were not cold-replayed.

# Boss tile bitmap rendering and invalidation: exact original-register ASM

The MAIN CODE interval `[F968,FA50)` contains the two complete, adjacent
near-Pascal BB tile-mask helpers: `tiles_bb_put_raw(int)` at
`[F968,F9EC)` (**132 bytes**) and `tiles_bb_invalidate_raw(int)` at
`[F9EC,FA50)` (**100 bytes**). Neither contains switch tables, NOPs,
initialized DATA, BSS or intentionally skipped instructions. The preceding
`90` at `F967` is outside both complete functions and remains unowned.
The original ordered MZ relocation list for the combined 232 bytes is
`[17]`, from the far Pascal `grcg_setcolor` call at frame-zero offset
`1A88` in the first function. Both functions return with `RET 2`.

The put function reads 24 tiles per row from the source BB cel's actual
128-byte bitmap, using FS:DI and two-byte skipped bitmap tails. It sets the
GRCG TDW mode using the real color at DS `4444`, then paints the selected
eight-pixel columns through the existing near graphics worker at `1045C`.
The current scroll state at DS `351A` and scroll line at `3516` retain the
original signed 400-line wrap. The bitmap segment comes from DS `4448`.
The invalidate function scans the same 24-by-23 bitmap, but invalidates
unset bitmap bits through the accepted near tile dirty-rectangle callback
at `BAD2` instead of drawing pixels. Its foreign Boss bitmap segment is
DS `C692`; it writes the original two-by-two dirty extent at DS `3502`
and uses 128- and 256-subpixel tile-center coordinates.

The maintained ASM reconstructs these complete procedures through named
near-Pascal stack locals, actual FS segment reads, the PC-98 GRCG driver,
bit-shift loops, and real far/near calls. It follows the independently
maintained original-assembly donor in pinned ReC98
`th04/main/tile/bb_put_a.asm`, including the GAME5 scroll branch. The
native boundaries, actual register/stack operations and source context
support reviewed original-register assembly reconstruction; literal
historical tokens/assembler and whole-program binary identity remain
unproved. No target-byte arrays, synthetic register stubs, hard-coded
instructions or filler are injected.

## Accepted native result

Focused receipt:
`.analysis/asm-replays/gpt-web-main-bb-mask-a/receipt.json`.
Two independent TASM32/TLINK producers pass the **complete 232/232 raw
bytes**, the original ordered relocation list `[17]`, actual MAP/OMF CODE
ownership, and full near-Pascal entry boundaries. Changing the initial
screen top from 16 to 32 pixels in the actual put source is assembled and
rejected by the native oracle; no source/payload-byte normalization occurs.
The native instruction/source-origin packet is
`.analysis/gpt-web-bb-mask-family-native-review.json`.

The explicit reviewed source adoption adds **232 authored original-ASM CODE
bytes**, two complete functions, zero padding or added DATA/BSS. The
separately accepted native worker at `1045C` and tile invalidator at `BAD2`
are referenced, not reimplemented or re-counted. No C++ exactness is claimed
for these original-register procedures.

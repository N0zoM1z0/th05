# Original TH05 shot laser raster painter

MAIN `[DDF4,DE58)` is the complete near `SHOT_LASER_PUT_RAW` function,
with 98 instruction bytes and two checked `EVEN` alignment NOPs at offsets
69 and 99. The original has no MZ fixups, table or owned DATA. The
previous stage-five midboss renderer ends at `DDF4`; the separate BB Cheeto
loader begins at `DE58`. Neither belongs to this source.

The painter takes screen X in AX, ring-buffer Y in DX, a sprite index in BX,
and an unsigned subpixel height in SI. It uses the existing foreign laser
width-mask byte at DS `1496`, rotates a WORD to cover non-byte-aligned X
positions, then chooses `STOSW` or `STOSB` as required. The 400-line PC-98
ring split is calculated in DX and resumed at VRAM row 0 with the same
mask. ES is set to `A800`; SI and DI are saved/restored, and DF is assumed
clear. This is the source-level register protocol retained in pinned ReC98
`th04/main/player/shot_laser.asm`, not the normal C++ sprite API.

The first actual TASM32 attempt produced 99 matching bytes and the opposite
encoding of the symmetric `XCHG CX,DX` instruction. Reversing the source
operand spelling makes TASM32 emit the original native encoding; this does
not change the algorithm, link output directly or add target-byte data.
The semantic source names geometry and actual near-register inputs; its
foreign-only binding exports no laser mask values or other function body.

## Accepted focused result

The preserved receipt at
`.analysis/asm-replays/gpt-web-main-shot-laser-put-a/receipt.json`
contains two independent TASM32/TLINK producers, a complete 100-byte
object/MAP/native MZ comparison, empty ordered relocations, and a rejected
source mutation of the 400-line wrap threshold. The instruction-level review
is `.analysis/gpt-web-shot-laser-put-native-review.json`. The explicit
original-ASM adoption credits **98 instruction bytes** and excludes the two
verified alignment NOPs. No other accepted unit is recompiled or credited.

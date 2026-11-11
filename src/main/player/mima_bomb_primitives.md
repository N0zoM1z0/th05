# Mima bomb foreground raster primitives

The complete MAIN `[1045C,10508)` block contains three adjacent original
near-register routines. `GRCG_TILE_BB_PUT_8` uses AX/DX as screen coordinates,
rolls a 16-row WORD mask over the 400-line VRAM ring at `A800`, and preserves
DI. The second routine draws all-white 16-bit and 32-bit row patterns, and
the third draws alternating GRCG masks. Both use the actual PC-98 color
register ports `7C/7E` and the native `A850` upper-playfield segment, saving
interrupt flags only around tile setup and switching the GRCG off at exit.

These are the complete natural geometry and register operations retained in
`ReC98/th04/main/tile/bb_put.asm` and the explicitly assembled
`sub_CEC2`/`sub_CEF2` portions of `ReC98/th05_main.asm`. All writes use real
VRAM offsets, with no screen bitmap or fake foreign symbol payload. The block
ends with one original `EVEN` NOP at `10507`. The preceding alignment byte
`1045B`, separately accepted `mima_bomb_bands_fill` at `10508`, and later
Mima backdrop wrappers are not included. No original relocation site exists
in the block.

A first actual TASM32/TLINK producer reconstructed all **172 bytes** and the
empty original relocation list, including the real main_01 `AE1` CODE and
DGROUP `209D` frames. A meaningful source negative lowers the 16-raster-row
limit to 15, without replacing any compared byte after linking.

## Accepted complete original-register ASM

The focused receipt
`.analysis/asm-replays/gpt-web-main-mima-bomb-primitives-a/receipt.json`
proves two independent actual TASM32/TLINK builds, every original instruction
and true public entry offset, raw byte identity and empty relocation order.
The row-count source mutation is assembled and rejected. Independent native
boundaries are in `.analysis/gpt-web-mima-bomb-primitives-native-review.json`.
The explicit reviewed adoption counts **171 authored ASM instruction bytes**;
the final `EVEN` NOP remains zero-credit, as does the preceding foreign NOP.

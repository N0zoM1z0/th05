# Cheeto blitter (assembly)

`cheeto_put.asm` blits one 32x32 Cheeto sprite: MAIN `DE72..DF28`, 178 bytes
of code plus four EVEN alignment NOPs. ReC98's `th05/formats/bb_cheeto.asm`
covers the same code; its history (24b96cd9) relates it to TH04's 32x32 tiny
sprite blitter, minus the blank-row checks.

## Interface

Near fastcall: left in AX, top (already wrapped to the VRAM ring) in DX, cel
in BX; no stack arguments. The caller (`cheetos_render()`) sets ES to `A800`
and the GRCG color, and does all clipping; the blitter validates nothing.
It preserves SI/DI, BP, DS/ES and the interrupt/direction flags, clobbers
AX/BX/CX/DX, and needs DF clear for LODSD/STOSW/STOSB.

The sprites are sixteen 32x32 monochrome cels at DS `378A..3F8A`, 32 rows of
four bytes each. The destination advances by 80 bytes per row and wraps at
32000. Even destinations get two word stores and an overflow byte; odd ones
first write a single byte. Zero bytes are still written through the GRCG.

## Why this stays assembly

The two row workers take the remaining row count in CH and return the result
of `DEC CH` in ZF straight to the caller's JNZ, while CL, DL, BH, BL and DH
carry the bit phase, first-byte mask, word count and overflow byte. Together
with the dword string instructions, this register/flag protocol points to
hand-written assembly. The related master.lib 0.23 routines (SUPERRPT.ASM,
SUPERL1P.ASM, SUPER1PL.ASM) use stack interfaces and other sprite formats,
so this is not a copy of one of them.

# Exact horizontal bit-flip lookup generation in TH05

The original far `hflip_lut_generate()` fills the 256-byte horizontal-flip
lookup table without copying a byte of precomputed image data. AL counts the
input byte from zero through 255; an eight-round `ROL AL,1` / `RCR DL,1`
loop reverses each nonzero byte's bit order, preserving DI and returning far.
The first entry is zero. The shared original-register source is retained in
pinned ReC98 `th03/formats/hfliplut.asm` and agrees with the three distinct
TH05 native function bodies:

| Artifact | Complete original function | Foreign DS table offset |
| --- | --- | --- |
| MAIN | `14B58..14B76` (30 bytes) | `2E8E` |
| OP | `D304..D322` (30 bytes) | `3662` |
| MAINE | `E802..E820` (30 bytes) | `25DE` |

The 8086 near-register body uses an original far return, with no relocations,
CODE tables, padding or owned initialized DATA. It belongs to the handwritten
assembly source family rather than being attributed to compiler-generated C++.
The segment-specific link binders contain only native CODE/DGROUP reservations
and foreign BSS lookup-table labels, not lookup values.

Native sources, registers, and segment offsets were independently checked
against the locally pinned decoded targets before strict replay. This scope
claims only the complete three 30-byte instruction bodies, not literal
historical source spelling or whole-game executable linkage.

## Accepted focused native builds

Two independent TASM32/TLINK producers match each full 30-byte function,
the empty ordered relocation stream, and the original public boundaries.
A real source mutation reduces the number of reversed bits from eight to
seven and is rejected in every artifact. Accepted receipts:

- `.analysis/asm-replays/gpt-web-main-hflip-lut-a/receipt.json`
- `.analysis/asm-replays/gpt-web-op-hflip-lut-a/receipt.json`
- `.analysis/asm-replays/gpt-web-maine-hflip-lut-a/receipt.json`

All **90 instruction bytes** count as reviewed ASM, with no NOP, table or
DATA credit. The existing CDG/PI source owners are unchanged.

# Mima bomb backdrop: complete original-register graphics family

The original MAIN interval `[1052C,1060E)` contains four complete, adjacent
near assembly procedures used by the Mima bomb backdrop. The first draws the
outer color bands and inner center using the separately accepted 35-byte
`mima_bomb_bands_fill` at `10508`; the second clears playfield columns, the
third clears both VRAM pages through GRCG/EGC page selection, and the fourth
provides a reusable twelve-DWORD/row GRCG fill loop. The register interface
uses ES:DI to address PC-98 VRAM, EAX as the GRCG write value, and the GRCG
mode/tile ports at `7C`/`7E`. Interrupt flags and DI are preserved exactly
where the native procedures preserve them. No new CLD, clipping, hardware
initialization, or defensive branch is introduced.

| Actual MAIN entry | Compared extent | Semantic role |
| --- | ---: | --- |
| `1052C` | 105 bytes | White outer/center bands, two-color GRCG writes |
| `10596` | 52 bytes | Black playfield column clearing |
| `105CA` | 54 bytes | Both-page full-plane clear |
| `10600` | 13 bytes | Twelve DWORD/row GRCG fill helper |

The preceding NOP at `1052B` belongs to neither this unit nor the accepted
`mima_bomb_bands_fill` owner. The original NOP at `10595` separates the first
two functions, and the final NOP at `1060D` aligns the following contribution.
Both inside-family NOPs compare against the target but have zero authored
credit. The source contributes no initialized data, BSS, copied target bytes,
artificial stub, or additional runtime dependency.

Semantic ancestry: the pinned ReC98 `th05_main.asm` labels `sub_CF50`,
`sub_CFBA`, `sub_CFEE`, plus `th04/hardware/grcg_fill_rows.asm`. The live
source uses named geometry, actual GRCG port instructions, real loops, and a
foreign-only binder for the already accepted near worker. The native proof
checks every original instruction and all four complete entry boundaries.
The instruction patterns and retained original-assembly reference support
reviewed native ASM reconstruction, without proving the literal historical
source text or assembler binary.

## Accepted complete native evidence

Focused receipt:
`.analysis/asm-replays/gpt-web-main-mima-backdrop-a/receipt.json`.
Two independent actual TASM32/TLINK builds match all 226 original bytes,
the empty original relocation list, actual CODE/CS/DS MAP placement and
complete OMF LEDATA. The compiled negative changes the genuine center-band
VRAM origin to the bottom-band origin and is rejected. The native review is
`.analysis/gpt-web-mima-backdrop-native-review.json`.

Explicit adoption credits **224 authored ASM instruction bytes**, with two
checked but uncredited alignment NOPs. The separately accepted 35-byte near
band worker at `10508..1052B` is not re-counted or recompiled. This is a
bounded CODE-family result, not whole-MAIN binary matching or a C++ claim.

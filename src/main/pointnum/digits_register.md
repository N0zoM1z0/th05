# Exact original-register decimal popup digit encoder

`POINTNUM_DIGITS_SET` occupies the complete MAIN `[15870,158AA)` function
family: 57 actual instructions bytes plus one checked `EVEN` NOP at offset 57.
The real near-Pascal `(WORD points, BYTE near *last_digit)` API reads both
arguments through the saved BP frame, consumes four stack argument bytes and
returns the popup width in AX. It preserves the caller's SI/BP and leaves
BX/CX/DX as scratch. The five glyph digits are stored least-significant
first via the caller's pointer, using the existing five-word powers-of-ten
table at DS `1422` without copying any table data.

The native routine switches BP from frame pointer into a temporary digit-width
accumulator *after loading both parameters*. It uses a single unsigned DIV
per decimal power, tracks the highest nonzero digit position, writes the
remainder, then returns eight pixels per visible digit plus the trailing zero.
The compact register-frame and LOOP form independently supports original
hand-managed ASM: the ordinary C++ spelling in `digits.cpp` needs a persistent
BP frame and two arithmetic operations for quotient/remainder, and emitted
96 bytes rather than the original 58. This source uses the explicit
original-register semantics retained in ReC98
`th05/main/pointnum/digits.asm`. Literal historical source and assembler
identity are not inferred from the modern reference filename.

This is a separate source owner from the adjacent accepted point-popup ring
allocation and from the independently accepted decimal DATA table. The
old natural C++ remains a semantic alternative with no exact credit.
The native DATA, BSS and MZ ordered relocation contributions are empty.

## Focused exact acceptance

The complete native receipt
`.analysis/asm-replays/gpt-web-main-pointnum-digits-register-a/receipt.json`
records two independent TASM32/TLINK producers, all 58 original compared
bytes, the real near-Pascal public boundary, empty fixup stream and OMF/MAP
CODE ownership. Its compiled source negative adds one visible digit-width
unit and is rejected. The independent native instruction record is
`.analysis/gpt-web-pointnum-digits-register-native-review.json`.

Explicit reviewed ASM ownership credits **57 authored instruction bytes**;
the trailing `EVEN` NOP is checked but not counted. The old C++ alternative
and its earlier 96-byte diagnostic remain useful source-language evidence,
not a competing accepted owner.

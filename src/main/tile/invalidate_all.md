# Whole-map dirty fill: native ASM exact; C++ intrinsic remains inexact

The native MAIN function `BD38..BD4E` is 22 instruction bytes, with no NOP,
table or fixup. It sets all 1600 bytes of the full 50x32 half-tile dirty map
at DS `4ADA` to one. The actual game bool is an unsigned byte. Native sets
ES from DS, writes 400 DWORDs and preserves DI, without adding CLD.

Maintained TH04 `main/tile/tile.cpp` and the pinned ReC98 tile source corroborate
the complete map and fill semantics. Their register-template/string-operation
body is not copied as C++ acceptance. The new candidate uses Borland's real
`__memset__` intrinsic from the pinned MEM.H, with the full unsigned-byte map.

The initial setup lacked TC4's separately declared boolean aliases and failed
at the frontend. Correcting the declaration to canonical `uint8_t` and the
true value 1 allows the first complete producer: 16 bytes, with 800 `REP STOSW`
stores and PUSH DS / POP ES instead of native 400 `REP STOSD` stores and
MOV AX,DS / MOV ES,AX. Neither implementation adds CLD. Raw equality fails;
there is no second positive, negative, padding addition, register kernel,
option sweep or ASM-origin inference. The source stays outside the live
manifest, with zero authored credit. The neighboring reset function and
its independent alignment NOP remain foreign.

Actual first producer:
`.analysis/native-producers/main-tile-invalidate-intrinsic-b/`.
Review: `.analysis/tile-invalidate-intrinsic-review.json`.
No existing accepted source/header or compiler tool changed or needed replay.

## Exact original register-level fill — 2026-11-10

The retained TH04 `main/tile/tile.cpp` shows a typed C++ helper that explicitly
sets ES:DI, builds the repeated dirty-flag byte in EAX, and uses a 32-bit
`REP STOSD`. The complete native TH05 `[BD38,BD4E)` routine has exactly that
hardware-level dataflow and preserves DI without adding CLD. The normal DF=0
caller convention remains unchanged. Its full original 22-byte instruction
span has zero relocations, NOPs, tables, or initialized DATA.

The ordinary C++ `__memset__` trial above still emits 16 bytes with a WORD
rather than DWORD fill, different segment-transfer instructions, and a
different assignment order; that failed C++ is retained for provenance without
C/C++ credit. The new maintained `invalidate_all.asm` encodes the *semantic*
50-by-32 flag-bank operation with named geometry and dirty value (one), not
an opcode array or an image payload. Its source-independent symbol binder
anchors the real 209D:4ADA foreign flag array, true AE1 CS frame and all
outside code gaps. No target bytes are supplied by the binder.

Focused strict replay:
`.analysis/gpt-web-main-tile-invalidate-asm-a/receipt.json`.
Two fresh TASM32/TLINK producers match **22/22 full bytes** and literal empty
original relocation order with source CODESEG/LEDATA, original MAP entry,
foreign DS and deterministic object/link outputs. The semantic negative
changes the nonzero dirty value from 1 to 2 and is rejected while preserving
function extent. These are 22 **reviewed ASM instruction bytes**, not
compiler-generated C++ attribution or dirty-map storage. The retained ReC98
reference establishes the register-level source model but does not establish
an exact historical translation unit or assembler identity.

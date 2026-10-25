# Opaque CDG plane drawing

Three complete 102-byte native contributions share one maintained semantic
original-assembly reconstruction. Each has 100 instruction bytes and two
checked NOP bytes with zero credit. These owners remain separate from C/C++
acceptance, the alpha renderer, assets and whole-program/packed-file equality.

| Artifact | Complete load range | Actual CS:offset | DS:slot pool |
| --- | --- | --- | --- |
| MAIN | 14C70..14CD6 | 14AB:01C0 | 209D:306C |
| OP | D590..D5F6 | 0D30:0290 | 0EFE:3A96 |
| MAINE | EA74..EADA | 0E80:0274 | 1011:29FE |

All three scopes fully decode as 49 instructions, including their two NOPs.
Each ends in RETF 6 at relative 98 followed by a NOP at 101; the other NOP is
at relative 75 before the plane loop. No other NOP, padding, table, placeholder,
inert branch, original MZ fixup or owned DATA occurs. Every direct branch lands
on a native instruction within the complete owner. Real far callers independently
establish the native frames; candidate calibration addresses are routing only.

## Source and origin review

The algorithm follows pinned ReC98 b6ba5b0a's
`th04/formats/cdg_p_na.cpp` and `cdg_impl.hpp`. That candidate uses synthetic
register-template C++ to describe a private segment/string-copy protocol; it
does not supply authored C++ acceptance. The maintained ASM instead uses a
semantic row-copy macro, symbolic plane/record constants, arguments and loop
labels. It includes no opcode arrays, codegen helpers, copied instruction
listing, numeric local CODE address or image payload.

Native BP is repurposed from the argument frame to dword width after argument
access; three stacked plane segments drive a B/R/G/E string-copy loop while
DS changes to foreign color data. This deliberate assembly-level protocol and
independent source review support explicit reviewed original-ASM ownership.
No specific inspected native subspan has positive compiler-generated provenance.
Literal historical source, original assembler identity and original mixed C/ASM
possibilities remain unproved. An exact replay alone would not establish origin.

The bounded vendor check searched all 653 members of the pinned master0.23
source archive for function identifiers and distinctive aliases, with no hits.
This does not exclude renamed vendor bodies, every historical adaptation or
all vendor ancestry. Shared hardware constants alone prove neither authorship
nor vendor origin. No compiler-generated or merely inexact C++ owner is promoted.

## Preserved ABI and behavior

The entry is far Pascal `(left, top, slot)` with three word arguments and
RETF 6. Full CDG16 and its 64-slot pool are reused unchanged from
`cdg_alpha_types.inc` and `cdg_alpha_symbols.inc`; canonical C++ records in
the MAIN EMS and MAINE staff headers remain pinned semantic inputs. The record
has five initial word fields, two byte fields at 10/11 and segment words at
12/14. Neither record nor pool is narrowed for matching.

The function saves BP/SI/DI/DS, incorporates `top * 5` into each video segment,
and converts `left` through signed SAR 3. Alpha's unsigned SHR behavior does
not transfer. BX retains the bottom-row destination and DX the upward row
stride. BP retains dword width; AL counts four planes. REP MOVSD copies bottom
to top, then the stack changes the video destination through R/G/E. It performs
the original do-while row copy without adding clipping or zero-width guards.

CLD clears DF, incoming interrupt state is unchanged, and no GRCG mode or alpha
plane is touched. ES returns at the E-plane segment adjusted by `5 * top`,
unlike alpha's sentinel-zero ES result. AX/BX/CX/DX/flags are working state;
BP/SI/DI/DS are restored. No whole-register return value is invented from the
exhausted AL counter. Foreign images and slot data are addresses only.

Both NOPs are conservatively checked alignment, zero credit. The internal
NOP's historical purpose is unknown; its position is compatible with loop
alignment. The source's EVEN directives reproduce the bytes in the reviewed
word-aligned context. Classification never masks or removes either byte.

Symbol-only binders supply real frames, the foreign slot label and reserves,
without initialized payload or artificial stack. MAIN uses its actual DATA end,
OP its complete foreign slot pool, and MAINE the independently accepted foreign
all-cast DATA bound. Every ORG is below 64 KiB; default DATA/BSS alignment and
actual SHARED/DGROUP contexts are preserved.

## Exact evidence and adoption

Receipts under `.analysis/cdg-opaque-native/` are `main-a/receipt.json`,
`op-a/receipt.json` and `maine-a/receipt.json`. Each passes two fresh independent
deterministic TASM producers, complete ordinary CODE SEGDEF/LEDATA/MAP coverage,
actual public/CS/DGROUP frames, every raw byte and the empty literal ordered
MZ relocation stream. Each has its own assembled plane-count 4-to-3 negative,
rejected over the same full scope and fixup stream. The same unchanged tool
execution proof is reused; no prior accepted source or dependency is edited
or cold-replayed.

Independent reports are `.analysis/cdg-noalpha-native-review.json`
(SHA-256 `3a3f0b77f99d68c608ee3da7390a674772df00fac0a69d24be1a72f1674098d8`)
and `.analysis/cdg-opaque-maintained-source-review.json`
(SHA-256 `471c6dfd15e9c90661f918f82577f7311ce9d366c20213e7771478d21c3d0e82`).
Descriptors pin the complete native proofs in `config/asm_families.toml`.
Exact records and the separate explicit per-owner/note adoption are in
`accepted_asm_families.json` and `reviewed_asm_families.json`.
Totals are 306 compared bytes, 300 reviewed ASM instructions and six checked
uncredited NOPs, with zero C/C++ or DATA credit. The global denominator and
98% objective remain open.

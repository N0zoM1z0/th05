# Mima backdrop band worker

MAIN `10508..1052B` is one complete 35-byte private near worker in
`main_01` / CS `AE1`, DS `209D`. It has no NOP, table, DATA, BSS or MZ fixup.
The following NOP at `1052B` remains outside this owner.

The two verified calls at `10544` and `1054C` set ES to `AE90` and `A850`
respectively, without stack arguments. Their outer wrapper saves/restores DI;
the worker deliberately overwrites DI without restoring it. It consumes the
caller's ES and EAX, and leaves DI, CX and flags changed. This private register
interface supports hand-controlled assembly ownership for the worker. No
ordinary C/C++ body is converted following a failed compiler experiment, and
no assembly-origin claim is transferred to surrounding entry points.

The semantic source fills two 48-row bands at X32 and X240, each 176 pixels
wide. Every row writes five DWORDs and a final WORD, then moves one VRAM row
upward. The caller has enabled GRCG TDW and its tile color, so the hardware
ignores the stored data value. ES/EAX/DX/DS/SI/BP and interrupt state remain
unchanged. The original clear-DF assumption is retained; no CLD, clipping or
error handling is added. Constants describe the whole geometry, and all loop
destinations are labels rather than copied target addresses.

ReC98 `th05_main.asm` lines 2466..2484 supplies candidate semantics. Native
instructions, both callers, return boundary and all branches are independently
read from the pinned candidate-local-attested MAIN. Historical source and
assembler identity remain unproved. All caller bodies and resources stay
foreign and receive no new coverage.

Native ABI/origin/boundary review: `.analysis/mima-bands-native-review.json`,
SHA-256 `8ed2d78a899de8acd31407e0b4c4dc50e38c4afe0c30c5998b1cf5f6123fea2c`.
Two fresh ordinary TASM/TLINK producers pass complete OMF/MAP, all 35 raw
bytes, deterministic outputs and original empty fixups. The normal band-width
176-to-144 assembled negative is rejected. No old owner or tool probe was
rebuilt; the standard replay tools and complete caller types are unchanged.

Accepted receipt: `.analysis/asm-replays/main-mima-bands-a/receipt.json`,
SHA-256 `48eb0fe45c12eca9254ea1adbab9675c22d679cdc1b0ecb87491e8dd934a9f9f`.
Explicit adoption adds 35 reviewed ASM instruction bytes, no C/C++ credit.

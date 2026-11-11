# Exact OP/MAINE four-plane background snapshot and restore

The two adjacent far C++ functions `bgimage_snap()` and `bgimage_put()` now
share one complete 157-byte compiler contribution in **each** decoded binary:

| Artifact | Snap (104 bytes) | Put (53 bytes) | Original relocations |
| --- | --- | --- | --- |
| OP | `D688..D6F0` | `D6F0..D725` | `[15,26,37,48]` |
| MAINE | `EB6C..EBD4` | `EBD4..EC09` | `[15,26,37,48]` |

The independent one-byte `EVEN` NOP at OP `D725` / MAINE `EC09` is outside
the C++ contribution and earns no authored credit. The separately accepted
`bgimage_free()` routines follow after those bytes, with no overlapping code.

The maintained TH04/TH05 C++ semantics allocate four 32,000-byte segment
buffers only when the first B-plane handle is null. The routines then copy
the E/G/R/B VRAM planes at `E000/B800/B000/A800` using one 8,000-DWORD
`REP MOVSD` per plane. Snap pops ES then DS (VRAM to buffer), whereas Put
pops DS then ES (buffer to VRAM). The precise ordering of four segment pairs,
`DL` countdown, preserved SI/DI and restored DS reproduce the original
hardware interface. No bitmap contents, allocation failures, extra bounds
checks or DATA variables are supplied.

The older separate-function TCC trial discovered a real compiler-context
issue: `bgimage_put()` references the C++ `bgimage` variable only in inline
ASM, so compiling it alone omitted the required DGROUP external declaration.
Keeping the two neighboring functions in their actual common C++ translation
unit causes Turbo C++ to emit that declaration from Snap's real data access,
without a fabricated symbol or changed instruction stream. Direct `-c`
rejects 386 `MOVSD`; unmodified TCC `-S` output assembled by TASM32 generates
both complete functions and the ascending relocation order.

Focused strict receipts:

- `.analysis/unit-replays/gpt-web-op-bgimage-transfer-complete-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-bgimage-transfer-complete-a/receipt.json`

Each has two independent TCC/TASM32/TLINK producers, complete original bytes,
ordered fixups, original CS/DGROUP/map and OMF CODE contribution boundaries,
and a compiled negative that changes the B-plane allocation size. Both
negatives are rejected. The source is shared, but OP and MAINE have their own
native segment/address binders and separate accepted evidence.

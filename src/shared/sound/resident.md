# Kaja driver resident detection

`mmd_resident.cpp` independently recovers the complete MMD detector in all
three MZ targets. Each extent has 47 instruction bytes, 15 instructions, two
FAR cdecl returns, no arguments and no original relocation, table or padding.
Every local branch ends at the final failure path. The subsequent original
NOP is outside each function and receives no credit.

| Artifact | Complete load scope | CS | DS | MIDI-possible byte | Selected interrupt byte | Receipt under `.analysis/unit-replays/` |
| --- | --- | --- | --- | --- | --- | --- |
| MAIN | `[14BA4,14BD3)` | 14AB | 209D | 0837 | 2F8E | `main-mmd-resident-exact/receipt.json` |
| OP | `[D350,D37F)` | 0D30 | 0EFE | 0A63 | 3762 | `op-mmd-resident-exact/receipt.json` |
| MAINE | `[E84E,E87D)` | 0E80 | 1011 | 06DD | 26DE | `maine-mmd-resident-exact/receipt.json` |

ES=0 selects the real-mode interrupt vector table. Its entry at 61h*4 is the
driver's far pointer. The complete five-byte signature header contains the
two-byte entry jump and three magic characters, with size/offset assertions.
Ordinary typed C++ reads test `MMD`; success selects interrupt61h, enables the
byte flag and returns1. Failure returns0 and preserves the previous state.
The original unchecked vector/pointer behavior is retained.

Source evidence is the maintained TH04 `src/shared/sound/mmd_resident.c` and
its typed signature macro, plus pinned ReC98 b6ba5b0a's `th02/snd/mmd_res.c`.
TH05 replaces that reference's handwritten LES and forced early RETF with a
typed `__es` pointer read and normal C++ returns. No forced arithmetic register,
instruction body, emitted byte or codestring is used. TH04 acceptance does not
transfer; the three native functions are reviewed and replayed independently.

The initial named far-pointer local emitted60 bytes, spilling four bytes to
the stack and adding a frame. The typed field-access form retains the real
vector load in ES:BX naturally, with no pointer materialization or Boolean
return template. Its first direct diagnostic was raw-equal. The final shared
header and source then pass two deterministic builds, valid OMF, all47 raw
bytes and the empty original ordered fixup stream in each artifact. Each
normal replay rejects the compiled interrupt61h-to60h selection mutation.
Only new units were built; installed tool probes and unchanged accepted inputs
were reused after identity checks. The binders own no helper bodies or data.

Receipt SHA-256, in table order:

* `0010fe3aa71a3be7fab42c289a64cddf7355d106b6a908bf1c1120074dc4b9c7`
* `b2a59de2935e85641661fd538f3711e2e1736d7f3b079867f82f0de6cd532186`
* `14439663721df02a1d3ad5a0e770042f32b2a5c4afcbf4457fa2366ee382762f`

Native boundaries and complete instruction/branch review are retained in
`.analysis/mmd-resident-boundary-review.json`. The actual state-selector callers
also retain their earlier independent [mode-selection acceptance](modes.md).
This claims no initialized DATA, BSS, packed-file or whole-executable recovery.

## PMD detector: exact MAIN, OP and MAINE C++ reconstruction

The PMD detector now has three independently accepted 46-byte C++ owners:
MAIN `[14B76,14BA4)` (`main-pmd-resident`), OP `[D322,D350)`
(`op-pmd-resident`) and MAINE `[E820,E84E)` (`maine-pmd-resident`). The native 16-bit function
initializes AX to zero, selects interrupt `60h`, resets three sound-mode bytes
from AL, sets ES from AX, examines the original PMD driver signature in the
interrupt vector and increments AX on success before returning via far C RETF.
All 46 instruction bytes and the empty original relocation stream match in
two fresh deterministic producers **for each** target. No DATA/BSS, padding, target bytes or
handwritten instruction body is attributed to this owner.

The initial ordinary C++ local `found` placed the result in DX. That added
three one-byte-longer byte stores and a two-byte DX-to-AX return transfer,
producing 51 versus 46 bytes. Multiple typed-state/return variants were
compiled, including direct Boolean return, register and narrow scalar locals;
none matched. The maintained original TH04 `th04/snd/pmd_res.c` demonstrates
the real DOS AX convention. Restoring `_AX` as the original hardware/result
state while retaining the typed `KAJA_ISR_MAGIC()` vector access naturally
reproduces all 46 bytes without copying its inline `LES` assembly. This
register use preserves a genuine externally observable CPU/ES contract, not
an arbitrary code-size hint.

Focused independent receipts (each with two positive compiler/linker producers):

- MAIN `.analysis/unit-replays/gpt-web-main-pmd-resident-20261110/receipt.json`
- OP `.analysis/unit-replays/gpt-web-op-pmd-resident-20261110/receipt.json`
- MAINE `.analysis/unit-replays/gpt-web-maine-pmd-resident-20261110/receipt.json`

Each compiled semantic negative changes the selected interrupt from `60h` to
`61h` and is rejected. The original source, artifact-specific binary macro,
CS/DS frames, actual MAP/MZ/OMF, compiler arguments and all source dependencies
are recorded in each receipt. OP and MAINE comparisons use their independently
pinned decoded load modules and original relocation order. All three accepted
MMD owners are unchanged; no shared whole-executable or packed-file claim is
inferred. Total new authored coverage from these three PMD owners is 138 bytes.

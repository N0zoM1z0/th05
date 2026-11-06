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

## PMD remains unaccepted

The adjacent MAIN PMD detector is `[14B76,14BA4)`,46 bytes. The new ordinary
`pmd_resident.cpp` keeps the same state reset, vector60h signature check and
integer result. Its first successful compiler producer emits51 bytes: the
result lives in DX, making the three byte stores one byte longer each, with
an additional two-byte transfer into the return register. An ordinary
`register` declaration leaves51 unchanged and was reverted. Neither trial
contains a physical-register arithmetic algorithm or grants exact credit.

Frozen diagnostics are `main-pmd-resident-b` and
`main-pmd-resident-register-a` under `.analysis/native-producers/`. Their old
nominal tail also displaced DATA; no whole-linked behavioral claim is made.
The maintained outside-only binder now aligns its foreign DATA gap to a real
paragraph, accommodating either46 or51 bytes without padding a function.
A subsequent ordinary C-frontend diagnostic still emits51 with the same DX
result allocation. It confirms the corrected binder's real DS addresses;
neither language form is exact. That first producer is retained at
`main-pmd-resident-c-a`; its experimental C source was removed. No PMD unit is
in a live exact manifest, and no OP/MAINE PMD producer was run.

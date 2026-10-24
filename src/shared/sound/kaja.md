# Kaja driver interrupt

Maintained semantic C++ adapts nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th02/snd/kajaint.cpp` with GAME=5.
It keeps the existing AX when music is disabled, reads the true far Pascal word
argument at SS:SP+4, and dispatches to PMD interrupt 60h or MMD interrupt 61h.
The genuine Borland register/peek/interrupt intrinsics supply those operations.
There are no emitted instructions or padding directives.

The complete OP decoded function is `[DC76,DC93)`: 29 bytes / 10 instructions,
SHA-256 `e54ac426391362ebd7e7c3b0822da10fc15c8e462498aa26c6319d71651a8722`.
All local jumps land on instruction starts. Its RETF 2 proves far Pascal cleanup;
24 original far callers independently establish frame:offset `0D30:0976`.
There are no MZ fixups inside the function. The following original NOP at DC93
is outside its complete extent and receives no authored credit.

OP's real DGROUP frame is `0EFE`; `snd_bgm_mode` is the byte at offset `0A62`.
Symbol-only context anchors these frames without providing implementations or
data values. The pinned decoded view preserves original ordered relocations
and the two historical decoder loads; it does not synthesize an original MZ
header or claim packed-file equality.

`.analysis/unit-replays/op-kaja-a` contains two isolated deterministic producers
and a compiled change of the MIDI discriminator from 3 to 2. Both complete raw
comparisons pass; the changed producer is rejected. The importer independently
rechecks frozen decoded bytes/proof, both MZ/MAP/OMF producers, actual O binary
arguments, source inputs and negative control. Public source-current acceptance
is in `config/accepted_units.op.json`. MAIN and MAINE now have independent passing receipts in
`.analysis/unit-replays/main-kaja-a` and `maine-kaja-a`. Both preserve the real O
compiler context used by the reference for this shared producer, overriding the
artifact default explicitly. Each has its own two fresh producers, compiled
mutation and target checks; acceptance does not transfer between artifacts.

| Artifact | Complete load extent | True far frame:offset | DGROUP flag |
| --- | --- | --- | --- |
| MAIN | `14F5C..14F79` | `14AB:04AC` | `209D:0836` |
| OP decoded | `DC76..DC93` | `0D30:0976` | `0EFE:0A62` |
| MAINE decoded | `EE1E..EE3B` | `0E80:061E` | `1011:06DC` |

The MAINE frame is independently established by ten original far callers,
rather than copying the calibration's E7F frame. MAIN has seven such callers.
The following NOP in each target is excluded from the accepted function.

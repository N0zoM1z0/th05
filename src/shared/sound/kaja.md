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
is in `config/accepted_units.op.json`. No MAIN or MAINE scope inherits this
acceptance even though the maintained source can be reused there.

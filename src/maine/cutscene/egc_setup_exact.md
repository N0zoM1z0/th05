# Exact MAINE cutscene EGC interpage-copy setup

The complete near `egc_start_copy()` hardware setup at decoded MAINE
`[A6D1,A705)` is reproduced from a standalone 52-byte Turbo C++ source
translation unit. It activates EGC, selects all four planes and the required
read/ROP/mask/address/bit-length values through their real PC-98 word ports.
The original far `EGC_ON` call supplies the only ordered MZ fixup, `[6]`.

The source preserves the hardware command's register protocol and the
`MOV AX,0` word write for the EGC address register, rather than changing
zeroing into a flag-modifying XOR. The command follows the original
`outport2` interface retained in ReC98's EGC hardware reference and emits no
hard-coded opcode bytes. Other registers use natural Borland `_AX`, `_DX`
and `outport` intrinsics.

The earlier combined `cutscene.cpp` candidate remains unchanged. Its EGC
helper was 51 bytes because it lowered the zero word as `XOR AX,AX`, while the
other nine accepted functions occupy independent, already verified scopes.
The standalone full function is kept separate so that accepting it does not
alter those established compiler inputs or claim any part of the neighboring
1,555-byte `script_op()` interpreter.

Focused receipt:
`.analysis/unit-replays/gpt-web-maine-cutscene-egc-exact-a/receipt.json`.
Two independent Turbo C++/TLINK producers match the full 52 native bytes,
the original `[6]` fixup and the true `group_01` CS/DGROUP frames. Changing
the address-register value from zero to one compiles and is rejected by the
strict oracle. No full cold replay was run.

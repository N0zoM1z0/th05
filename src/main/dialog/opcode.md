# Complete dialog interpreter candidate

The pinned MAIN interpreter `[13B82,13D4A)` is 456 bytes: 425 instruction bytes,
one zero at 425 and a 30-byte command table at 426. Its 124 instructions have no
NOPs. All fifteen table destinations and direct branches land on reviewed
instruction boundaries. Original ordered MZ fixups are
`[395,336,312,269,224,217,174,145,136,86]`.

The canonical semantic body is `opcode.inl`; `opcode.cpp` uses the actual
main_01 context and late `-a2` after the packed declarations. The complete
five-byte sprite command and all accepted box/run dependencies are unchanged.
Direct compilation produces 455 bytes. The missing compiler-owned zero also
moves the table operand and forward external labels one byte early. Ordered
fixups agree, but the full byte/size gate fails; no exact credit is imported.

A genuine STD-callback prefix in a separate segment also produced 455. Its
experimental `opcode_context.cpp` and binder were retired during cleanup;
complete frozen inputs remain under
`.analysis/unit-replays/main-dialog-opcode-context-a/`. The independent failed
baseline remains in `main-dialog-opcode-standalone-a/` under the same parent.
Declaration timing, switch casts, explicit reserved cases and initial alignment
trials remain failed. `-G` produces 468. Those alternative diagnostics are
[archived](../../../docs/LOCAL_STORAGE.md).

## Compiler-generated ASM observation

Compiling the unchanged C++ with TCC `-S` emits a genuine `db 1 dup (?)`
between RET2 and the command table. Assembling that unmodified generated file
with TASM32 reproduces all 456 raw bytes, including the zero. Its original
fixups are instead emitted in ascending order, so the result still fails exact
acceptance. A diagnostic DOS TASM 4.1 from existing private media gives the same
raw equality and wrong order; it is not an accepted/pinned toolchain addition.
No ASM instruction transcription, output patch or relocation sorting is used.

Both raw-equal failed diagnostics remain live:
`.analysis/native-producers/main-dialog-via-asm-a/` and
`main-dialog-via-asm16-a/`. The standalone source is restored. The remaining
question is producer/source context that reproduces both table alignment and
original relocation order, not adding a zero by hand.

The earlier native/producer review is `.analysis/dialog-opcode-root-review.json`,
SHA-256 `cbfac3b961c10cd82eba16ca5b9561722359c57a8c760628fd97333f94b54df8`.
Its semantic model is historical corroboration, not a recurring acceptance task.

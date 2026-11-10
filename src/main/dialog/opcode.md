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

A genuine STD-callback prefix in a separate segment also produced 455.
Declaration timing, switch casts, explicit reserved cases and initial alignment
trials failed. `-G` produces 468.

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

A later normal `-a` spelling after the canonical types, prompted by the
item-family result, still emits 455 with the same native descending fixups.
The complete first-size gate fails; no second producer or negative runs.
The source is restored byte-for-byte.
Together with the stage initializer follow-up, this confirms that the item
recovery's genuine source context cannot be replaced by this spelling alone.

## 2026-11-10 physical dialog table alignment follow-up

The authentic `dialog_op()` C++ still compiles to **455 rather than 456 bytes**.
The direct Turbo C++ object already preserves all ten **individual native
ordered** relocation sites, but omits the natural CODE switch-table zero at
function-relative +425. The generated unedited C++ assembly contains
`db 1 dup (?)` in the *standalone* source and TASM32 then reproduces 456 raw
bytes; its MZ fixup order is **ascending** rather than the original reverse
record order. These failures are independent and cannot be conflated.

New actual cold-source experiments tried the complete 106-byte preceding
`dialog_box_wipe()`/fade implementation before the opcode and also the real
270-byte following `dialog_run()` in a shared source. Both emitted the same
native-ordered opcode fixups but a **455-byte** function. The joined
106+455+270 source generated **831 bytes** rather than native 832. Compiling
the authentic maintained three-function `runtime.cpp` via the supported
unmodified `TCC -S → TASM32` pipeline likewise emitted **831 bytes**; the
opcode table lacked a `db 1 dup (?)` declaration *within that combined
translation unit*. The whole-group TASM relocation records were ascending
instead of the native grouping, so no whole-code credit is possible.

Additional isolated, real Turbo C++ compiler-option trials show `-a1` or
`-a` after the packed header, and `-a1` before it, preserve the wrong
455-byte extent. Both `-a4` and `-a8` are **invalid pragmas** in installed
Turbo C++ 4.02; setting `-a2` before the packed runtime header breaks its
intentional record layout assertion, so that source is invalid. These are
failed observations, not a recommendation to override game ABI types.

Frozen first-producer inputs and MAP/OMF/MZ evidence are kept under
`.analysis/gpt-web-dialog-box-opcode-{b,run-a}/`,
`.analysis/gpt-web-dialog-align-*-b/` and
`.analysis/gpt-web-dialog-runtime-compilerasm-a/`. All current accepted
surrounding Box/Runner source is unchanged. A genuine different original
compiler-context layout, not source-visible fake zero-byte instructions,
patched MZ data or sorted fixups, is still required before claiming an exact
456-byte opcode function.

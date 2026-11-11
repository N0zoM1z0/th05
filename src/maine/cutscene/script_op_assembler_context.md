# MAINE cutscene script dispatcher: TCC group and fixup-order blocker

The full 1,555-byte `script_op(unsigned char)` at decoded MAINE
`[A9C3,AFD6)` remains **unaccepted**. Its existing natural C++ body in
`cutscene.cpp` was observed to match the complete native instructions under
direct TCC `-c`, but the original sequence of 42 MZ relocation entries did
not match. The nine separately accepted neighboring cutscene functions remain
unchanged and retain their own evidence.

A new targeted compiler experiment used genuine TCC 4.02 `-S` output, TASM32,
TLINK and the existing real `CUTSCENE_TEXT`/`CUTSCENE_AFTER_TEXT` source
contributions. Plain TASM32 assembly initially failed with 101 `CS unreachable`
and short-relative-jump errors. The generated assembly declares `GROUP_01`
with `CUTSCENE_TEXT` only; later functions are emitted into
`CUTSCENE_AFTER_TEXT` but their near calls and jumps still assume `GROUP_01`.

Adding a **declaration-only** `GROUP_01 group CUTSCENE_AFTER_TEXT` to an
isolated experimental assembly wrapper, before including the *unchanged*
generated `.ASM`, resolves all assembler errors and links successfully.
However, the resulting full script-dispatcher comparison is still inexact:

- Native code has `MOV BX,0A56h` at function offset 28; TASM emits
  `MOV BX,0896h` (two differing immediate bytes at relative offsets 29–30).
  The source is a compiler-generated sparse-switch lookup; this is a group-
  versus-segment-relative table-address calculation, not an application
  algorithm difference.
- Both images have **42** original/code segment fixup entries, but TASM
  serializes them in ascending address order, while the native list starts
  `[179,156,14,1230,1200,...]`. Neither sorting the native list nor patching
  OMF records would be a valid source reconstruction.

Private reproducible evidence is retained in
`.analysis/gpt-web-maine-cutscene-s-diagnostic/` (failed direct TASM group
context), `.analysis/gpt-web-maine-cutscene-s-grouptrial/` (successful
assembler/linker and strict inexact full comparison), and the source staging
script `.analysis/gpt-web-maine-cutscene-s-diagnostic.py`.

A productive next attempt should recover the original Borland compiler's
**group-relative switch-table OFFSET and OMF relocation emission context**
from meaningful source/module declarations. It must compare all 1,555 bytes
and all 42 literal ordered fixups and compile a source negative before
acceptance. Do not promote a partial matched function, artificial assembler
patch or accepted neighbor as evidence for the interpreter itself.

## Later direct/split compiler diagnostics

The fresh local `gpt-web-maine-cutscene-direct-a` TCC `-c` experiment has all
1,555 original script-op bytes exact, but its 42 relocations remain in a
different OMF order. Moving script-op into its own real CODE segment yields
its complete 1,555-byte function, but changes 27 far-call segment words and
the relocation order; splitting `cutscene_animate` also yields one extra
trailing compiler alignment byte. The isolated experiments are in the private
`gpt-web-maine-cutscene-split-scriptop-{a,b}` directories. These are useful
placement evidence, not acceptance or a reason to reorder fixup records.

## Resolved: original single CODE segment

The compiler-buffer hypothesis was confirmed with a real unified translation
unit. With the previously split 111-byte prefix and remainder restored to one
`CUTSCENE_TEXT` segment, the correct LEDATA boundaries appear at offsets
1,024 and 2,048. The complete `script_op()` now matches every byte and all
42 ordered fixups, and the entire 2,848-byte module matches its original 64
ordered fixups. The strict receipt is
`.analysis/unit-replays/gpt-web-maine-cutscene-script-op-unified-a/receipt.json`.
The earlier mismatches above remain valid diagnostics for the different split
producer, **not a current open interpreter blocker**.

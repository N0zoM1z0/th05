# TH05 demo replay candidate

Natural source is adapted from ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/demo.cpp` → `th04/main/demo.cpp` and `th04/main/demo.hpp`. The original macro's handwritten exit-call instructions have been replaced with the real `GameExecl(DEMOPLAY_BINARY_OP)` C++ call. The original callee at load `0xCEC2` ends in `RETF 4` at `0xCF5E`; its declaration remains Pascal far, returning `int`.

Native decoding independently establishes the complete original contribution `[0xB756,0xB826)`, 207 instruction bytes plus one checked linker-relaxation NOP, with no tables:

| Function | Original start | Size |
|---|---:|---:|
| `demo_load()` | `0xB756` | 94 |
| `DemoPlay()` (MAP: `demoplay()`) | `0xB7B4` | 114 |

There are six ordered original MZ fixup sites relative to the complete extent: `195,188,89,84,73,30`. All original local branches land on decoded instruction starts. MAIN01 is frame `0xAE1`, original DGROUP is `0x209D`. The private native review is `.analysis/demo-boundary-review.json`; it includes every original instruction, call, operand binding, boundary, fixup, source snapshot and return.

The maintained owner defines no initialized DATA or BSS. `DemoBuf`, input state, the mutable replay filename, OP executable name and resident pointer remain genuine foreign variables. `resident_t` is the existing complete canonical128-byte type with demo number at offset31. The replay record has a real byte input stream plus one-byte shift flags; regular/extra capacities are5000/20000 frames and10000/40000 bytes.

The first separate-segment replay did not accept the full208. The original exit call contains `NOP; PUSH CS; CALL near` at `0xB81F`; the first instruction is the padding left by far-call linker relaxation. A real far C++ call and a separate foreign CODE context may retain a far call instead. The binder supplies only the true far symbol/address and no instructions. Observe actual compiler/linker output; do not add a false near prototype, emit bytes, an instruction macro or a fake helper. A genuine common-SEGDEF interleaved context may be needed for the whole function.

The independent complete94-byte `demo_load()` scope was the first replay proposal. Its meaningful negative changes only the first allocation-selection threshold from demo number4 to3. The private registration proposal is `.analysis/demo-dialog-candidates.json`. That preparation did not compile or accept either source.

`main-demo-b` is an honest mixed-result replay: `demo_load` passes all94
bytes and ordered fixups in both independent producers, with its own compiled
allocation-threshold control. Only that complete function is imported. The
114-byte playback function still retains a far GameExecl call where the
original has linker shortening, and remains unaccepted in that receipt. The entire saved mixed
parent and its failed result are preserved and revalidated on subset import.
The original oversized context ORG was split at the real14AB0 frame; the
failed assembler-only first attempt produced no compiler artifacts.

## Complete DemoPlay acceptance with genuine common SEGDEF

`main-demoplay-common-segment-a` accepts the complete114-byte `DemoPlay()`
from the unchanged maintained C++ source, header, first-declaration context
and compiler arguments. The far Pascal `GameExecl(const char far*)` API is
unchanged; native provider `0xCEC2` still ends with `RETF4` at `0xCF5E`.
Both callers belong to the same public `DEMO_TEXT` SEGDEF in the new oracle
context. Group/CS identity alone did not permit TLINK's observed shortening.

`probes/units/demo_play_bindings.asm` is one frozen conditional symbol-only
source. Its first object precedes the genuine208-byte compiler contribution
`[0xB756,0xB826)`; its second object follows it and declares the foreign far
callee at its true address. Both views have valid OMF checksums and no
LEDATA/LIDATA, instruction bytes, fixups, synthetic entry or stack. All ORGs
are below64KiB. The empty first-prototype segment retains its original group
context. The callee is beyond the compiler contribution, with no inserted
inside-function gap or byte normalization.

The complete native scope `[0xB7B4,0xB826)` ends in near `RET` at `0xB825`.
Its only NOP is at `0xB81F`, relative107, immediately before `PUSH CS; CALL
near`. This genuine linker-relaxation NOP is compared normally and gets zero
authored credit: **113 authored instruction bytes / 114 complete compared**.
Ordered MZ fixups are `[101,94]`; complete raw SHA-256 is
`1f5f93790ef1f77b33922fb2277b7b165e93b46544f35bb03f5ab2450c5cc34c`.
Owned DATA/BSS remain empty.

A preliminary relink used the retained old compiler object unchanged and
proved this layout before any new compilation. Only the new receipt
`.analysis/unit-replays/main-demoplay-common-segment-a/receipt.json`, SHA-256
`dbb97a3cc80d153b72d4258731d2c7b012de9fdfb51f6e6a7b0aca12b827fb1e`,
supplies acceptance: two fresh deterministic compiler producers, complete
raw comparison, original relocation order and the function's own compiled
`DEMO_N-4` to `DEMO_N-5` negative. The negative keeps the same114-byte scope,
NOP, ordered fixups and binding models, but changes the actual C++ output
and is rejected. No earlier `demo_load()` receipt or source identity changes;
its94 bytes receive no additional credit. Installed toolchain probes are reused.

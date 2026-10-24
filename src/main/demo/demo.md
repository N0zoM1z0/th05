# TH05 demo replay candidate

Natural source is adapted from ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/demo.cpp` → `th04/main/demo.cpp` and `th04/main/demo.hpp`. The original macro's handwritten exit-call instructions have been replaced with the real `GameExecl(DEMOPLAY_BINARY_OP)` C++ call. The original callee at load `0xCEC2` ends in `RETF 4` at `0xCF5E`; its declaration remains Pascal far, returning `int`.

Native decoding independently establishes the complete original contribution `[0xB756,0xB826)`, 208 instruction bytes, with no tables or padding:

| Function | Original start | Size |
|---|---:|---:|
| `demo_load()` | `0xB756` | 94 |
| `DemoPlay()` (MAP: `demoplay()`) | `0xB7B4` | 114 |

There are six ordered original MZ fixup sites relative to the complete extent: `195,188,89,84,73,30`. All original local branches land on decoded instruction starts. MAIN01 is frame `0xAE1`, original DGROUP is `0x209D`. The private native review is `.analysis/demo-boundary-review.json`; it includes every original instruction, call, operand binding, boundary, fixup, source snapshot and return.

The maintained owner defines no initialized DATA or BSS. `DemoBuf`, input state, the mutable replay filename, OP executable name and resident pointer remain genuine foreign variables. `resident_t` is the existing complete canonical128-byte type with demo number at offset31. The replay record has a real byte input stream plus one-byte shift flags; regular/extra capacities are5000/20000 frames and10000/40000 bytes.

Full208 is a candidate, not an exact claim. The original exit call contains `NOP; PUSH CS; CALL near` at `0xB81F`; the first instruction is the padding left by far-call linker relaxation. A real far C++ call and a separate foreign CODE context may retain a far call instead. The binder supplies only the true far symbol/address and no instructions. Observe actual compiler/linker output; do not add a false near prototype, emit bytes, an instruction macro or a fake helper. A genuine common-SEGDEF interleaved context may be needed for the whole function.

The independent complete94-byte `demo_load()` scope is the safe first replay proposal. Its meaningful negative changes only the first allocation-selection threshold from demo number4 to3. The private registration proposal is `.analysis/demo-dialog-candidates.json`. Neither source has been compiled or accepted during this preparation.

`main-demo-b` is an honest mixed-result replay: `demo_load` passes all94
bytes and ordered fixups in both independent producers, with its own compiled
allocation-threshold control. Only that complete function is imported. The
114-byte playback function still retains a far GameExecl call where the
original has linker shortening, and is unaccepted. The entire saved mixed
parent and its failed result are preserved and revalidated on subset import.
The original oversized context ORG was split at the real14AB0 frame; the
failed assembler-only first attempt produced no compiler artifacts.

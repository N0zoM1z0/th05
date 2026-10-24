# Custom-ball reset and allocation

This natural C++ candidate owns two complete original MAIN functions:
`b4balls_reset` at `[0x183D5,0x183F0)` (27 bytes) and `b4balls_add`
at `[0x183F0,0x18459)` (105 bytes). Coordinates are offsets in the
unrelocated MZ program image. Their frame is `1527`, group `main_03`.
All 132 bytes decode as instructions; neither function has a following
switch table, alignment byte, or original MZ relocation in its extent.

The original executable SHA-256 is
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
ReC98 revision `b6ba5b0a`, `th05/main/bullet/b4balls_add.asm`, supplies
reference disassembly and names. Original target operands and complete
RET boundaries were independently checked. This source expresses the
algorithm without assembly or target instruction arrays. Compiler-generated
origin is inferred from the ordinary BP frames, local word, saved SI/DI,
structured loops and typed helper calls; source spelling is reconstructed.

The unchanged accepted `b4ball.hpp` supplies the complete 26-byte live
record, 25-byte template and 64-slot custom-entity overlay. Slot zero is
the template; slots 1 through 63 are live balls. Reset changes only their
flags. Allocation scans for the first free slot, initializes the fields
actually written by the original and leaves age, previous position and
unused fields alone. The initial velocity uses performance-adjusted
speed, widened to a word. The stored speed remains the raw template byte.

Both entry points have the genuine `extern "C" void near Pascal` no-argument
interface already declared by the frozen header. There is no deliberate
carry-return protocol: neither body contains CLC/STC/POPF, and reviewed
Yuki/Mai reset callers and allocator callers do not consume CF. Incidental
registers and flags at RET are not a source return value. The foreign
helpers remain the actual AL-input/AL-output `playperf_speedtune` at
`0x171EA`, and near Pascal `vector2_near` at `0x152DA` with three word
argument slots and RET 6.

Private integration inputs are `.analysis/b4ball-spawn-bindings.asm`,
`.analysis/b4ball-spawn-unit-proposal.toml`, and
`.analysis/b4ball-spawn-boundary-review.json`. The symbol-only binder
supplies no helper bodies, table values or owned padding. The proposed
negative changes a new ball's initial damage from zero to one. Exact
acceptance awaits two fresh strict raw/ordered comparisons and that
owner-level negative; source presence alone receives no credit.

The adjacent updater `[0x18459,0x1856A)` (273 bytes) remains outside this
owner. Its Motion return-value lowering needs separate evidence; this
packet adds no register-based reconstruction for it. The new header uses
a short unique guard to avoid Borland's significant-identifier limit.

`main-b4ball-spawn-a` passes two fresh deterministic complete132-byte raw
comparisons and the empty original ordered relocation stream. The actual
new-ball damage0→1 mutation is compiled and rejected. Both complete functions
and132 instruction bytes are accepted, without DATA, BSS, tables or padding.
The separate273-byte updater remains unimplemented and uncredited.

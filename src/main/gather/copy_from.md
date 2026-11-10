# Original near-Pascal bullet-template copy from Gather

`set_bullet_template_to_gather_template(gather_t near&)` copies the
live Gather's 14-byte embedded BulletTemplate at offset 24 back to the
foreign global `bullet_template` at DS577E. The preserved ReC98
`th04/main/gather.cpp` names the original `copy_near_struct_member()` operation
with `prepare_di_si`, which determines the reverse DS-to-ES register order.

The complete native MAIN callback at `[17087,170A2)` preserves BP, SI and DI,
sets ES=DS, copies seven original 16-bit words with `REP MOVSW` and returns
using the original near-Pascal `RET 2` convention. Its assembler source is
`copy_from_bullet.asm`; shared semantic sizes are in the already maintained
`copy_to_types.inc`, while all globals and foreign segment providers remain
source-free. No synthetic CODE, image data, entity state, extra animation
behavior or altered interface is added.

The original address `17087` is **odd**. The source and source-free
`GATHER_COPY_FROM_TEXT` SEGDEFs therefore use `byte` alignment. Inheriting
`word` alignment from the distinct even-address forward copy would shift
both the function and DGROUP by one byte; no artificial padding is allowed.
With the authentic byte-aligned code segment, the two independent real
TASM32/TLINK producers match **27/27 original bytes**, the unchanged empty
relocation list, public and MAP bounds, and the original MAIN03/DS frames.
A compiled semantic negative reduces the genuine seven-word copy to six and
is rejected. Focused receipt:
`.analysis/gpt-web-main-gather-copy-from-asm-b/receipt.json`.

This grants only 27 **reviewed source-backed ASM instruction bytes**. The
separate previously accepted 27-byte forward copy is not counted twice, nor
is the retained ordinary C++ assignment retrospectively claimed exact.

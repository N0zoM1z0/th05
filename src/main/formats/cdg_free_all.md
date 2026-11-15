# `cdg_free_all()`: release every CDG slot (ASM)

`cdg_free_all.asm` frees the 64 CDG slots from 63 down to 0 by calling
`cdg_free()`, preserving SI, and returns far Pascal. It is 14 bytes at MAIN
`[1526E,1527C)`, following ReC98 `th04/formats/cdg_load.asm`.

`cdg_free()` is in the same code segment, so the call is `PUSH CS` followed by
a near call, which keeps the far return frame `cdg_free()` expects.

- TASM paragraph-aligns the `SHARED` segment by default, which put the entry
  two bytes late. The source declares the segment with BYTE alignment.
- A C++ version compiled to 23 bytes: a BP frame, an extra jump into the loop,
  an `OR` test, and the linker's far-call relaxation.

The same source is used for OP and MAINE; see
[cdg_free_all_op_maine.md](cdg_free_all_op_maine.md).

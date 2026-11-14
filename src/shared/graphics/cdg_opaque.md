# Opaque CDG plane drawing — exact C++

`cdg_put_noalpha_8(left, top, slot)` is far Pascal (RETF 6). MAIN `[14C70,14CD6)`,
OP `[D590,D5F6)` and MAINE `[EA74,EADA)` each contain a 102-byte copy:
100 instruction bytes, an explicit `nop` after `cld` at +75, and a trailing
alignment NOP at +101. There are no relocations. ReC98 builds the same
`th04/formats/cdg_p_na.cpp` into all three TH05 binaries.

`cdg_opaque.cpp` follows that source. It pushes the E/G/R plane segments,
derives the bottom-left destination with a signed `>> 3`, and keeps the dword
width in BP and the row stride in a register variable (DX). It switches DS to
the color planes and copies every plane with `rep movsd` rows from bottom to
top, popping the next plane segment into ES. ReC98's `REP MOVSD` opcode emits
are replaced by real inline `rep movsd` under the `tcc-s-tasm32` pipeline.
Both NOPs are compared and uncredited.

All three artifacts pass two producers, and the compiled 4→3 plane-count
negative is rejected. Receipts are under
`.analysis/unit-replays/claude-cdg-opaque-{main,op,maine}-20261114/`.
These functions replace the earlier reviewed-ASM owners, which wrongly
treated the BP-as-width register protocol as proof of hand-written assembly.

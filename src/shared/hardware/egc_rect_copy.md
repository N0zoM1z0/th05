# EGC page-1-to-page-0 rectangle copy — exact C++

`egc_copy_rect_1_to_0_16(left, top, w, h)` is far Pascal (RETF 8). OP
`[E2D8,E354)` and MAINE `[F402,F47E)` each contain 123 instruction bytes and
one trailing alignment NOP. The only relocation is the far `EGC_OFF` call at
+116. The accepted `egc_rect_setup()` (ReC98 `egc_start_copy`) follows directly.

`egc_rect_copy.cpp` follows the TH05 branch of ReC98 `th04/hardware/egcrect.cpp`.
It sets the EGC ROP, computes the 16-dot destination word with signed `>> 4`,
and stores the word count in the foreign `egcrect_w`. BP holds the row stride.
Each word inside page 0 (`0 <= DI < 32000`) is read on access page 1 and
written on page 0. The store must be a plain far-pointer assignment:
`poke()` makes TCC route the value through two stack temporaries. The
parameters are loaded with inline `mov`, as in ReC98, to keep them out of SI.

Two producers per artifact match all 124 bytes, and the 400→399-row plane
limit negative is rejected. Receipts:
`.analysis/unit-replays/claude-egc-rect-copy-op-20261114c/receipt.json` and
`.analysis/unit-replays/claude-egc-rect-copy-maine-20261114/receipt.json`.
These functions replace the earlier reviewed-ASM owners.

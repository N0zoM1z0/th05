# Exact .PI masked-row EGC setup in OP and MAINE

`pi_mask_setup_egc_and_advance()` is a complete 65-byte near C++ function in
both decoded executable images: OP `DD97..DDD8` and MAINE `EF3F..EF80`.
It activates EGC through the actual far driver call, sets active/read planes,
ROP, address and bit length using ports `4A0/4A2/4A4/4AC/4AE`, then selects
one of four 16-bit scanline masks through the original `pi_mask_ptr` and
`pi_mask_y` globals. The mask is written to EGC register `4A8` and the
scanline index advances by one. The native ordered far-call relocation is
`[3]` in both targets.

Source follows pinned ReC98 `th05/formats/pi_cpp_2.cpp` with typed 16-bit
register accesses and actual PC-98 hardware `OUT` operations. The `MOV AX,0`
and `SHL AX,1` instructions are expressed semantically to preserve the
original operand width and register use. All mask data and the EGC provider
remain external; source supplies neither target bytes nor game assets.

Focused exact receipts, each with two independent positive TCC `-S`/TASM32/
TLINK producers, original full bytes and ordered fixups, and a rejected
source mutation that changes the scanline mask from 3 to 2:

- `.analysis/unit-replays/gpt-web-op-pi-mask-egc-setup-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-pi-mask-egc-setup-a/receipt.json`

This owner does not overlap the separately accepted masked row kernel or its
caller wrappers. No full cold replay was run.

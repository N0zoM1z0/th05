# OP's independent PC-98 video plane address bank

The decoded OP `[0FA84,0FA94)` contains four contiguous initialized
32-bit *far memory addresses*, with offset zero and PC-98 segment words
A800/B000/B800/E000. These are the four standard blue/red/green/extended
video-memory planes, not image data. The OP source path owns a distinct
16-byte hardware configuration contribution from the separately accepted
MAINE owner, although both compile the same semantic segment definitions.

The natural C source declares four individually named `unsigned char far *`
objects using the standard PC-98 video segment selector expressions in
`src/shared/hardware/vram_plane_frames.h`. Those names are maintained
hardware roles; the original OP disassembly includes its low-level
`libs/master.lib/grp[data].asm` hardware DATA context. No claim is made
that OP originally included the separate TH05 MAINE hardware header or
that the old global symbol alias was emitted by this C unit. Four-byte
physical far-pointer widths and total 16-byte extent are asserted.

The native OP binder preserves code group op_01 `A390`, shared frame
`D300`, and DATA `0EFE:0AA4`. It provides no candidate instruction or
address value; the original downstream DATA suffix is symbolically
reserved after the contribution to satisfy the original DOS MZ initial
SS:SP allocation floor (as established for OP's accepted sound-priority
DATA). The scoped replay
`.analysis/unit-replays/gpt-web-op-vram-plane-frames-a/receipt.json`
passes two native Borland C producers with complete 16-byte raw/OMF/MAP
DATA identity and no ordered relocations. Changing the green plane
physical segment from B800 to B810 is compiled and rejected. The two
following unknown bytes and the next already accepted OP setup data
remain outside this ownership claim.

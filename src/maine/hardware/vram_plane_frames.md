# MAINE PC-98 video plane far-pointer data

The exact original MAINE `[1082E,1083E)` DATA band contains **four
independent 4-byte far pointers**, each pointing at offset zero of a real
PC-98 graphics plane. The source exposes the actual C publics
`VRAM_PLANE_B`, `VRAM_PLANE_R`, `VRAM_PLANE_G` and `VRAM_PLANE_E` and
generates their bit patterns from the hardware segment constants
`A800`, `B000`, `B800`, `E000`. These selectors are real PC-98 planar
video memory, not copied sprite bits, VM instructions or ordinary user
configuration. The original ReC98
`th05/hardware/vram_planes[data].asm` defines all four in this order.

The native C type `unsigned char far *` has an asserted four-byte large-
model pointer representation. An ordinary constant expression constructs
each `[offset=0,segment]` far address and the Borland compiler emits the
complete contiguous 16-byte initialized DATA. The original ASM additionally
had a `_VRAM_PLANE` alias for the first dword: this individual-unit C
producer declares the four individual names, not an unproved extra
linker public for the alias. No additional game DATA or imported image
allocation is included.

The outside-only binder has the real MAINE frames group_01 `A540`,
SHARED `E800`, DATA `10110:071E` and provides no address bytes inside the
unit. The scoped receipt
`.analysis/unit-replays/gpt-web-maine-vram-plane-frames-a/receipt.json`
passes two original-size Borland C producers, raw equality of all 16 bytes,
full OMF/MAP initialized-DATA scope and the empty original ordered fixup
stream. Mutating the blue-plane physical segment `A800→A810` genuinely
changes initialized DATA and is rejected. The preceding unreviewed DATA
and following original control state remain outside the claim; no entire
MAINE or unrelated unit replay was run.

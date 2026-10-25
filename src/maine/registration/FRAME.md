# Registration frame candidate

`maine-registration-frame-a` passes all40 bytes, both original ordered
fixups, two fresh deterministic producers and its wait1→2 negative. The real
Borland `outportb` API emits the original page I/O instructions directly.
No instruction ASM or register alias is used.

This independent natural C++ owner covers the complete original MAINE function
`[0xBD1E, 0xBD46)`: 40 instruction bytes, ending in a plain near `RET`.
There are no instruction NOPs, direct branches, padding or CODE-data tables.
The literal original MZ relocation order is `[16, 6]`; neither the original
order nor the original bytes may be normalized.

The source updates the sound controller, updates the glyphballs, waits one
frame, writes the current page to the PC-98 access-page port `0xA6`, replaces
that byte with `1 - page`, and writes it to display-page port `0xA4`. These are
ordinary C++ operations with a genuine hardware-I/O boundary, implemented using
Borland's real `<dos.h>` `outportb` macro/intrinsic. There is no instruction
assembly, physical-register algorithm, call-distance cast or padding directive.
The pinned TC4 header declares `__outportb__(unsigned, unsigned char)` and defines
`outportb(port, value)` as its void expression.

`registration_page` names the real initialized byte at original DS:`0x1521`,
whose original value is zero. It is foreign state here, not newly owned DATA.
The existing full `glyphball.hpp` is included unchanged. The real foreign
providers are `snd_se_update`, C far cdecl at `0x0E80:0x0320`;
`glyphballs_update`, near cdecl void at original `0xBE76`; and `frame_delay`,
C++ far Pascal taking one int, at `0x0E80:0x0A88` with `RET 2`. All callers of
this frame use near void with no arguments; no AL or FLAGS status is invented.

Original bytes and the complete boundary were checked from the retained
hash-attested decoded MAINE view. ReC98 commit
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05_maine.asm` `sub_BD1E`,
is secondary semantic evidence. Its reconstructed ASM producer is not proof of
original C++ source or original OMF record boundaries. The far-call addresses
in the reconstructed calibration differ from the original; the binder uses
the original frames and offsets. It supplies labels only outside owned CODE,
plus the foreign page byte. There is no fabricated helper body or stack.

The proposed independent owner is `maine-registration-frame`, module
`th05/r_frame.cpp`, segment `REG_FRAME_TEXT`, group `GROUP_01`, standard MAINE
compile context. The meaningful owner control changes `frame_delay(1)` to
`frame_delay(2)`. No compiler has run for this candidate. Fresh producer size,
full raw bytes, literal ordered relocations, OMF integrity and the compiled
negative must all pass before any acceptance or authored credit.

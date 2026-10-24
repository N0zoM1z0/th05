# Yumeko sword sweep

The complete original near function occupies MAIN load-image1F59C–1F6DD:
321 bytes and94 decoded instructions, without post-RET table or padding.
Its final RET at1F6DC immediately precedes the accepted final-ring prologue.
Original ordered MZ relocation sites are1F6B1,1F61D,1F5F8,1F5E9.
This native review and source presence are not an exact acceptance claim.

The natural algorithm alternates swords from the two playfield edges while
advancing the real boss2 Y coordinate. After a vertical sweep, it switches to
accelerating aimed bullet volleys, then restarts the sword wave. Difficulty
parameters retain their actual Pascal order: spread deltas24,16,12,10 and
sword spacing40,30,24,16. Gather colors are7,6. These values were derived from
the actual word stack order, not the visual low/high order of an ASM DWORD.

The source includes the accepted complete update.hpp interfaces unchanged.
It needs no additional records, scalar ABI views, Subpixel constructors,
class-return temporaries or pseudoregisters. All signed coordinates and byte
angles remain the genuine fields of Boss24, Sword26 and template25. The local
state aliases name real statebyte slots13–15, without adding globals or storage.

Foreign calls retain real original addresses and signatures: SELECT_FOR_RANK
0AE1:21A2, sound14AB:0232, RNG1527:0050, gather1705D, canonical class-valued
player_angle_from171CC, sword allocator1ED41 and regular bullets17204. The
pointer-bearing callbacks transitively declared by the accepted header remain
in their true group context, even though this owner does not use their bodies.

The private binder, unit/control proposal and native review are
`.analysis/yumeko-sweep-bindings.asm`,
`.analysis/yumeko-sweep-unit-proposal.toml` and
`.analysis/yumeko-sweep-boundary-review.json`. The meaningful negative increases
the volley speed reset threshold from6 to7 pixels per frame. No negative float
is quantized through an unsigned-byte helper.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` TH05 disassembly supplies
behavior corroboration; the original complete boundary, actual operands and
ordered relocations were independently read natively. No compiler body is
transcribed into assembly and no accepted source/header/core file is changed.

`main-yumeko-sweep-a` passes two fresh deterministic complete321-byte
raw comparisons and the complete original ordered fixups. Its own meaningful
source mutation is compiled and rejected. The complete function and321
instruction bytes are accepted, with no tables, padding, DATA or BSS credit.

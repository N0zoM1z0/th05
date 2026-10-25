# Current-note C++ candidate

`current_note.cpp` remains unaccepted. It follows ordinary C++ field accesses:
read the driver part pointer, cap the gate at four ticks, and return the note
only while remaining length exceeds both that gate and one tick. Otherwise the
result is the FFh rest byte. It contains no assembly, pseudo-register algorithm,
opcode emission, packed word alias or instruction template.

The complete native OP function is DA12..DA30 (30 bytes), CS 0D30, with 15
instructions, near RET, no NOP/table/padding and no ordered MZ fixup. DS:BX is
the address of a near driver-part pointer; DS belongs to the driver during the
call, not game DGROUP. The conventional fastcall declaration leaves the unused
AX/DX slots explicit and receives the pointer in BX. Native preserves BX and
returns the note in AL. No callback, storage allocation or new DATA is defined.

`pmd_part.hpp` describes the full candidate 98-byte QQ record from pinned
ReC98 b6ba5b0a's `libs/kaja/kaja.inc`, including its named tail through reserved
byte 97. It does not use the shortened 86-byte C++ view or a dummy prefix to
reach note byte 85. Compile-time checks establish the source layout: length at
4, gate at 5, note at 85, final reserved byte at 97 and total 98. These checks
passed the pinned compiler. They do not prove the actual external driver's
allocation extent, the historical source type, or signedness of unread fields.

The first natural compiler contribution is **51 bytes**, not 30. It loads the
two byte fields separately, stores the local gate in a stack slot, and adds an
ENTER/LEAVE frame and SI/DI saves. Native loads both fields together into AX.
No union, register template, prologue switch or whole-body ASM replacement is
introduced to force that encoding. The larger CODE contribution also shifts
the scaffold's subsequent DATA frame to 0F00; it supplies no new evidence for
native DS or driver storage. The size gate fails before a raw-byte verdict.

Only the first producer was compiled. There is no second positive, compiled
negative or accepted receipt. The private proposal is removed from the live
manifest; all 30 native bytes remain unknown, separate from the already accepted
neighboring piano ASM contributions. Failure to reproduce the compiler output
does not prove original ASM provenance.

Frozen inputs/arguments, OMF, MAP, MZ and logs remain in
`.analysis/piano-note-natural/op-a/`. Its `first-producer-review.json` has
SHA-256 `fa2d7fca915378dc743bcc6872254cb98bd5ab40e945e164838158aa620b52b5`.
The independent full piano native/origin review is recorded in
[piano notes](piano.md). No accepted source dependency changed, and the installed
tool execution proof was reused.

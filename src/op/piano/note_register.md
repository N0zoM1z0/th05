# Exact PMD current-note lookup in OP

`piano_current_note_from()` now has a complete 30-byte Turbo C++ owner at
`[DA12,DA30)` in decoded OP, with its original near fastcall convention.
The incoming driver-part pointer is held in BX and refers to a pointer to
the full PMD QQ record. The function loads the neighboring remaining-length
and gate-time bytes together into AX, caps the gate at four ticks, and returns
the current note only when the remaining length exceeds both the gate and one
tick. Otherwise AL is the `FFh` rest sentinel.

The maintained C++ uses the complete `PmdPart` type and real `offsetof`
fields. Its explicit `PUSH BX`/`POP BX` preserve the original near-fastcall
register contract; normal Borland C++ did not insert them when using its
`_BX` intrinsic. Packing the two adjacent byte fields into AX avoids the
extra reloads and local variables of the earlier 51-byte conventional
candidate. No fake PMD record layout, inline instruction bytes or foreign
data are supplied.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-piano-note-register-a/receipt.json`.
Two independent direct Turbo C++/TLINK producers match all 30 original
bytes and the empty ordered fixup stream; reducing the maximum gate from
4 to 3 in source is compiled and rejected. The adjacent accepted piano
ASM helpers and 218/116-byte C++ initializer/renderer remain unchanged.

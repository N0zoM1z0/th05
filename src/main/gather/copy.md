# Gather template copies — exact C++

`set_gather_template_to_bullet_template()` at MAIN `[16F70,16F8B)` and
`set_bullet_template_to_gather_template()` at `[17087,170A2)` are 27-byte
near-Pascal functions that bracket the accepted `gather_add` code. Both copy the
14-byte `BulletTemplate` as seven words with `REP MOVSW`. They have no MZ
relocations.

ReC98's `th04/main/gather.cpp` writes these copies as C++ using
`copy_near_struct_member(..., prepare_si_di / prepare_di_si)`. The maintained
`copy_to_bullet.cpp` and `copy_from_bullet.cpp` use the same TH05 order: CX
first, then `push ds / pop es`, the two pointer registers, then the inline
`rep movsw`. TCC generates the BP frame and the SI/DI saves. Two producers
match all 27 bytes of each function, and the compiled 7→6 word-count negative
is rejected. Receipt:
`.analysis/unit-replays/claude-gather-copy-20261114/receipt.json`.

A plain struct assignment is not exact: it emits a `F_SCOPY@` far call.
These functions replace the earlier reviewed-ASM owners.

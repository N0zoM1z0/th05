# Complete native tile invalidation reset

The original MAIN `[BD24,BD38)` contains the complete `tiles_invalidate_reset()`
near function: 19 real instructions bytes followed by its checked single-byte
`EVEN` alignment NOP. It clears the same 50-by-32 unsigned dirty-flag map at
DS:4ADA as the independently accepted `tiles_invalidate_all()` that follows.
The original preserves DI, selects ES from DS, sets EAX to zero, and writes
400 DWORDs through `REP STOSD`. The normal DF=0 caller contract is preserved.

The maintained `invalidate_reset.asm` uses real register-level semantics from
ReC98 TH04's typed `tiles_invalidate_set_all(false)` rather than inserting
opcode byte arrays or claiming a historical source file. The foreign-only
binder supplies the original CS AE1, DS209D and buffer address, with no CODE
or stored flag values. The neighbouring nonzero fill remains a separate unit.
One NOP at offset 19 is compared but never counted as authored instructions.

The standalone focused replay
`.analysis/gpt-web-main-tile-invalidate-reset-asm-a/receipt.json`
passes both fresh TASM32/TLINK producers, exact 20-byte CODE and original empty
ordered relocations, true linked start/end, complete OMF/LEDATA and real DGROUP.
Its own 400-to-399-DWORD mutation compiles successfully, preserves the exact
function extent and is rejected by the strict raw comparator. Only **19
reviewed ASM instruction bytes** gain authored credit; the one checked `EVEN`
NOP does not. The existing accepted 22-byte all-dirty fill and its input files
were unchanged and were not cold-replayed.

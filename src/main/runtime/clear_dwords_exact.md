# clear_dwords(): DWORD zero-fill helper

`clear_dwords(void near *dest, unsigned int count)` at MAIN `CF62..CF79` is a
23-byte near Pascal helper written in assembly; ReC98's `th05_main.asm` has it
as `sub_E708`. It sets ES to DS, reads the destination and the number of
32-bit units from `SS:[SP+4]` and `SS:[SP+2]`, clears EAX and stores with
`REP STOSD`, preserving DI, and returns with `RET 4`.

ZUN landmine: it never clears the direction flag, so it relies on it already
being clear. The only caller is `stage_state_init()`, which passes each pool
as `sizeof(pool) / sizeof(unsigned long)`.

# js_start(): joystick detection

MAIN `363E..3668`, 41 bytes of assembly plus one `EVEN` NOP. Polls the PC-98
sound board status port `0188h` up to 256 times, then enables joystick input
in PSG mixer register 7 through `SOUND_I` and `SOUND_O` (at `247E` and
`2494` in MAIN), stores whether a joystick was found at DGROUP:03D0, and
returns far. Unlike master.lib's version, it doesn't search for a SAJ-98
board. OP and MAINE contain the same function at different addresses.

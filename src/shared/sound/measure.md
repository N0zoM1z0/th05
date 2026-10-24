# BGM measure query

Natural C++ follows ReC98 b6ba5b0a th05/snd/delaymea.cpp and the real
KAJA PMD/MMD measure protocol. Disabled music returns the original-1 sentinel;
AH5 queries the driver, with MIDI's original192 ticks for hardcoded4/4.
Only those real hardware input/output registers are explicit.

The complete function is decoded OP E0CE..E0F1 and MAINE F242..F265,
35 bytes each. Both actual source contexts use BINARY O; original frames are
D30/EFE and E80/1011 respectively. No CODE table, padding, initialized DATA,
BSS or external helper body is owned. `op-bgm-measure-a` and
`maine-bgm-measure-a` each pass two independent fresh raw/ordered producers,
deterministic compiler OMF and their own compiled MIDI-meter mutation4→3.
The later measure-delay wrapper is outside these accepted extents.

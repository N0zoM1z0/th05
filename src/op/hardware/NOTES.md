# OP hardware data

OP.EXE carries its own copies of three small data tables that MAINE.EXE also
has: the glyph fade-in masks, the title-screen PI fade masks and the four VRAM
plane pointers. Each is a separate C file because each sits at its own place in
OP's data segment.

The link scaffolds for these units reserve the rest of OP's data segment
*after* the table. Without that reservation the test executable's initial
SS:SP falls below the MZ minimum-allocation check.

Open question: the 32 zero bytes right after `PI_MASKS` (OP `[FA64,FA84)`)
and the two bytes after the VRAM plane pointers have no known owner yet.

# sparks_update(): move and age the sparks (original assembly)

`update.asm` walks the 64 active sparks. A removed spark becomes free; a live
one moves by `PlayfieldMotion::update_seg1()` (which returns the new point in
DX:AX), is removed when that point leaves the playfield (unsigned range
checks on X and Y), and otherwise gains 1 subpixel of downward velocity and
ages by one frame, expiring after 40 frames. Same algorithm as ReC98's
`th04/main/sparks.asm`.

Unlike `sparks_init()`/`sparks_invalidate()`, this loop uses the correct
count of 64.

The plain C++ version (`update.cpp`) compiles to 72 bytes instead of 76:
Borland merges the two `F_REMOVE` stores and copies Y into AX for its test.
A Y local with an early `continue` gives 84 bytes. That is why this function
is kept as assembly.

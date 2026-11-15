# Random ring readers (original assembly)

`randring_readers.asm` builds two identical families of readers, one in
main_01 (`randring1_*`) and one in main_03 (`randring2_*`). Each has three
entry points:

- `next16()`: the raw 16-bit word at the cursor,
- `next16_and(mask)`: that word ANDed with the argument,
- `next16_mod(n)`: the unsigned remainder of that word divided by the argument.

All of them read a word at `randring[randring_p]` (two overlapping bytes) and
then increment only the cursor's low byte, so it wraps at 256.

- ZUN quirk: at index 255 the high byte of the sample is the cursor's own low
  byte, because the cursor directly follows the ring.
- ZUN landmine: `next16_mod(0)` raises a divide error.

The argument-taking entries are near Pascal (`RET 2`) and read their argument
through BX from the stack. The NOPs between the entries are alignment padding.

Plain C++ did not reproduce the raw reader: a normal local compiles to 21
bytes, a register local to 15 with an extra DX-to-AX move, and a prefix
increment to 19 (see `randring_next.cpp`).

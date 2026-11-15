# Point popups: notes

Point popups are the numbers that rise from collected items. There are 200
white and 80 yellow 16-byte `pointnum_t` records (`lifecycle.hpp`; the same
record is also declared in `stage_state_init.hpp`): flag, age, current
subpixel X/Y, previous Y, pixel width, five little-endian decimal digits and
one padding byte. `pointnums_alive` holds near pointers to the surviving
records plus a terminating 0.

## What is built

| Function | Built from | Notes |
| --- | --- | --- |
| `pointnums_add_yellow/white` | `add.asm` | `add.md` |
| `pointnum_digits_set` | `digits_register.asm` | `digits_register.md` |
| `pointnums_init` | `init.cpp` + `init.inl` | |
| `pointnums_invalidate` | `invalidate.asm` | `invalidate.md` |
| `pointnums_update` | `update.asm` | `update.md` |
| `pointnum_put`, `pointnums_render` | `put.asm`, `render.asm` | `render.md` |

`digits.cpp`, `invalidate.cpp`, `lifecycle.cpp` and `update.cpp` are C++
versions that are not built. Of these, only `invalidate.cpp` compiles to the
original bytes.

## Init, invalidate, update order

In the original, init (11 bytes), invalidate (44) and update (111) follow each
other, with an alignment NOP after init and after update. The NOP after init
is outside the init unit. `lifecycle.cpp` compiles all three as one file to
184 bytes: no NOPs, the invalidation pushes both arguments straight from
memory, and the update gets a stack frame and different register allocation.

## `digits.cpp`

The plain C++ digit loop compiles to 96 bytes instead of 58: `ENTER`, both SI
and DI saved, the first-nonzero position, count and quotient in stack locals,
and separate DIVs for quotient and remainder. The original reuses BP as the
first-nonzero position once it has loaded both parameters and uses a single
DIV per power of ten.

# Original four-plane background snapshot state in OP and MAINE

Both programs store the same complete mutable 8-byte `bgimage_planes_t`
initializer: the four 16-bit `__seg` pointers for the PC-98 B, R, G, E
snapshot planes start null. Its actual native field addresses are:

| Program | B | R | G | E | Complete DATA extent |
| --- | --- | --- | --- | --- | --- |
| OP (DS `0EFE`) | `09E4` | `09E6` | `09E8` | `09EA` | `F9C4..F9CC` |
| MAINE (DS `1011`) | `06C2` | `06C4` | `06C6` | `06C8` | `107D2..107DA` |

These identities come from actual 16-bit native consumers, not just the
zero initializer bytes. The previously exact `bgimage_snap` producer tests
the first segment and writes all four after separate 32,000-byte allocations;
`bgimage_free()` checks/releases the same pointers, while the native
`bgimage_put_rect_16` renderer reads each field for source-plane access.
Both program images use those four exact DS offsets and the existing
canonical `bgimage_free.hpp` declares the full type and field offsets.

The new `bgimage_planes_initial.cpp` uses that canonical eight-byte C++
struct to emit one complete four-word `_DATA` LEDATA per program, without
CODE, relocation, foreign fields or extra initialization. Two independent
Borland/TLINK producers per program match all original eight bytes and the
empty ordered MZ relocation stream, with a compiled nonzero first-plane
negative rejected:

- OP: `.analysis/unit-replays/gpt-web-op-bgimage-four-planes-20261112-a/receipt.json`
- MAINE: `.analysis/unit-replays/gpt-web-maine-bgimage-four-planes-20261112-a/receipt.json`

The two distinct accepted units add **16 source-authored semantic C++ DATA
bytes**, not new instructions. The adjacent sound state and memory-budget
words retain their own accepted owners. No complete executable claim is made.

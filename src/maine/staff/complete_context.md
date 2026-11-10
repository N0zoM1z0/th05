# MAINE Staff: complete original-order scene, device transfer and controller

The maintained `staff_complete_context.cpp` compiles **20 genuine functions**
in original physical order from `[D31F,E801)`: the 17 Staff scene helpers
(4229 bytes), the two near-Pascal PC-98 bitmap-transfer procedures (43 and 83
bytes), and `staffroll_animate()` (991 bytes). A real independent linked
producer now reproduces **all 5346 raw bytes** and the original *unsorted,
literal ordered* relocation stream for the complete span. The last RET at E800
belongs to the controller; the one-byte WORD alignment at E801 is outside
all 20 owned functions and is not credited.

The source contains no duplicate function bodies. All 17 scene definitions
come from the existing canonical `body/*.inl` files. The controller's unchanged
C++ algorithm is shared by its standalone wrapper `controller.cpp` and the
full context via `controller_body.inl`. Both bitmap device procedures are
reconstructed in `bitmap_hardware_context.inl` using authentic CPU registers,
352-row/20-word `REP MOVSW`/`REP STOSW` loops, real E000/A800 plane changes,
GRCG modes and output-port shutdown, as preserved in the original ReC98
`th05/end/verdict_bitmap.asm`. Compiler-supplied prologue/epilogue
preserve SI/DI; manually saving them a second time had produced eight extra
bytes. This is *inline original-register assembly owned by a C++ compilation
unit*, not a claim that the hardware routine was written in ordinary C++ or
that historical assembler provenance is proven.

The earlier standalone 126-byte TASM test differed in three XOR opcode
*direction* encodings and relocation-record order. In the genuine combined
Turbo C++ object, the assembler inside TCC naturally chooses the native XOR
encodings. The two external GRCG calls also inherit the correct original OMF
FIXUPP partition. Neither the TASM object nor native bytes were patched.

The source-free `maine_staff_complete_context_bindings.asm` supplies only
real library providers, DATA/BSS public names and true original physical
frames. In particular, when `SHARED` naturally WORD-aligns after controller
E801 to physical E802, four earlier scene provider declarations require their
true original offsets **minus two** in that segment. This is an externally
visible address calculation, not executable padding or relocation rewriting.
It restores all earlier far calls without altering any CODE byte. The actual
MAP confirms original CS A54, SHARED frame E80 and DGROUP/DS 1011.

Three **new**, non-overlapping complete source-owned functions passed separate
focused replay runs, each with two fresh real Turbo C++/TLINK producers,
unaltered complete raw bytes, native literal ordered fixups and an own
compiled semantic negative:

| Accepted complete function | Original range | Exact bytes | Negative |
| --- | --- | ---: | --- |
| `verdict_bitmap_snap(size_t)` | `E3A4..E3CF` | 43 | 352→351 rows |
| `verdict_bitmap_put(size_t)` | `E3CF..E422` | 83 | TDW color 1→2 |
| `staffroll_animate()` | `E422..E801` | 991 | Palette blue 48→47 |

The provenance-aware compiler-origin tags distinguish C++ hardware-register
intrinsics from the ordinary C++ controller. All three share genuine source
context, but each receipt applies one complete native function boundary; no
partial-code, table, DATA or BSS credit is inferred. Receipt paths:

- `.analysis/unit-replays/gpt-web-maine-staff-bitmap-snap-43-20261110/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-staff-bitmap-put-83-20261110/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-staff-controller-991-20261110/receipt.json`

Alongside the already accepted 17 scene functions, the contiguous 20-function
source context now accounts for **5346 exact CODE bytes**. This turn adds
**1117 new bytes** (126 hardware inline-ASM-in-C++ and 991 ordinary C++),
without counting the previously accepted 4229 a second time. No full cold
replay of unrelated artifacts and no whole-MAINE executable claim are made.

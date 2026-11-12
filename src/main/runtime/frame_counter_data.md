# Complete original MAIN frame-history initializer

The original initialized DATA interval `[22892,2289C)` is a contiguous
**10-byte** group of genuine mutable frame counters. Its members have the
same identities and widths as the maintained accepted runtime declarations:

| Original DS offset | Type | Native variable | Original initialization |
| --- | --- | --- | --- |
| `1EC2` | `unsigned long` (32 bits) | `total_slow_frames` | 0 |
| `1EC6` | `unsigned long` (32 bits) | `total_frames` | 0 |
| `1ECA` | `unsigned int` (16 bits) | `total_std_frames` | 0 |

The frame loop at MAIN `AF8F` increments `total_slow_frames` as a 32-bit
accumulator and at `AF94` increments `total_frames`; the dialogue/STD
transition at `13A36` increments `total_std_frames` as a word. The already
accepted `GameExecl()` handoff reads all three at these exact DS offsets and
writes the corresponding resident statistics. This native instruction and
consumer provenance distinguishes these ten initialized bytes from unrelated
zero-filled or BSS storage.

`frame_counter_data.cpp` defines exactly these three normal C++ scalar
initializers. Its first diagnostic compiled successfully but pulled unrelated
CODE-segment declarations from the handoff API header into the large model,
causing TLINK's legitimate `Group MAIN_01 exceeds 64K` rejection. The final
DATA-only producer keeps the **same canonical C++ public symbols and types**
without including foreign CODE-segment declarations; it does not reserve or
emit CODE or additional state.

The focused strict replay at
`.analysis/unit-replays/gpt-web-main-frame-counters-data-c/receipt.json`
contains two independent original Turbo C++/TLINK producers. Both verify
one complete 10-byte `_DATA` SEGDEF/LEDATA at the target interval, all raw
bytes, original empty ordered MZ relocation stream, and native MAP bounds.
A compiled semantic mutation changes `total_std_frames` from zero to one and
is rejected. This accepts **10 new game-authored C++ initialized DATA bytes**;
no surrounding gameplay-loop instructions or already accepted handoff code are
recredited, and no cold replay of those unaffected consumers is needed.

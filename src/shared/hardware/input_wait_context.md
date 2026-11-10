# Complete TH05 held-input sampler and UI change wait

The two adjacent original MAIN SHARED functions are now independently accepted
from one original-order maintainable Turbo C++ translation unit,
`input_wait_context.cpp`. The pinned ReC98 `th05/hardware/inp_h_w.cpp`
provides the genuine source dataflow, and original `th05_main.asm` confirms
both source boundaries, PC-98 hardware operations and physical frames.

| Function | Original MAIN range | Exact bytes | Source mutation rejected |
| --- | --- | ---: | --- |
| `input_reset_sense_held()` | `150C8..150D8` | 16/16 | 1024→1023 port-delay loops |
| `input_wait_for_change(int)` | `150D8..15102` | 42/42 | 16-bit CPU ZERO→SIGN flag timeout check |

The first function calls the real SHARED reset and sense code through the
original `PUSH CS / near CALL` hardware ABI. It waits exactly 1024 iterations
of `OUT 5Fh,AL / LOOP` between samples, eliminating typematic-release
transients. These are genuine source-level Turbo C++ inline ASM operations,
not emitted opcode templates. The far return restores AX from the second
sense routine. A previously retained ordinary far-call-only 18-byte
candidate inserted two artificial TLINK relaxation NOPs and was inexact;
this source instead follows ReC98's actual near-with-CS call strategy.

The second function remains real C++ with an original BP-register countdown.
It first waits for all currently held keys to clear, then polls the actual
IRQ-owned `vsync_Count1` word for a frame change until input is pressed or the
nonzero timeout expires. The `FLAGS_ZERO` test is represented directly using
TC4's actual `_FLAGS & 0x40` intrinsic, which makes the final decrement use
the CPU zero flag and preserves the original 42-byte function without extra
memory accesses. Input sensing never fabricates a keyboard state, joystick
callback or delay guard; the adjacent input scanner is independently accepted.

The genuine MAIN context has `SHARED CS=14AB`, `DGROUP DS=209D`, preexisting
reset/sense entrypoints at `14FC2/14FCA`, and `vsync_Count1` at DS267A.
The source-free linker binder exports these foreign labels, the full native
physical prefix/suffix and original MAP/OMF bounds, with no implementation,
initialized DATA or intervening padding. Both functions have **zero original
MZ relocations** and no table or NOP ownership.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-input-held-wait-58-20261111/receipt.json`.
Each complete function has two independently compiled Borland/TLINK producer
rounds with every original raw byte and relocation matching, plus its own
compiled semantic negative. **58 C++-owned CODE bytes** are newly credited.
Earlier first-producer 18-byte failures in `input_held.md` are historical and
not counted; none of the three accepted BIOS scanners is recompiled or
credited again.

## 2026-11-11: OP and MAINE also source-exact

The same maintained original-order C++ module was independently compiled
for **OP** and **MAINE**, with only the genuine source-free physical segment
and DATA bindings changed. Both full functions are separately accepted in
each artifact, making the complete held-key and waiting code source-exact
across all three TH05 binaries:

| Artifact | Held scanner (16) | Input change wait (42) | CS / DS | VSync word |
| --- | --- | --- | --- | --- |
| MAIN | `150C8..150D8` | `150D8..15102` | `14AB` / `209D` | DS267A |
| OP | `E094..E0A4` | `E0A4..E0CE` | `D30` / `EFE` | DS2E4E |
| MAINE | `F208..F218` | `F218..F242` | `E80` / `1011` | DS1DCA |

For each of OP and MAINE both functions match every original byte and their
original empty relocation lists in **two fresh native Borland/TLINK rounds**.
Each additionally rejects its own compiled source mutation (1024→1023
settling delay and ZERO→SIGN CPU timeout flag). Their foreign reset/sense
entrypoints remain at OP `DF8E/DF96` and MAINE `F102/F10A`, exactly matching
the separately accepted 262-byte full BIOS input scanners; the source never
copies, reimplements or credits those scanners a second time. No synthetic
padding, unknown keyboard value, OMF rewrite, changed far ABI or initialized
provider payload is used.

Focused accepted receipts:
`.analysis/unit-replays/gpt-web-op-input-held-wait-58-20261111/receipt.json` and
`.analysis/unit-replays/gpt-web-maine-input-held-wait-58-20261111/receipt.json`.
Thus the **three binaries collectively gain 174 exact authored C++ bytes**,
without reclassifying the separately accepted 783 original-register ASM
instruction bytes of the three BIOS scanner families.

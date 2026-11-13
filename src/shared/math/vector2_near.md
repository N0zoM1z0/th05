# Near vector: exact source-language ASM, inexact natural C++

The complete MAIN procedure is 152DA..15311, 55 instruction bytes with no
table or MZ fixup. ReC98 b6ba5b0a th04/math/vector2n.asm places ENDP before
the following EVEN NOP at 15311; that separate byte remains unknown and is not
part of the proposed C++ contribution. The earlier 56-byte routing included it.

The real near Pascal interface takes a near reference to the canonical
four-byte SPPoint, a byte angle in a WORD stack slot and a signed WORD length,
returning with RET6. Both signed samples are loaded before either output is
stored. Signed products are arithmetic-shifted by eight, then their low words
are written to x and y. The overlapping foreign sine/cosine arrays and all
geometry identities are imported unchanged; no data or result buffer is owned.

The natural C++ attempt first emitted106 bytes, then92 after keeping samples
and coordinates in their actual word domains. On 2026-11-13 it was reduced
again to **67 bytes** by using the Borland `<dos.h>` pseudoregister interface
for the signed 32-bit products and the original byte-angle/table-offset
lifetime. The source contains no inline instruction text. It reads both
signed samples before either store and obtains the near result reference from
the actual Pascal stack slot `BP+8`, avoiding an unnecessary saved-SI pointer
local.

Two fresh independent native producers emit the same complete 67-byte
contribution and normalized OMF. The original ordered relocation stream is
empty in both. A same-extent source negative changes the fixed-point shift
from eight to seven and emits a different 67-byte contribution. The candidate
still differs from the original 55-byte function (only9/55 bytes match), so it
remains an inexact compiler-context experiment and receives **zero CODE
credit**. It is not promoted to an accepted unit and does not replace the
exact original-language ASM owner.

Evidence: `.analysis/gpt-web-vector2-near-67-results-20261113.json`, with
positive producers `.analysis/gpt-web-vector2-near-67-positive-a-20261113/`
and `...-positive-b-20261113/`. The earlier natural-source review remains
`.analysis/vector2-near-native-source-review.json`; the private proposal
remains `.analysis/vector2-near-proposal.json`. All accepted vector owners,
headers, C/C++ counts and ownership remain unchanged.

Review SHA-256:
`522ab7e042c6281f08cf84247377b2fb8f23812af9dc3cb64bcb27c954e9f2a3`.

## 2026-11-10 exact register-level near Pascal vector

A maintained original-language `vector2_near.asm` now reproduces the complete
MAIN `[152DA,15311)` **55/55 byte** function. The real preserved ReC98
`th04/math/vector2n.asm` supplies a true 16-bit near-Pascal algorithm using
32-bit signed `MOVSX`, `IMUL` and arithmetic `SAR`, not a guessed compiler
pattern or a target byte array. The function reads the signed length from
SS:BP+4, the byte angle from BP+6 and the near SPPoint reference from BP+8;
it saves BP and returns with `RET 6`. Both original sine and cosine samples
are loaded from the externally bound unmodified DS tables before the first
output write, and both signed products are shifted by eight before storing
their low words. The original following `EVEN` NOP at 15311 remains **outside**
this function and does not earn credit.

Two independent TASM32/TLINK producers match the entire 55-byte CODE,
original empty ordered relocation stream, original `main_03`/CS1527 and
DGROUP/DS209D framing, true MAP bounds and CRC-valid linked/OMF bytes.
Changing the real X-product shift to seven bits compiles a same-extent
negative that fails comparison. The exact receipt is
`.analysis/gpt-web-main-vector2-near-asm-b/receipt.json` and the pinned
native review is `.analysis/gpt-web-vector2-near-native-review-20261110.json`.
All 55 bytes gain **reviewed ASM instruction ownership**. The earlier natural
C++ 92-byte candidate is still inexact and is not reclassified or replaced.

## 2026-11-13 follow-up: stack and register-lifetime lowering probes

The best maintained pure-C++ diagnostic remains the **67-byte** two-producer
candidate above; it is not exact and earns no CODE credit. Three additional
natural-source directions were tested against the complete 55-byte leaf:

- Reading the signed length explicitly through `_BP + 4` still makes Borland
  canonicalize the parameter load to `MOVSX EAX,[BP+4]` followed by
  `MOV EDX,EAX`; combining that with direct pseudoregister products emits
  **76 bytes**.
- Loading the sine sample through `_CX` and then sign-extending to `_ECX`
  emits a word load followed by an EAX-based sign extension and another copy
  to ECX; the complete function grows to **78 bytes**.
- Marking the angle/length parameters `register` does not bind them to the
  native register lifetime. The ordinary-register form spills the long
  length and both samples, emitting **93 bytes**; the mixed pseudoregister
  form emits **84 bytes** and still routes the second product through EAX.

These are first-producer shape diagnostics, not acceptance attempts. They
show that direct stack spelling, a 16-bit CX staging value, and register
parameter hints do not reproduce the native `EDX` lifetime or direct
`MOVSX ECX,word` table load. No target bytes, inline instructions, artificial
barriers, or duplicate ASM credit were introduced. The retained 67-byte
candidate and its two positives/compiled shift negative remain the current
best natural C++ evidence; a better ordinary-source lowering is still open.

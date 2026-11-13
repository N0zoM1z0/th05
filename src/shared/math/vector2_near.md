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

## 2026-11-13 additional register-allocation probes

Three further ordinary C++ formulations were compiled as isolated native
shape diagnostics against the complete 55-byte leaf:

- Register-wide cosine, sine, length and product locals emit **106 bytes**.
  Borland spills all three inputs and both products into a 20-byte frame,
  reloads each operand for multiplication, and stores the results from the
  stack. Register locals do not bind the original EDX/ECX/EAX lifetime.
- Register 16-bit samples followed by explicit 32-bit pseudoregister products
  emit **102 bytes**. The compiler saves both SI and DI for the samples, spills
  the signed length, and still rewrites the first product through EAX before
  the second product. The extra callee-saved registers cost more than the
  original direct sign-extended table loads.
- A 16-bit register length local with explicit sign extension emits **80
  bytes**. It avoids the long-length stack slot but adds an SI save/restore,
  copies the sign-extended value from EAX into EDX, and still routes both
  products through EAX. The table-load order also differs from the native
  cosine-to-EAX / sine-to-ECX sequence.

All three are one-producer diagnostics only: none matches the original raw
bytes, and none supersedes the two-producer 67-byte natural-C++ result. They
reinforce the remaining compiler boundary: TC++ 4.02 does not expose a source
register-allocation construct that keeps the signed WORD parameter directly
in EDX, loads the two table samples directly into EAX/ECX in native order, and
uses the two-register multiply/shift sequence without copies. No inline
instruction body, forced output patch, padding or duplicate ASM credit is
introduced. The reviewed 55-byte original-ASM implementation remains the
sole exact owner.

The three fresh isolated producer directories are
`.analysis/gpt-web-vector2-near-register-wide-products-a-20261113/`,
`.analysis/gpt-web-vector2-near-register-samples-pseudoreg-products-a-20261113/`
and `.analysis/gpt-web-vector2-near-word-local-signextend-a-20261113/`.

## 2026-11-13: reordered table and split-product follow-ups

Three more isolated natural-source producers tested whether reordering the
cosine/sine loads and splitting the two multiply/shift expressions could keep
the original EAX/ECX/EDX lifetimes:

- Reordered cosine-first and sine-second loads with compound pseudoregister
  products emit **76 bytes**. Borland still stages the second table sample
  through EAX before copying it to ECX, and copies EDX into EAX for the second
  multiply. More importantly, the compound `>>= 8` on the unsigned DOS
  pseudoregister lowers to logical `SHR`, not the native signed arithmetic
  `SAR`; it is not a semantically equivalent candidate for negative products.
- Loading the length into DX and then sign-extending DX to EDX emits **78
  bytes**. The compiler sign-extends through EAX and copies EAX to EDX; the
  table loads and product lowering still introduce extra moves. The compound
  product shift again uses logical `SHR`.
- A signed 16-bit register local for the length emits **80 bytes**, including
  a saved SI, the same EAX-to-EDX copy, and logical shifts. It does not bind
  the source value to the original direct stack-to-EDX sign extension.

These are one-producer diagnostics, not accepted source or behavior models.
The output is longer than the 67-byte best natural C++ result, and the
unsigned-pseudoregister shift changes negative-product semantics. The complete
55-byte original ASM owner remains the only exact implementation; no
instructions, target bytes, padding or new CODE credit are introduced.

Producer directories:
`.analysis/gpt-web-vector2-near-reordered-split-products-a-20261113/`,
`.analysis/gpt-web-vector2-near-dx-word-then-signextend-a-20261113/` and
`.analysis/gpt-web-vector2-near-signed-register-length-word-a-20261113/`.

## 2026-11-13: exact 12-byte natural-C++ residual

The complete original byte stream and the maintained 67-byte C++ producer were
re-decoded side by side from the pinned MAIN image and two fresh producer
outputs. The original 55-byte procedure is compact because it uses each
native destination register as the direct output of its source operation:

```asm
movsx edx, word ptr [bp+4]
mov   bl, byte ptr [bp+6]
mov   bh, 0
add   bx, bx
movsx eax, word ptr [bx+CosTable8]
movsx ecx, word ptr [bx+SinTable8]
imul  eax, edx
sar   eax, 8
imul  edx, ecx
sar   edx, 8
mov   bx, word ptr [bp+8]
mov   word ptr [bx], ax
mov   word ptr [bx+2], dx
```

The natural C++ producer preserves the same Pascal stack ABI (`length` at
BP+4, angle at BP+6, result reference at BP+8), the same signed products,
`SAR` operations, output order and `RET 6`, but Turbo C++ lowers three values
through EAX:

1. Length becomes `MOVSX EAX,[BP+4]; MOV EDX,EAX` instead of direct
   `MOVSX EDX,[BP+4]` (**+3 bytes**).
2. The sine table value is loaded into EAX and copied to ECX before the cosine
   value is loaded into EAX. Native code loads cosine directly to EAX and sine
   directly to ECX (**+3 bytes**).
3. The second product is computed by copying EDX into EAX, multiplying and
   shifting EAX, then copying EAX back to EDX. Native code multiplies and
   shifts EDX in place (**+6 bytes**).

Those three compiler-lowering differences account for the complete **12-byte**
residual (67 versus 55). The original has no SI/DI saves, stack locals, table
or relocation. The natural candidate also has no extra table, relocation or
owned data; its extra bytes are register copies only. This is a precise codegen
boundary, not a source-ABI error or missing target context. The 55-byte
reviewed ASM remains the sole exact owner, and the 67-byte natural C++ attempt
continues to earn zero CODE credit.

## 2026-11-13: TCC `-S` pipeline and inline-MOVSX probe

The maintained 67-byte natural C++ candidate was also run through the
accepted far-vector-style TCC `-S` → TASM32 → TLINK pipeline with the genuine
`main_03` group and DS `209D`. It still emits **67 bytes**, with no fixups.
The full instruction stream is unchanged in shape: `MOVSX EAX,[BP+4]` then
`MOV EDX,EAX`; cosine/sine samples load through EAX with an EAX-to-ECX copy;
the second product copies EDX into EAX and returns the result to EDX. The
alternate compiler pipeline therefore does not reduce the 12-byte residual.

A second attempt tried to reuse the semantic inline `MOVSX` form accepted by
the adjacent far-vector C++ owners. In this near owner, TCC 4.02 `-S` rejected
all tested forms at the frontend's inline-assembly expression parser: a direct
`MOVSX EDX,[BP+4]`, a table `MOVSX EAX,[BX+CosTable8]`, and a table
`MOVSX ECX,[BX+SinTable8]` (including the clean single-segment/no-wrapper
variant). An explicit `_SinTable8` spelling is reported as undefined. The
same far-vector source form remains accepted in its own far-function TU; this
is a context-specific frontend result, not proof that all TCC inline MOVSX is
unsupported. No object was produced by those failed variants and none is an
acceptance candidate.

The TCC-S 67-byte producer is
`.analysis/gpt-web-vector2-near-natural-tccs-a-20261113/`; the failed inline
syntax matrices and their compiler logs are retained under the matching
`.analysis/gpt-web-vector2-near-inline-*-20261113/` directories. The original
55-byte reviewed ASM remains the only exact owner; no CODE or negative-control
credit is claimed by these diagnostics.

## 2026-11-13: near-context inline-MOVSX parser boundary

The 12-byte register-allocation residual was probed again by trying the same
semantic inline-386 forms used by the adjacent far-vector C++ source. In the
near Pascal translation unit, Turbo C++ 4.02 rejects `MOVSX EDX,word ptr
[BP+4]`, direct `MOVSX EAX/ECX,word ptr [BX+CosTable8/SinTable8]`, and
`MOVSX EAX,SI` at the inline-assembly expression parser. Adding explicit
instruction terminators and matching the far source's `extern "C"` table
declarations does not change the failure. The diagnostics stop before an
object is produced; they are not candidate outputs.

A paired control confirms that this is not a blanket prohibition on inline
assembly in a near function: an ordinary 16-bit `MOV AX,BX` inline statement
compiles in the same near Pascal/TCC-S context. The far-vector source still
accepts its two `MOVSX` table instructions in its genuine far Pascal context.
The observed boundary is therefore specific to the near-owner MOVSX forms,
not to all inline assembly, all 386 instructions, or the table symbols in
C++ generally.

The simple-MOV control is only a parser probe and emits a 27-byte diagnostic
contribution; it is not a semantic vector implementation. The 67-byte
natural-C++ source remains the best complete two-producer candidate, with
correct signed products, arithmetic shifts and empty ordered fixups. The
original 55-byte reviewed ASM remains the sole exact owner. No target bytes,
inline opcodes, artificial codegen barriers or duplicate CODE credit are
introduced by these probes.

Retained diagnostics:
`.analysis/gpt-web-vector2-near-inline-semicolon-a-20261113/`,
`.analysis/gpt-web-vector2-near-inline-table-semicolon-a-20261113/`,
`.analysis/gpt-web-vector2-near-inline-table-c-linkage-a-20261113/`,
`.analysis/gpt-web-vector2-near-inline-register-only-a-20261113/` and
`.analysis/gpt-web-vector2-near-inline-near-mov-control-a-20261113/`.

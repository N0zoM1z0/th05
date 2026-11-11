# Unaccepted TH05 far vector pair: Borland 386 register lowering

Original MAIN `[14AB8,14B58)` contains two far-Pascal vector functions: a
69-byte `vector2` body and one outside-body `EVEN` NOP at `14AFD`, followed
by the complete 90-byte `vector2_between_plus` body. The second calls the
real far `iatan2` at `_TEXT:1F3A`; the combined ordered MZ fixup list is
`[94]`. The signed sine/cosine tables at DS `041C` and `049C`, the external
far result references and the 16-bit Pascal stack cleanup remain foreign.

A true Turbo C++ 4.02 large-model candidate was compiled from the natural
ReC98 `th03/math/vector.cpp` arithmetic, using the original SI/BX/EAX/EDX/
ECX register flow and typed signed-word table reads. Actual standalone CODE
was **171 bytes** rather than the original 160. The compiler lowered each
signed table read to `MOVSX EAX,[BX+table]` followed by `MOV EDX,EAX` or
`MOV ECX,EAX` rather than the native direct `MOVSX EDX/ECX,[BX+table]`.
The unsigned Turbo C register intrinsic multiplication additionally generated
`SHR EAX,8` where the original uses signed `SAR EAX,8`. A signed expression
cast addresses that semantic issue, but does not fix the register load shape.

The pinned ReC98 code historically writes the two 386 signed-load operations
as emitted assembler bytes. A direct attempt to express these as semantic
inline `MOVSX` mnemonics was rejected by the pinned Turbo C++ parser; no
output-byte mutation, synthetic source function or raw instruction byte
stream was substituted. Actual diagnostic input and OMF/MAP/MZ are retained
under `.analysis/gpt-web-vector2-far-first/`; the private mnemonic experiments
are `.analysis/gpt-web-vector2-far-second-source/`.

**No accepted credit** follows from these semantic attempts. The interval
remains unknown in the live ownership map; the separately accepted near
vector helper and the independent `vector2_at` implementation must not be
recounted. A future candidate needs a source-language mechanism whose actual
compiler output produces the signed 386 loads and original full CODE/fixup
order without copying native instruction bytes.

## 2026-11-11: both far-Pascal functions now exact C++

The old 171-byte candidate above was a useful failed *direct* compiler
experiment. The key toolchain difference is that Turbo C++ 4.02 accepts
semantic inline 386 `MOVSX EDX,[BX+CosTable8]` and `MOVSX ECX,[BX+SinTable8]`
when generating `.ASM` with `-S`, even though its direct `-c` assembler
rejects the same mnemonics. Its unmodified generated assembly can be
assembled by the real TASM32 and linked by TLINK. The signed 32-bit
multiplication and arithmetic right shift remain ordinary C++ expressions.

Two separately maintained complete far-Pascal C++ functions are now exact:

| Original complete function | Source | Compared bytes | Original fixups |
| --- | --- | ---: | --- |
| MAIN `14AB8..14AFD`: `vector2()` | `vector2_far_direct.cpp` | 69 | `[]` |
| MAIN `14AFE..14B58`: `vector2_between_plus()` | `vector2_far_between.cpp` | 90 | `[24]` |

The original one-byte `EVEN` NOP at `14AFD` separates these two complete
functions and is **not authored by either**. The original sine/cosine table
storage at DS `041C/049C` and real far `iatan2` at `_TEXT:1F3A` are foreign.
Both sources preserve the original Pascal cleanup sizes (12 and 20 bytes),
far result references, signed multiplication, and actual EAX/EDX/ECX and
SI/BX/DX register interface. No opcode emission, artificial alignment or
binary bytes appear in the source. This is full source-backed C++ ownership,
not a retrospective promotion of the earlier inexact diagnostic.

Strict focused receipts:

- `.analysis/unit-replays/gpt-web-main-vector2-far-direct-a/receipt.json`
- `.analysis/unit-replays/gpt-web-main-vector2-far-between-a/receipt.json`

Each receipt contains two independent TCC `-S` / TASM32 / TLINK producers,
complete original raw-byte and ordered-fixup comparisons, actual MAP/OMF
scope checks and a compiled semantic negative that changes the byte angle's
high part. Both negatives are rejected. No full cold replay or affected old
compiler owner rebuild was needed.

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

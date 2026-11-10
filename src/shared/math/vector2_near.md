# Near vector candidate

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

This is an ordinary C++ attempt, following the existing conservative origin
review. The reference's unsupported inline 32-bit instructions do not prove
original handwritten ASM and are not transcribed. The first wide-local source
emits 106 bytes. The maintained source keeps samples and final coordinates in
their actual word domains and reuses one ordinary byte offset, reducing output
to 92 bytes. It retains both products before the stores and adds no checks.

Both successful single-producer diagnostics stop short of acceptance. Their
whole raw scopes differ from the original 55 bytes; ordered fixups remain empty.
The remaining differences include stack temporaries, index lifetimes and
register allocation. Larger CODE also moves the nominal harness DATA frame,
so no original whole-layout or device-execution claim is made. No second
positive, negative, new model or live manifest entry was produced.

Current diagnostic: `.analysis/native-producers/main-vector2-near-word-domain-a/`.
Complete native/actual/source evidence is
`.analysis/vector2-near-native-source-review.json`. The private proposal remains
at `.analysis/vector2-near-proposal.json`; all accepted vector owners, headers,
C/C++ counts and ownership remain unchanged.

Review SHA-256:
`522ab7e042c6281f08cf84247377b2fb8f23812af9dc3cb64bcb27c954e9f2a3`.

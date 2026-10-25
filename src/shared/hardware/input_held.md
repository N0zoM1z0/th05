# Held-input sampling candidate

`input_held.cpp` is unaccepted source. It expresses the two real FAR input calls
and return value in ordinary C++, retaining assembly only for the PC-98 port 5Fh
settling loop. It supplies no input-provider body or copied instruction bytes.

| Artifact | Complete native load range | CS | DS | Real reset / sense providers |
| --- | --- | --- | --- | --- |
| MAIN | 150C8..150D8 | 14AB | 209D | 14FC2 / 14FCA |
| OP | E094..E0A4 | 0D30 | 0EFE | DF8E / DF96 |
| MAINE | F208..F218 | 0E80 | 1011 | F102 / F10A |

Each native function is 16 bytes, returns a word in AX with RETF, and has no
instruction NOP or MZ fixup. It has no arguments. Both providers really return
far; reset clears two words and falls through into sense. Their complete shared
return lies before this wrapper. A fake independent reset RET or a near-returning
replacement would change that ABI. The declarations retain the actual shared
CS context and `samecodeseg` information without changing the FAR types.

MAIN's first actual compiler contribution is **18 bytes**, not 16. TCC emits
ordinary FAR calls; TLINK relaxes each to NOP / PUSH CS / near CALL. The two
actual instruction NOPs are at relative 0 and 12. Native uses PUSH CS / near CALL
without those bytes. Both generated calls resolve to the real providers, but
complete raw extent fails. The NOPs are linker relaxation with zero authored
credit; they are neither removed nor normalized. Actual OMF has word-aligned
SHARED CODE and empty word-aligned DATA/BSS, with only the real DGROUP GRPDEF.

The first size failure stopped the replay. There is no second producer, compiled
negative or accepted receipt. OP/MAINE binders are prepared but were not built;
the shared failed compiler context gives no reason to repeat it there. Proposals
are parked privately, outside all live exact-unit manifests. All three functions
remain unknown ownership and add zero authored bytes.

Candidate evidence is pinned ReC98 b6ba5b0a's `th05/hardware/inp_h_w.cpp` and
history 6e91c4f99aa7e883d3099702b3fbf3133b9455e3. The synthetic reference and
the failed C++ result do not independently establish historical original ASM.
The adjacent 42-byte wait function remains unknown and was not compiled.
The vendor KEYRESET delay idiom does not establish ancestry of this whole body.

Private frozen inputs, arguments, OMF, MAP, MZ and logs are retained in
`.analysis/input-held-natural/main-a/`. Its `first-producer-review.json` is
SHA-256 `628d468c2cccc200c98af4e63459dfbb621f3831ff9832633f87401215248996`.
The independent vector/input origin review is
`.analysis/vector-input-native-origin-review.json`, SHA-256
`c5533ad8c6319d7b47dc06ce1772aece7ef5d7ffb55802c845d0a6ab626fb424`.
Unchanged accepted objects and installed tool execution proof were reused.

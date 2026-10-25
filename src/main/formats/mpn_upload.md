# Bounded natural MPN upload candidate: no acceptance

`mpn_upload.cpp` expresses the complete two-page upload through ordinary C++
loops and the real video-page port operation. It loads the image bank, draws
four columns at X576..624 and 25 rows at Y0..384 on page 1 then page 0, resets
the image index for each page and releases the bank. It changes no accepted
source, header or object identity.

The native near Pascal function at E57C..E5C1 is 69 bytes, ends with RET4,
has no instruction NOP/table/padding and has ordered MZ fixups [12,32,61].
The following NOP at E5C1 is outside this function. The existing canonical
`int pascal near mpn_load(const char far *)` declaration is retained, including
its historical unassigned return value. No AX result is invented. All three
real far helpers retain their actual ungrouped _TEXT/CS0000 declarations;
the upload declaration follows in main_01. No shared first-declaration
context is changed or false near provider introduced.

The first setup attempt failed to assemble the symbol-only binder because
the genuine far labels lacked `ASSUME CS:_TEXT`. No C++ object was produced.
The corrected setup changes only that declaration and preserves the complete
C++ source, header and compiler options. Its first complete producer generated
94 bytes and stopped at the extent gate, before a second producer or negative.
The failed manifests and both original attempt directories remain private.

The valid actual OMF contains one complete 94-byte CODE contribution and
empty DATA/BSS. The compiler uses a local stack frame for page/image state,
an OUT DX,AL sequence and ordinary loop-entry branches. Its MZ order is
[86,48,13], also different from the original. The larger body shifts the fixed
foreign tail and paragraph frames; those changes are layout drift, not new
native addresses. No binding adjustment, flag/type/register/expression trial,
source byte emission or ASM promotion follows. Default incremental plans
exclude this failed candidate, and it grants zero authored exact bytes.

## Separate original-language limits

MPN_LOAD_INNER at 41B2..420E is 92 bytes with an ordinary far filename argument
and RETF4. Its raw DOS interrupts, DS swaps, BX stack access and SI/DI locals
do not independently distinguish handwritten assembly from compiler code with
interrupt intrinsics. The initial positive ASM inference was challenged and
withdrawn under the same policy as the deferred STD/MAP loaders. It stays
unknown; no assembly source or producer is made for it.

MPN_FREE at 420E..4225 is an ordinary 23-byte guard/release/clear/RETF function.
Its trailing NOP at 4225 is outside that function. It also stays C++/unknown;
neither its language nor unframed producer context transfers from the adjacent
accepted renderer. The separately reviewed 92-byte MPN drawing family at
4226..4282 and its existing acceptance remain unchanged.

Private corrective language review:
`.analysis/mpn-load-inner-origin-challenge-review.json`, SHA-256
`94dad4a514c5f193341b2eed459d99fa27f2efc268401fcb5e73f86eff0b88c7`.
Independent actual first-producer review:
`.analysis/mpn-upload-natural-first-independent-review.json`, SHA-256
`1eab9c38e39791578e9d3adef1f849696f9227d53c4d756a8a4504401fb3049e`.

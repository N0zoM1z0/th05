# Shared polar and vector arithmetic

Natural C++ adapted from pinned nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/math/vector.cpp`,
`th01/math/polar.hpp`, with the TH05 byte-angle specialization. The maintained
TH04 `src/shared/math` owner corroborates the arithmetic and compiler context;
its acceptance is not transferred. The real `SPPoint` and Subpixel identities
come from TH05's existing geometry declarations.

Each artifact has two complete functions: `polar` is 28 bytes and `vector2_at`
is 68. `polar` multiplies signed words in 32 bits and arithmetic-shifts by eight;
`vector2_at` masks the angle to a byte, indexes the real overlapping sine/cosine
tables and writes two adjacent signed subpixel coordinates. The register
variables are the compiler's DOS intrinsics, not an emitted instruction stream.
No table values are copied into source or the symbol-only scaffold.

| Artifact | Original decoded span | DS | Sine / cosine offsets | Receipt |
| --- | --- | --- | --- | --- |
| MAIN | `14E44..14EA4` | `209D` | `041C / 049C` | `main-vector-a` |
| OP | `D834..D894` | `0EFE` | `0590 / 0610` | `op-vector-b` |
| MAINE | `EC84..ECE4` | `1011` | `027A / 02FA` | `maine-vector-a` |

All 96 bytes per artifact match both fresh producers. There are no CODE tables,
padding or MZ fixups. Both functions end in their actual far Pascal returns,
cleaning six and ten argument bytes respectively. The compile-time mutation
changes `polar`'s shift from eight to seven, doubling its radius contribution;
the oracle rejects that actual changed output. No whole-program, table-data,
foreign context or packing credit is claimed.

The first OP scaffold omitted a stack and TLINK emitted invalid default stack
allocation. Only that uncredited scaffold gained a real 128-byte stack; its
fresh replay validates the resulting MZ before comparing the unchanged source.
MAIN and MAINE retained their already valid independent contexts.

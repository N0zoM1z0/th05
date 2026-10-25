# STD and MAP allocation release candidates

Two ordinary C++ functions are prepared without importing the loader bodies:

| Owner | Original MZ program-image interval | Code | Ordered MZ fixups |
| --- | --- | ---: | --- |
| `std_free.cpp` | `C7FA..C811` | 23 | `[14]` |
| `map_free.cpp` | `E606..E61D` | 23 | `[14]` |

Both actual functions consist of the complete allocation null guard, a word
argument to the real far Pascal `hmem_free`, a zero assignment to the original
segment variable and a near RET. The original six instructions were checked
independently in the supplied locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The pointers are genuine two-byte `__seg` allocation addresses, rather than DOS
file handles or four-byte far pointers. There is no carry-return protocol.

The STD segment is at DS `0F52`, the MAP segment at `4AD8`, and the original DS
frame is `209D`. The real library callee is `0000:291E`, with declaration
`void pascal far hmem_free(void __seg *)` and a two-byte argument. Both owners
belong to frame `AE1`/`main_01`. The MAP header contains all eight bytes and
the section record all320 bytes, including its genuine unused columns; the
source supplies no object fragments, field aliases or invented padding.

Natural source provenance is maintained TH04 `src/main/stage/std.cpp` and
`src/main/formats/map.cpp`. The canonical declarations are corroborated by
ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/formats/{std,map}.hpp`, `th05/formats/std.cpp`, and
`libs/master.lib/master.hpp`. Donor acceptance does not transfer.

STD retains the explicit initial `-k-` from pinned `th05/formats/std.cpp`,
which contains the actual release definition. The MAP source retains the
ordinary maintained donor options without a frame option. Initially copying
STD's `-k-` onto MAP had no independent producer-context basis; it was removed
before any compiler run. This correction follows provenance, not observed
code size, and the first actual contribution still requires verification.

Each RET is followed by an original90 byte, at `C811` and `E61D`. Those bytes
are observed and preserved outside the proposed function extents. Their
original object/padding provenance is not established here, and they receive
no source ownership or authored credit. No codestring directive or byte is
added to reproduce them. Each first producer must establish its entire actual
CODE contribution in MAP/OMF; a size other than23 is a failure requiring review,
not permission to skip an extra byte. The binders supply only the real foreign
callee, segment-variable labels and ranges outside each whole owner.

The previous276-byte census suggestion included two incompatible loader donors.
The original184-byte STD loader uses raw DOS reads, changes DS to its allocated
segment, performs three REPNE SCASB title scans, and has three MOVZX byte reads.
The reference expresses its parsing with pseudoregisters and emitted opcodes;
those bodies are evidence only and are not copied. The original68-byte MAP
loader likewise uses raw DOS reads and a DS swap, while the maintained TH04
donor uses master file APIs and frees at a different sequence point. Both
loaders are parked before compilation. A generic interrupt intrinsic alone
does not justify reconstructing their surrounding parsing/register algorithms.
No original-language classification or ownership exclusion is inferred.

The existing89-byte `main-enemy-std-run` owner is already accepted and remains
unchanged. These two candidates neither duplicate it nor change any accepted
header. No DATA, BSS, assets, file names or script contents are defined here.

`main-std-free-a` now accepts the complete23-byte STD function: two fresh
deterministic producers passed full raw bytes, the original ordered `[14]`
fixup and OMF checks. Its own compiled allocation-guard inversion was rejected.
STD source/header and the maintained binder are frozen accepted dependencies.

MAP remains unaccepted. `main-map-free-a` stopped at its first producer's
complete-contribution gate: ordinary natural source generated27 rather than23
bytes, with `PUSH BP; MOV BP,SP` and `POP BP` adding four bytes around the same
release algorithm. The shortened target's original producer context is not
proved. The larger function also shifts its fixed foreign context by four
bytes, so its actual segment-variable address is `4ADC` instead of `4AD8`;
this is layout drift, not new object-field evidence. No second positive or
MAP negative was compiled. The ordinary MAP source is retained unchanged,
without a `-k-`, register, flag or prologue retry.

Private proposals, independent native boundaries and artifact/source hashes
are in `.analysis/std-map-free/`. The actual MAP first-producer review is
`map-first-producer-review.json`. Neither parked loader receives credit.

# Resident-program entry candidate: unaccepted

`initialize.cpp` is a natural C++ reconstruction of ZUN's embedded `-S` entry
function. Its first real Borland producer emits **260 bytes**, while the complete
original function occupies **269 bytes** at outer file `0E8D..0F9A`, child COM
`04A9..05B6`. The nine-byte complete-boundary mismatch rejects this candidate.
It adds zero functions and zero authored bytes to accepted progress.

The native review is retained at
`.analysis/zun-resident-review/native-abi.json`. The entry is near cdecl,
`int main(int, const unsigned char **)`, with tiny near argument pointers.
The original has a twelve-byte local frame, saves SI/DI and returns AX status.
The compiler object's actual public is `_main`; there is no renamed entry or
assembler implementation.

Natural behavior follows the complete native control flow:

- Search for the nine-byte resident ID in an eight-paragraph allocation.
- Print the logo, clear graphics, and interpret options only for argc equal
  to two. Accept `-` or `/`, then `R`/`r` to remove or `D`/`d` to enable debug;
  trailing argument characters are not validated.
- Reject an existing resident or failed allocation; otherwise preserve the
  provider's ID area, clear bytes 10 through 127, and initialize configuration.
  Byte 9 remains outside the clearing loop.
- Free the allocation on configuration failure. On success, propagate the
  debug switch into the resident debug byte at offset 23.

The existing full 128-byte resident and six-/ten-byte configuration types are
reused. Native first declarations preserve near Pascal providers, including
segment-only pointers, six-byte cleanup for resident search/allocation,
two-byte cleanup for DOS output/free, and no parameters for graphics clear.
Semantic message arrays are external objects; no target-derived initializers
or fake strings are supplied or credited.

The source reference is pinned ReC98 `b6ba5b0a`: `th05/res_kso.cpp` includes
`th02/res_init.cpp`. The reference's three artificial barriers (`seg = seg`,
`argv = argv`, and `optimization_barrier()`) are omitted. Its reference-taking
ID helper workarounds are also not copied. Direct typed provider calls derive
ID length and paragraph count from the canonical structure. The source keeps
the real `#pragma option -2` before C/C++ tokens and compiles in tiny model.
The exact reason for all nine differing bytes has not been isolated; no
instruction gaps or padding are invented to compensate.

Only `.analysis/zun-resident/main-natural-a/` is evidence for this candidate.
The private wrapper includes the unchanged accepted configuration source and
then the new entry source, in the reference's original function order. It
invokes the pinned compiler once with
`-c -I. -O -b- -3 -Z -d -DGAME=5 -mt th05/zres.cpp`.
Its valid OMF `_TEXT` is 582 bytes: configuration starts at zero, `_main` at
322, and `_main` ends at 582. DATA and BSS are empty. This establishes the
260-byte complete compiler extent; it does not claim a new raw-byte comparison
for either function. OMF module, dependencies, object, source snapshots and
commands are retained in the private directory.

No link, second producer, compiled negative or acceptance import is needed
after this complete-size failure. The existing accepted 322-byte configuration
unit, its dependency identities and all other accepted evidence remain
unchanged. Continue by finding a justified original source/context difference;
do not add optimization barriers, dummy statements, ASM or padding solely to
force an exact result.

Independent semantic/OMF/input review is retained at
`.analysis/zun-resident-review/main-natural-review.json`, SHA-256
`38e43ebe9353838824ea727405e748a0259c2c5e041884c13a0b25b67eda7357`.
It found no semantic issue and confirms the zero-credit size rejection.
All 303 public tests and full CI pass with this source present.

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
The nine-byte gap is now isolated to three DOS message calls that the compiler
merges into a shared error tail. Other local-frame, argument and segment-pointer
operations agree in shape. No instruction gaps or padding compensate for them.

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
Historical public checks passed with this source present. That old test count
is not current progress and does not accept the entry; ordinary recovery needs
only the focused checks described in the current workflow.

A later targeted jump-optimization diagnostic applies the supported `-O-`
pragma before the entry's tokens, keeping the preceding configuration intact.
Its valid object emits322 bytes for configuration and262 for main, still
seven short. It does not eliminate the shared message tail. An initial
unsupported `-O-j` spelling fails the frontend and produces no object; the
cached compiler usage identifies `-O` itself as the jump-optimization switch.
Both attempts are retained under `.analysis/zun-resident/main-jumps-{a,b}/`.
No link, second producer or negative followed. The original260-byte source
profile is restored, with no accepted source or progress change from this trial.

## 2026-11-11: matched size is not matched code

Further focused Turbo C++ 4.02 experiments changed only the control-flow
structure of the three genuine error-return branches (bad option, resident
already present, and memory allocation failure), using C++ `goto` to a common
failed-status return. With jump optimization disabled using the supported
`#pragma option -O-`, four branch combinations (`011`, `101`, `110`, `111`)
compiled to the original **269-byte function size**. All were linked as real
COM programs with the original `C0T.OBJ` startup, the separately accepted
322-byte configuration function, genuine near DOS/resident provider positions,
and foreign message labels.

The resulting four complete 269-byte functions are **not exact**: each differs
in 183 original byte positions beginning with branch displacements around
`04DE`, because Borland sinks message printing to different shared tails.
The correct size therefore does not establish the original C++ control flow.
No original-data bytes, artificial optimization barriers or binary patches
were used. Source and OMF trials are retained under
`.analysis/gpt-web-zun-gotos-*`; linked full-function comparisons are under
`.analysis/gpt-web-zun-main-linked-*`.

This 269-byte ZUN main remains unaccepted. Its earlier 260-byte natural source
is unchanged and still expresses the resident installation/removal behavior.
The next useful work is to identify a historically meaningful branch-layout
or compiler-context difference, not to promote an equal-length producer.

## Later exact foreign-provider recovery

The complete source-backed Master `RESDATA_EXIST`/`RESDATA_CREATE` calls that
this natural resident entry invokes are now independently recovered and
compared at `05DA..0698` (190 bytes). See
[exact memory providers](resdata_native.md). These are original 8086 vendor
ASM, not substitutes for compiler-generated `main()`, and do not repair the
still-mismatched 269-byte entry.

## Subsequent complete foreign file I/O providers

Nine near-Pascal Master file I/O providers at `0698..0970` now have
independent, exact [vendor ASM source](file_family_native.md). The resident
entry's DOS-file callbacks therefore have real original-code definitions
rather than merely symbol addresses. This does not alter the C++ `main()`
control flow or accept its still-mismatched 269-byte scope.

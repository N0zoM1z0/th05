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

Thirteen near-Pascal Master file/DOS providers at `0698..09D6` now have
independent, exact [vendor ASM source](file_family_native.md). The resident
entry's DOS-file callbacks therefore have real original-code definitions
rather than merely symbol addresses. This does not alter the C++ `main()`
control flow or accept its still-mismatched 269-byte scope.

## Master GRCG clear helper also source-exact

The original 36-byte `GRAPH_CLEAR` immediately after the unaccepted 269-byte
resident entry (`05B6..05DA`) now belongs to the same complete native
[Master graphics/memory source](resdata_native.md) as resident search/create.
The `-S` vendor CODE has a continuous 1,056-byte exact interval from
`05B6..09D6`, but this adds no credit to the compiler-generated `main()`
whose error-branch layout remains unresolved.

## ZUN resident initialization data is now exact

The natural [320-byte `_DATA` contribution](semantic_data.md) defining all
actual startup messages, defaults and resident ID is source-exact. It is
compiled as readable UTF-8 → native CP932 with the real tiny-model DATA
placement, not copied from the target. The `main()` control flow itself is
still unaccepted; source and DATA evidence must not be conflated.

## Direct Japanese literal and complete DATA-context probe

A focused experiment replaced the named message arguments with the original
Japanese string literals from `th02/res_init.cpp`, then repeated direct
TCC `-c` and TCC `-S`/TASM compilation both with and without the complete
320-byte accepted initializer in the translation unit. Direct TCC still
produces a 260-byte main; the assembly backend still produces 273. The
message-definition linkage alone therefore does not explain the original
269-byte failure-branch layout. Private OMF evidence lives under
`.analysis/gpt-web-zun-main-inlineliterals-*`. The natural `main()` source
stays unchanged and unaccepted.

## Original C0T link context recovered separately

The actual C0T.OBJ startup at `0100..0367` and its `1650..16BE` initialized
DATA have [source-origin native acceptance](crt_native.md). This identifies
the true 18-byte `_INIT_` table and 84-byte BSS context omitted by earlier
symbol-only linkage. Both CRT and the adjacent accepted 322-byte
configuration function now link exact under that layout; the separate
**269-byte `main()` control flow remains unaccepted** and is not patched or
reclassified as vendor material.

## 2026-11-11: compiler optimization shape definitively isolated

A further **private diagnostic only** restored the three historical ReC98
`th02/res_init.cpp` optimization barriers *as experiment variables* and
relinked with the now-proven authentic C0T `_INIT_` table (`0012h` bytes) and
BSS (`0054h` bytes). Turbo C++ 4.02's real tiny-model `-c` compilation
produced the original **269-byte `main()` CODE extent** **only when all three
reference barriers were present**. With one missing, the direct-object entry
was 260, 263 or 266 bytes. A separate `-S`/TASM32 experiment always emitted
273 bytes regardless of the same barrier mask.

Under the correct preserved CODE/DATA linker frames, the fully linked
269-byte *experimental* `main()` matches **269/269 original bytes**, and the
original 615-byte C0T startup, 322-byte accepted `cfg_init()` and 320-byte
accepted semantic C++ DATA match as well. A second independent native `-c`
producer reproduced every one of those scopes. A real compiled negative
changed the `argc == 2` option-dispatch condition to `argc == 3`; it changed
exactly one original `main()` byte and left all other scopes unchanged.

The ignored, proof-local diagnostics are retained under:

- `.analysis/gpt-web-zun-barrier-matrix-*/` (all three-barrier mask profiles)
- `.analysis/gpt-web-zun-main-barrier-context-b/` (first correctly linked match)
- `.analysis/gpt-web-zun-main-exact-diagnostic-positive-b/` (second match)
- `.analysis/gpt-web-zun-main-exact-diagnostic-negative-argc/` (compiled negative)
- `.analysis/gpt-web-zun-main-exact-diagnostic-summary.json` (range-only summary)

**This is NOT an accepted game-authored C++ reconstruction.** The reference
calls these self-assignments / empty inline-function calls explicit
*optimization barriers*. Their purpose is to alter Borland's basic-block
merging, not to express game behavior, and adding them solely to obtain a
byte match would violate the oracle source-provenance rule. All artificial
barriers remain private and ignored; the committed natural C++ source
[`initialize.cpp`](initialize.cpp) remains unchanged and unaccepted.

Sixteen further compilations of genuinely empty lexical scopes, including
the historic `RES_INIT_BOTTOM` macro block and scoped individual error
handlers, all still emit the natural 260-byte `main()` with no instruction
credit. The remaining challenge is a historically credible control-flow
expression that naturally prevents the three erroneous shared print tails,
**not** compiler option selection, CRT placement, string encoding or a missing
native provider. The existing accepted config/C0T/Master/DATA scopes all
remain independent and current.

## Natural error-exit source spelling, native C0T context

Four additional **behavior-preserving C++ expressions** were compiled
with the actual tiny-model Borland TCC 4.02 `-c`, original C0T startup,
322-byte accepted `cfg_init()`, 320-byte initialized DATA and the
previously recovered resident symbol bindings. Each trial linked a
complete COM with TLINK and compared the 269-byte `main()` extent.

| Natural source form | Native TCC `main` | Raw original match |
| --- | ---: | --- |
| Comma-expression `return (dos_puts2(msg), 1)` | 259 B | No |
| Shared error message and single failure label | 271 B | No |
| Return Boolean predicates already guaranteed by each error path | 290 B | No |
| Inline error-printing helper returning 1 | 259 B | No |

The **271-byte shared failure label** is only two bytes over the
original, but still differs at 148 aligned positions in the complete
scope. None preserved the historical distinct error-exit basic-block
arrangement. This further localizes the unresolved problem to compiler
control-flow/code sharing; the original C0T/semantic DATA placement is
not the cause. These are native producer diagnostics in
`.analysis/gpt-web-zun-natural-return-*/`, generated by
`.analysis/gpt-web-zun-source-returns-20261111.py`. They receive no
C++ acceptance or partial byte credit. The maintained natural
`initialize.cpp` is unchanged; no artificial optimizer barrier was added.

## Natural error-label dispatch probes (2026-11-11)

Two further genuinely behavioral C++ changes were built through TCC `-c`
and linked against the accepted original C0T, resident DATA and config
context. Distinct `goto` handlers for the three print-and-return
failures generated a **261-byte** main; distinct handlers only for
already-present and out-of-memory generated **260 bytes**. Neither
matches the original 269-byte complete `-S` main, despite preserving
the status messages and return values. The compiler still shares
failure blocks. Private producer evidence is retained in
`.analysis/gpt-web-zun-label-probe-*/` and the corresponding
`.analysis/gpt-web-zun-label-probe-20261111.py` script.
These failed variants do not change the maintained natural source
or any accepted owner.

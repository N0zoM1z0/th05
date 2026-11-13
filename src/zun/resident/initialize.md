# Resident-program entry: accepted exact native reconstruction

**Accepted — 269/269 bytes, two independent cold producers.**

`initialize.cpp` is now the accepted natural C++ reconstruction of ZUN's
embedded `-S` entry function. The complete three-source context in
`main_context.cpp` emits the original **269 bytes** at outer file `0E8D..0F9A`,
child COM `04A9..05B6`, through two independent cold producers. The original
ordered relocation stream is empty and exact, the complete `_main` MAP
boundary is explicit, and a compiled semantic negative is rejected. This
adds one accepted function and 269 authored CODE bytes to the ZUN ledger.

The older 260-byte, 269-byte/17-mismatch and shared-tail experiments below are
historical rejected hypotheses. They remain useful compiler evidence but are
superseded by the accepted complete-context source and receipt.

## 2026-11-13: exact complete-context acceptance

The accepted unit is `zun-resident-main` in `config/exact_units.zun.toml`.
Its maintained source wrapper is `src/zun/resident/main_context.cpp`, in
original order: semantic initialized DATA, `cfg_init()`, then `main()`.
Only foreign CRT/DOS/resident/graphics symbols are provided by the
symbol-only `probes/units/zun_resident_main_bindings.asm`; it contains no
instruction or initialized-data directives. The source uses native CP932
compiler input and real TCC 4.02 tiny-model flags.

The focused receipt is `.analysis/unit-replays/42313e66afdf4c289bcf0b3fadee2794/receipt.json`.
It records two independently reproduced 269-byte scopes, exact original
bytes and relocation order, and rejection of the configured source mutation.
The accepted ledger is `config/accepted_units.zun.json`. The MAP oracle now
recognizes `_main` as the C entrypoint public while continuing to reject
arbitrary undecorated labels as function boundaries; 13 focused function-unit
tests cover that rule.

## Historical pre-acceptance semantic and ABI investigation

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

## Native 2026-11-11 success/failure control-flow probes (not accepted)

Four further **genuinely behavioral C++** rewrites of the resident `-S`
`main()` were passed through the original tiny-model Turbo C++ `-c` and the
real C0T/`cfg_init()`/320-byte DATA + TLINK source context. They changed only
control-flow arrangement, never target bytes, pointer arithmetic, data or
foreign implementation. The native original function is **269 bytes**.

| Natural original-behavior source form | Emitted `main` | Raw original match |
| --- | ---: | --- |
| Wrap resident initialization in `if(seg)`, place no-memory exit last | 260 B | No |
| Put `cfg_init()` success/return-zero path first | 260 B | No |
| Parse `argc` with a `switch` rather than an `if(argc == 2)` | 262 B | No |
| Invert debug-option check, handle invalid option first | 258 B | No |

In the first two cases the optimizer emitted the same 260-byte length as the
maintained natural source, despite the visibly different control-flow layout.
The `switch` produced two more bytes; the inverted debug check produced two
fewer. None reproduced the original three distinct failed-print call tails,
and none is accepted as a 269-byte source. This reinforces the earlier
isolation of Borland's basic-block/error-tail coalescing problem: trivial
success-path reordering, status-return spelling and conditional reversal do
not recover the historical branch layout. These experiments use no dummy
self-assignments or artificial optimization barriers.

All four real producer scripts, retained source closures, linked binaries and
result JSONs are under `.analysis/gpt-web-zun-natural-return-{create-success-first,
cfg-success-first,argc-switch,debug-invalid-first}/`; the reproducible runner
is `.analysis/gpt-web-zun-control-shapes-20261111.py`. The maintained
`initialize.cpp`, accepted resident DATA/CRT/config, and all other ZUN owners
remain unchanged. No partial CODE credit or whole-file exactness is claimed.

## Structured-error-exit native probes (2026-11-11)

Three further behavior-preserving control-flow forms were compiled by the real
tiny-model Turbo C++ `-c` producer, then linked with the accepted C0T,
`cfg_init()` and initialized resident DATA. The original `-S` `main()` is
269 bytes; the ordinary maintained candidate is 260 bytes:

| Source form | Native `main()` size | Full original match |
| --- | ---: | --- |
| `do/while(false)` around initialization, `break` to one failure return | 261 | No |
| Explicit integer status returned through a common exit | 276 | No |
| `switch` on resident-presence result before allocation | 272 | No |

These real control-flow changes still do not reproduce the original distinct
DOS error-print tails. No artificial barriers, copied machine instructions,
or changes to the accepted resident source were used. The kept local trial
runner is `.analysis/gpt-web-zun-structured-exits-20261111.py`; each linked
COM and `result.json` is under the matching
`.analysis/gpt-web-zun-natural-return-{do-while-failure,status-return,nested-presence-switch}/`
directory. The 269-byte natural C++ `main()` remains unresolved.

## Mixed control-flow and jump-optimizer experiments (2026-11-11)

Four further natural source-level option-dispatch and allocation branch forms
were compiled with the actual tiny-model TCC 4.02 producer, the original C0T,
`cfg_init()` and the accepted 320-byte semantic DATA. Only the resident entry
had `#pragma option -O-` (jump optimization disabled); the accepted prefix
kept its original compiler settings. Results versus original 269-byte `main()`:

| Control-flow form | Emitted complete main | Native raw match |
| --- | ---: | --- |
| `switch(argc)` with `case 2` | 270 | No |
| Debug-option test with invalid condition first | 260 | No |
| Creation success path before memory-failure exit | 262 | No |
| Config initialization success path before error exit | 262 | No |

The 270-byte `switch` source remains very different from the original in its
complete branch layout; matching size or a near match is not useful without
exact original ordered bytes. None of these experiments used self-assignments,
empty helper calls or instruction fillers. They do not alter the maintained
`initialize.cpp` or its unaccepted status. Reproducible diagnostics:
`.analysis/gpt-web-zun-noopt-natural-flow-20261111.py` and the saved linked
`.analysis/gpt-web-zun-natural-return-*-no-jump-opt/` trials.

## Natural resident-presence and allocation nesting (2026-11-11)

Three further behavior-preserving `main()` arrangements were compiled with the
real tiny-model TCC, original C0T, accepted `cfg_init()` and the same 320-byte
DATA and TLINK frame. Their structure differs substantially from the
maintained linear error returns: (1) fully nesting successful creation and
initialization before the two failure exits, (2) allocating only in the
`!seg` branch with the already-present exit in `else`, and (3) putting the
successful path inside a nested `if(seg)` and sharing a bottom failure return.
**All three still emit 260-byte CODE functions**, rather than the original
269 bytes, with 150–154 positional mismatches in the original complete extent.
Borland therefore coalesces the common error-print tails despite these
meaningful control-flow changes. No dummy operations, optimizer barriers or
copied instructions are involved, and no source or original-target acceptance
has been changed.

Reproduce with `.analysis/gpt-web-zun-nested-real-branches-20261111.py` and
its three `.analysis/gpt-web-zun-natural-return-{nested-success-or-error,
absent-only-creation,shared-bottom-failure-return}/result.json` records.
This narrows the next investigation to the original compiler's construction
of distinct error-call tails; further equivalent outer `if/else` rearrangements
are unlikely to be productive without new disassembly or compiler evidence.

## 2026-11-13 natural control-flow recovery

A new source-only control-flow form now reproduces the complete 269-byte resident `main()` extent in a real TCC/TASM/TLINK producer build, with no inline assembly, self-assignment, or optimization barrier:

- `if(seg) goto resident_remove_success;` keeps the original success branch forward and places the not-found path first.
- The successful removal path jumps to `resident_success`, sharing the final zero-return tail with normal initialization.
- The not-found path retains its ordinary `dos_puts2()` call and failure return; compiler jump-tail sharing with the later file-failure path now matches the original bytes.

The producer comparison is exact for outer `ZUN.COM` offsets `0x0E8D..0x0F9A` (269/269 bytes), corresponding to child COM addresses `0x04A9..0x05B6`. This is a first-producer raw-byte result; the canonical two-round unit replay and acceptance-ledger entry remain pending.

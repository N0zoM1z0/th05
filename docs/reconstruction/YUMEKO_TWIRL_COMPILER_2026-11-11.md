# Targeted Yumeko native C++ twirl-branch diagnostics

Maintained source background: [swords_update.md](../../src/main/boss/yumeko/swords_update.md).

## 2026-11-11 additional contiguous Boss-source compiler probes

The maintained original-order MAIN03 cohort was rebuilt with one new
source variant at a time, using the true nine-function
`attacks_context.cpp` family and its existing native source-binding
object. This is a **targeted first-producer diagnostic**, not a complete
replay or an acceptance receipt. The baseline still emits 2,139 bytes,
with the updater contributing 283 bytes and its ordered relocation
unchanged; the full updater remains raw-inexact. Original updater
instructions at relative `+5E` and `+72` are respectively
`0F 8C AA 00` (`JL near +10C`) and
`0F 8D 96 00` (`JGE near +10C`).

The current ordinary `-O-` C++ instead emits a short `JL` to a local
jump proxy, then a short jump, and another proxy after the parity
branch. The original two long conditional branches jump directly
to the loop increment/tail. The baseline full function has 29
mismatching positional bytes despite its correct complete length
and relocations. The additional semantic-equivalent C++ controller
forms in this run produced these real combined CODE lengths:

| Compiler source form | Full MAIN03 CODE | Exact? |
| --- | ---: | --- |
| Maintained baseline | 2139 B | No |
| `switch(i & 1)` early-continue cases | 2154 B | No |
| Conditional sprite-index ternary assignment | 2153 B | No |
| Conditional comma expression using `(void)` | 2144 B | No |
| Odd-case early continuation with even-case fall-through | 2141 B | No |

The original native diagnostic script remains at
`.analysis/gpt-web-yumeko-newtwirl-probe.py`. Only the valuable 2,139-byte
baseline `.analysis/gpt-web-yumeko-newtwirl-baseline-native-a/`
is retained; other generated unsuccessful native snapshots were pruned.
Each trial used
temporary `swords_update_trial.cpp` and `attacks_context_trial.cpp`,
removed afterwards. **No fabricated branch, ASM replacement, acceptance
claim or partial C++ code credit** is introduced. The exact original
283-byte **reviewed ASM owner** and the accepted 354-/428-byte major
Yumeko attack C++ bodies remain untouched. Future natural-source work
should tackle branch-resolution/codegen structure rather than alter
the original gameplay twirl semantics.

## Additional true Borland first-producer flow trials

Three further source-level experiments used the exact original-order
nine-function Yumeko compilation cohort and real TCC/TASM/TLINK output.
Each changed only the updater's twirl branch and restored all trial
files afterwards:

| Source-equivalent branch structure | Complete MAIN03 CODE | Raw/ordered exact? |
| --- | ---: | --- |
| One-iteration `for` loop around sprite wrapping | 2143 B | No |
| `do/while(0)` with conditional `break` | 2143 B | No |
| Boolean guard expression with conditional sprite adjustment | 2152 B | No |

The real original combined contribution is **2,139 bytes**. These new
forms again introduce local short-branch proxies rather than the two
original 386 near-conditional jumps to the loop tail. Their full
function lengths, raw bytes and ordered relocations do not match, so
none provides a natural C++ acceptance candidate. The reproducible
probe `.analysis/gpt-web-yumeko-twirl3.py` remains; its old
generated native-output directories were removed during storage cleanup.
The accepted ASM and the
adjacent 354-/428-byte Boss attack C++ source are unchanged.


## Outer twirl dispatch rewrite diagnostics

Four further **semantic-equivalent** `swords_update()` source shapes were
compiled in the full original-order nine-function MAIN03 context with the
real Borland producer (no manually inserted instruction or barrier):

| Candidate control flow | Full combined CODE | Whole raw/ordered MZ |
| --- | ---: | --- |
| Early goto to ordinary sword motion | 2141 B | Inexact |
| Independent twirl-time conditionals | 2143 B | Inexact |
| Flattened `else if` parity dispatch | 2143 B | Inexact |
| Flattened parity dispatch with early `continue` guards | 2141 B | Inexact |

The original combined CODE is **2139 bytes**. In particular, the compiler
still emits local short conditional branches and proxy jumps rather than
the original pair of direct 386 near conditionals to the outer loop
increment. All runs were first-producer scoped diagnostics and preserved
the actual authored operands and sword behavior; no acceptance or machine
code owner was changed. The private
`.analysis/gpt-web-yumeko-twirl4.py` can reproduce these trials;
the superseded per-variant native build directories were deleted.

## Direct parity-tail C++ lowering trials

Four more whole-function source variants were compiled with the original
nine-function Yumeko TCC/TLINK context, using unchanged type definitions
and genuine sword twirl semantics. None is a source/byte acceptance.

| Trial | Real combined CODE | Ordered original relocation |
| --- | ---: | --- |
| Odd branch with early `continue`, even branch fall-through | 2,141 B | Changed |
| Parity inversion with explicit `even_twirl` goto | 2,143 B | Changed |
| Shared, genuine post-twirl `finish_twirl` label | 2,143 B | Changed |
| Even parity branch first, early `continue` in both arms | 2,141 B | Changed |

All four continue to lower the original direct **386 near JL/JGE**
branches into a short Jcc followed by proxy jumps. Original combined
CODE is **2,139 B**, with the 283-byte updater already owned by exact
reviewed ASM. The reproducible trial script is
`.analysis/gpt-web-yumeko-direct-tail-20261111.py`; historical native
build snapshots were pruned after their results were documented.
The maintained C++
port and adjacent accepted 354/428-byte major attack functions were
left unchanged.

## Isolating the Borland jump-optimization conflict

A focused original-order nine-function native compile identifies why the
current semantic C++ source cannot yet reproduce the original **283-byte**
sword updater. With the maintained `#pragma option -O-`, the combined
contribution is **2,139 bytes**, but the parity wrap guards lower to
short conditional branches and local jump proxies.

Enabling Borland's genuine jump optimizer (`#pragma option -O`) produces
the **correct two 386 near-conditional instructions** at updater offsets
`+5E` and `+72`, matching the original opcodes and branch locations:
`0F 8C` (JL) and `0F 8D` (JGE). However, the total combined CODE becomes
**2,135 bytes**. The optimizer also eliminates exactly two unrelated
two-byte short jumps: the bounds-check fallthrough at original `+9A`,
and the collision-hit continuation at original `+C2`. The loop tail
therefore shifts from `+10C` to `+108`, and all near-Jcc displacements
are four bytes shorter. This is a real code-generation tradeoff, not a
different sprite or collision algorithm.

The compiler option is **whole-function**, not a switch that can be
applied to the parity block alone. Moving `#pragma option -O-` back before
normal sword motion or collision restores the original 2,139-byte
baseline but also restores the wrong short-branch proxies. Equivalent
`else`, shared-label and collision-continuation rewrites under `-O`
still produce the 2,135-byte optimized shape.

The actual 2,135-byte optimized native comparison is retained at
`.analysis/gpt-web-yumeko-conditional-long-baseline-optim-native/`.
The probe `.analysis/gpt-web-yumeko-conditional-long-20261111.py`
can regenerate the other deleted trial snapshots. No game-source or
accepted ASM change was made. The remaining task is
to find historically plausible *natural C++ control flow* that
preserves both original short jumps while enabling 386 near conditionals,
without fake instructions or optimizer barriers.

## Six additional real optimized-flow C++ first-producer experiments

Six further **behavior-preserving** `-O` source variants were compiled in the
real nine-function Yumeko MAIN03 context: separate bounds checks, inverted
positive bounds gate, explicit collision `else` continuation, equivalent
collision-to-decay goto, direct removal on an out-of-bounds path and a
post-collision label. They are not accepted. Borland canonicalized all six to
the same **2,135-byte** combined CODE shape with correct 386 near `JL/JGE`
opcodes at sword-updater offsets `+5E/+72`, but still removed the original
two unrelated short jumps. Original target is **2,139 bytes**; original
relocation sites after the updater are displaced four bytes in all six
variants, so even preserving the opcode family cannot grant source credit.

The executable, source-cleaning one-producer diagnostic is retained in
`.analysis/gpt-web-yumeko-optim-flow-boss-20261111.py`, with actual native
builds under `.analysis/gpt-web-yumeko-optim-flow-*-first/` and the summary
`.analysis/gpt-web-yumeko-optim-flow-results-20261111.json`. All trial source
files were removed. No code or acceptance metadata was modified for the
unresolved natural updater; the previously exact reviewed ASM owner remains.

## Natural C++ switch-on-bounds and collision-state experiments (2026-11-11)

Three additional real Borland `-O`/TASM/TLINK first-producer experiments varied
**actual gameplay control-flow**, without artificial side effects, assembly
padding, optimizer barriers, copied target instructions or new runtime state:

| Semantics-preserving source representation | Combined original-order CODE | Original complete equality |
| --- | ---: | --- |
| `switch(bool(out_of_bounds))` with explicit `goto remove` | 2,148 B | No |
| `switch(bool(in_bounds))` with inverted removal dispatch | 2,148 B | No |
| `switch(sword->flag)` routing `F_REMOVE` to decay and other flags to collision | 2,141 B | No |

The real original nine-function context is **2,139 bytes**. Each alternative
compiles successfully and differs in the full original machine bytes and
ordered relocation positions. The boolean-boundary dispatches do preserve a
separate short branch around a bounds gate that plain `-O` had coalesced, but
at the expense of extra jump/condition encodings and a shifted collision tail.
The separate collision-state switch also changes the emitted branch layout
rather than restoring the native two short join jumps. These represent
**negative code-shape evidence**, not accepted C++ equivalence. In particular,
none replaces or claims the already accepted 283-byte reviewed ASM owner.

Runnable private diagnostic:
`.analysis/gpt-web-yumeko-natural-join-tests-20261111.py`, using the real
main_03 original-order producer and the unchanged pinned negative/positive
comparison. Corrected bounds-switch linked images and results are in
`.analysis/gpt-web-yumeko-natural-join-*-fixed-first/` and
`.analysis/gpt-web-yumeko-natural-join-results-fixed-20261111.json`;
the collision switch is under
`.analysis/gpt-web-yumeko-natural-join-collision-state-switch-first/`.
The first malformed bounds-switch source probes produced frontend errors and
were corrected before any size/code conclusion was drawn. All temporary
source inclusions were removed; accepted C++ and ASM bytes are untouched.

## Collision switch ordering cannot recover the two historical short joins

Four additional natural-C++ `-O` trials recompiled the actual nine-function
MAIN03 Yumeko source context, without changing player collision or sword
decay semantics. An enum-state `switch` putting the collision `default`
first, and another variant jumping from `F_REMOVE` directly to the decay
label, both produced **2,141 bytes** (original **2,139**). Switching on the
Boolean `flag != F_REMOVE` or `flag == F_REMOVE` instead emitted **2,150**
and **2,151 bytes** respectively, including an extra near conditional/jump
pair. All four complete original-byte and ordered relocation comparisons
failed. Therefore merely changing the `case` order, using an explicit decay
label, or switching on a Boolean cannot restore the two original short join
jumps that Borland optimizes away. The accepted 283-byte original ASM owner
and maintained C++ candidate remain unchanged.

Reproduce with `.analysis/gpt-web-yumeko-collision-join-variants-20261111.py`;
the real native builds and diagnostics are under
`.analysis/gpt-web-yumeko-collision-join-*-first/` and the compact result
file `.analysis/gpt-web-yumeko-collision-join-results-20261111.json`.
All temporary source-inclusion trials were removed after compilation.

## Six additional natural C++ branch-joining trials (2026-11-12)

The unresolved source-language `swords_update()` was retested in the **real
nine-function MAIN03 compiler context**, not against a hand-crafted
sword-only segment. Each first producer compiled a distinct natural,
behavior-preserving C++ rewrite under Borland's real `-O` optimization:

| Variant | Native compiler context size | Complete raw / ordered fixups |
|---|---:|---|
| Positively guarded in-bounds motion plus explicit success label | 2,135 B | No / No |
| Two-stage independent X/Y boundary guards | 2,135 B | No / No |
| Shared active-sword completion label after collision | 2,135 B | No / No |
| Y-hit failure guard and explicit no-hit exit | 2,135 B | No / No |
| Separate early continue guards for X and Y player overlap | 2,135 B | No / No |
| Single-iteration `do` loop with genuine collision exits | 2,135 B | No / No |

All six independently emitted the **same** lowered branch layout as the
original optimized baseline, including the correct 386 near JL/JGE opcode
families at updater offsets `+5E`/`+72`, but jumping to the shortened loop
tail at `+108` rather than the original `+10C`. The compiler still folds
the original short clip join at `+9A` and separate no-hit join at `+C4`,
removing two genuine two-byte jumps. Consequently the original whole
context is **2,139 bytes**, and all relocations after those deleted joins
remain four bytes too early in the compiled candidate. The first 283
candidate bytes' positional 143-byte comparison is affected by this shift
and is **not** a function-equivalence metric.

The fresh one-producer diagnostic script, source variants and summaries are
retained in the private `.analysis/gpt-web-yumeko-rejoin-20261112.py`,
`.analysis/gpt-web-yumeko-rejoin-results-20261112.json`, and the six
`gpt-web-yumeko-rejoin-*-20261112-first` directories. Each variant uses the
actual `src/main/boss/yumeko/attacks_context.cpp` with a temporary source
include, real pinned Borland TCC/TLINK, current target boundaries and the
original relocation order. Temporary source files were deleted after
compilation. **No** new C++ exactness, partial code credit, or negative
acceptance is claimed. The maintained inexact C++ source and separately
accepted 283-byte reviewed ASM Sword updater remain unchanged. Further
progress requires a real C++ control-flow expression that keeps both short
join jumps *and* the true near twirl conditionals without synthetic work,
bytes, or optimizer barriers.

## Four optimized genuine next-slot control-flow alternatives (2026-11-12)

The original-order nine-function Yumeko MAIN03 source was compiled in
four additional **actual pinned Borland/TLINK first-producer trials**.
Each variant changed only the natural C++ 283-byte sword update body,
used documented jump optimization `#pragma option -O`, and retained the
original gameplay result of every active sword's twirl, player hit,
out-of-bounds removal and decay. There are no manufactured side effects,
new runtime flags, `volatile` barriers, assembly opcodes or dummy calls.
Temporary `.cpp` sources were removed after every producer run and the
accepted reviewed 283-byte ASM owner is untouched.

| Genuine C++ source-flow form | Actual whole MAIN03 CODE | Matching original updater positions | Original ordered fixups |
| --- | ---: | ---: | --- |
| Named next-sword label for hit and miss | 2135 | 143/283 | Different |
| Keep immediate hit continuation; label only no-hit | 2135 | 143/283 | Different |
| Three real early X/Y/hit exits to one next slot | 2135 | 143/283 | Different |
| Shared normal next-slot exit after conditional hit | 2135 | 143/283 | Different |

The original **whole** nine-function CODE contribution is **2,139
bytes**. All four genuine native candidates canonicalize to the same
**2,135-byte** optimized output, recovering the two desirable original
near-conditional jump opcodes but eliminating the original two separate
short jumps. The updater's first optimized `JL near` at +5E has bytes
`0F 8C A6 00` rather than original `0F 8C AA 00`, and the `JGE near`
at +72 similarly has `0F 8D 92 00` instead of original
`0F 8D 96 00`. The missing four bytes shift the real loop tail and
later ordered relocation positions. Equal semantic behavior is **not**
a byte-exact acceptance or a substitute for a full second producer.

The reproducible first-producer script is retained at
`.analysis/gpt-web-yumeko-natural-nextslot-20261112.py`, with all four
actual source/OMF/MAP/MZ diagnostic directories under
`.analysis/gpt-web-yumeko-natural-nextslot-*-20261112-first/` and
machine-readable results at
`.analysis/gpt-web-yumeko-natural-nextslot-results-20261112.json`.
The canonical `src/main/boss/yumeko/swords_update.cpp`, its hashed
review evidence and both already accepted adjacent major Yumeko
C++ attacks remain unchanged. No new authored CODE is claimed; no
full cold replay was performed.

## 2026-11-12: local Y-decision switch probes (true nine-function context)

Three more **actual original-order Turbo C++/TLINK first producers**
examined a narrower hypothesis than the previous full-bounds or
whole-collision-state switch tests. Under the genuine `-O` jump optimizer,
which already recovers the native `0F 8C`/`0F 8D` near twirl conditionals,
the specific missing short joins are at original updater-relative `+9A`
(the final playfield-Y clip gate) and `+C4` (the no-hit continuation).
Each candidate rephrased *only* the relevant final Boolean as an ordinary
`switch (condition)` with exact, real `goto remove` or `continue` cases.
The collision and Y-boundary semantics, native DX:AX motion return,
real sword pool, and subsequent eight original-order functions were kept.

| New semantic C++ flow | Actual complete nine-function CODE | Raw/ordered exact? |
| --- | ---: | --- |
| Local `switch` on final Y clip predicate only | **2,150 B** | No / No |
| Local `switch` on final player-Y hit predicate only | **2,151 B** | No / No |
| Both local `switch` decisions | **2,164 B** | No / No |

The original full contribution is **2,139 B**; ordinary optimized C++ is
**2,135 B**. These switches prove that a local source-level dispatch can
make Borland retain an *additional* short jump after the corresponding
condition (`+A1` in the clip trial, `+BF` in the hit trial), but the
compiler also emits new case dispatch, shifts the other branches, and
adds **15 / 16 / 29 bytes** relative to its optimized baseline. The
whole updater and following real callbacks are therefore still inexact;
size or the presence of a familiar short jump is not accepted as a
partial machine-code match.

The runnable, source-cleaning diagnostic is
`.analysis/gpt-web-yumeko-local-switch-20261112.py`, with three immutable
first-producer output directories
`.analysis/gpt-web-yumeko-local-switch-*-20261112-first/` and structured
`.analysis/gpt-web-yumeko-local-switch-20261112-results.json`. All trials
use the actual `attacks_context.cpp` and the pinned original target rather
than a synthetic prefix. The temporary experiment source files were deleted
after compilation; **the maintained Yumeko C++ candidate, existing accepted
354/428-byte attack callbacks, and complete exact 283-byte reviewed ASM
updater remain unchanged**. No fake instruction, artificial optimizer
barrier, padded short jump, whole cold replay, or C++ byte-credit claim
was introduced. A next attempt needs a source-flow shape that naturally
retains both historical short joins *without* the switch-dispatch overhead.

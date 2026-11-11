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

The independent native diagnostic tool and compiler cases are in ignored
`.analysis/gpt-web-yumeko-newtwirl-probe.py` with result snapshots in
`.analysis/gpt-web-yumeko-newtwirl-*-native-a/`. Each trial used
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
none provides a natural C++ acceptance candidate. The ignored diagnostic
source and first-producer reports are under
`.analysis/gpt-web-yumeko-twirl3.py` and
`.analysis/gpt-web-yumeko-twirl3-*-native/`. The accepted ASM and the
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
code owner was changed. Inspect private outputs under
`.analysis/gpt-web-yumeko-twirl4-*-native/` and the script
`.analysis/gpt-web-yumeko-twirl4.py`.

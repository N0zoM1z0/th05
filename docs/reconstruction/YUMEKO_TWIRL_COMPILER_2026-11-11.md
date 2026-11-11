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

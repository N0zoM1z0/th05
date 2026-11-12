# TH05 MAINE final verdict bonus: actual resource and scoring formula

The complete source-defined **340-byte** `verdict_apply_bonus()` and
**1,748-byte** `verdict_main()` now share the same real starting-resource
domains from `bonus_scoring_rules.hpp`: lives 1..6 and bombs 0..2. The
bonus function retains the original six-way lives compiler dispatch
table, awarding a base bonus of **2,500 / 2,000 / 1,500 / 1,000 /
500 / 0** as lives increase. It then adds **2,500 / 1,500 / 1,000**
for starting bombs 0/1/2, a **2,000** bonus for normal/turbo mode,
three units per actual graze, and **200 × (misses − bombs used)**.
The original signed 32-bit total clamps to [0,10,000], then scales
by 100 before contributing to the final `skill` score and the exact
percentage UI. No new Resident fields, score accumulator, lookup
object, shortcut branch, game balance alteration or resource strings
are inserted.

The scoring driver also retains its original 1–6 and 0–2 switch keys
but defines those enum values from the same source-level settings.
Its completion-time, rank, high-score, cumulative penalties, second
comment seek and strict slow-play gate remain original; only the
readability/provenance of the shared starting-resource choices is
changed. Both complete functions still belong to the same genuine
10-function original `full.cpp` compiler context and keep their
unmodified far file/graphics ABI.

A first *real* Borland diagnostic emitted **339** instead of the
original 340 bonus-function bytes when `VBR_*` numeric macros were
inadvertently spelled as `2500L`, `2000L` and similar long constants.
The original C++ used ordinary `int` literals except for the
**signed `200L`** miss-minus-bomb term. Restoring the *correct source
literal type* in the semantic macros recovers the genuine codegen
and avoids an artificial helper or emitted machine-code padding.
Only the complete exact producer is accepted.

All **ten complete native function extents**, totaling **3,384 source
CODE bytes**, were recompiled twice with pinned Borland/TLINK and
matched raw bytes, 34 original compiler-generated switch table bytes,
actual MAP/OMF owner extents and the full original 50-site ordered MZ
fixup stream. The existing main completion-window mutation and new
compiled turbo-bonus mutation are both rejected. Verified receipt:
`.analysis/unit-replays/gpt-web-maine-verdict-bonus-rules-c/receipt.json`.
The prior size-mismatch probes remain unaccepted diagnostics. The
family was already accepted; no existing CODE credit is duplicated,
no full MAINE executable or cold replay is run, and no source string
pool is independently reattributed.

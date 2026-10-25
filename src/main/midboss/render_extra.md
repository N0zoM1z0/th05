# Extra-stage midboss renderer candidate

The complete original Extra renderer occupies `[DD2A,DD8F)` (101 bytes,
41 instructions), near frame `0AE1` with DS `209D`. It has two original ordered
fixups `[78,57]`, zero instruction NOPs, and no table, padding, DATA or BSS.
The separately accepted stage-five twin starts at `DD8F` and is not credited
again here.

Machine-code shape alone cannot distinguish the twins. The actual original
Extra setup instruction at `14A0D` writes `2F1A` to the midboss render pointer
at DS `C4B8`, selecting `AE1:2F1A = DD2A`. Stage-five setup selects `DD8F`.
Native review verifies this actual store, all complete returns and branches,
and both routing candidates rather than silently choosing the first match.

The natural body is literally identical to the accepted stage-five body, with
the real callback name and owning CODE segment changed. It uses the same full
22-byte midboss, real 64-pixel sprite geometry, scalar rolling conversion,
damage flash/reset and genuine defeat dispatcher. This source reuse transfers
semantics and type knowledge, not acceptance. Its own focused two-producer
replay and original relocation stream remain mandatory.

Accepted `render5.hpp` and providers are unchanged. The independent symbol-only
binder supplies true far master sprite calls and near scalar/defeat labels,
with all holes outside the complete 101-byte contribution. Actual OMF must
confirm that extent before the fixed tail is valid. The source contains no
assembler, bytes, pseudoregisters, register-allocation hints or fake helpers.

Private `.analysis/midboss-extra-render-boundary-review.json` includes native
boundaries, NOP checks, callback identity and source hashes.
`.analysis/midboss-extra-source-equivalence.json` records literal body equality
to the semantic donor. The private unit proposal uses a meaningful damage reset
0-to-1 negative. `python3 .analysis/extra-survivor-render-review.py` repeats the
bounded checks. This owner remains uncompiled and unaccepted.

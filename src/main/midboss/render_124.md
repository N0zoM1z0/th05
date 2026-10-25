# Stage 1, 2 and 4 midboss rendering candidates

Three complete original callbacks are adjacent in `main_01`, frame `0AE1`:
`midboss1_render` at `[DAE1,DBA1)` (192 bytes), `midboss2_render` at
`[DBA1,DC28)` (135 bytes) and `midboss4_render` at `[DC28,DCA7)` (127 bytes).
Native review decodes all 454 bytes as 177 instructions, validates each complete
return and all internal direct branches, and finds no tables or padding.

The owner reuses the unchanged full canonical 22-byte midboss and the accepted
stage-five renderer's real sprite, scroll and defeat interfaces. Stage one
draws its animated base layer and the phase-specific second layer; damage
flashing and clearing apply only to its phase-three layer. Stage two selects
the stationary or moving animation cadence after clipping negative Y. Stage
four adds its real `boss_statebyte[15]` silhouette condition to the damage flag.
All three route big-explosion rendering to the actual foreign defeat renderer.

Animation keeps signed integer promotion of the byte frame clocks. Scroll
conversion is a real near Pascal scalar-return API, not an aggregate returned
point or a CF predicate. Sprite functions retain their true far Pascal frame
zero ABI. First callback declarations capture their actual `main_01` context
before the canonical setup list. No accepted header, fake helper, raw-byte
array, assembly, emit or register-allocation hint is introduced. There is no
initialized DATA or BSS contribution.

The original ordered fixups are `[169,122,69]`, `[112,94]`, and `[104,86]` within
the three respective functions. Across the adjacent range the actual original
stream is `[169,122,69,304,286,431,413]`. This is a significant producer-context
fact: it must not be replaced with a globally reversed or sorted stream. The
private proposal therefore registers three complete C++ function scopes,
sharing one real source TU and one compile per producer round. It makes no
whole-454-byte ordered-fixup claim. Actual next MAP functions bound the first
two; the final compiler contribution end bounds stage four.

The independent symbol-only binder leaves the full natural code contribution
in place and supplies real sprite, scroll, defeat and DS labels only outside
it. Each ORG remains below 64 KiB. Its fixed tail is valid only after actual
OMF confirms the complete compiler contribution shape; no inside-function
padding can repair a different result.

Private `.analysis/midboss-render-124-boundary-review.json` records the target
and source hashes, full native boundaries, calls, branches, layout and distinct
original relocation streams. `.analysis/midboss-render-124-unit-proposal.json`
contains all three scopes and their own meaningful staged negatives: stage
one's phase-two base cel advances by one; stage two's moving base cel advances
by one; stage four's real silhouette state condition is inverted.
`python3 .analysis/midboss-render-124-review.py` repeats the bounded review.
The candidates remain uncompiled and unaccepted pending grouped two-producer
raw/per-function-ordered-fixup checks, OMF/MAP/dependencies and own controls.

The focused `main-midboss-render-124-a` replay passed all three complete
192-, 135- and 127-byte scopes from two fresh shared-TU producers. Each scope
matched every raw byte and its own original ordered fixup stream. The root
imported all three scopes, totaling 454 bytes. This is not a claim that the
whole 454-byte original relocation stream equals the new TU's stream; no
sorting or normalization occurred. Exactly one negative was compiled, owned
by `midboss1_render` and changing its phase-two base cel. Scopes two and four
share that oracle control. Their separately configured controls remain
available but were not compiled in this replay. The accepted C++, ABI header
and binder are frozen.

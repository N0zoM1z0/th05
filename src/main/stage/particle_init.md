# Stage-two particle initializer

The standalone natural C++ candidate owns exactly MAIN load
`11700..118EC`, one complete 492-byte near Pascal function taking the real
near reference to `s2particle_t`. Its actual RET2 ends immediately before the
separate accepted 653-byte update. All 186 original instructions are reviewed;
there are no native NOPs, compiler tables, padding or owned DATA/BSS. Original
ordered fixups are `[484, 441]` and must remain in that order.

The eight regions of the 4096-frame cycle choose the angle, compute the spawn
X position, add signed `IRand() % 8` jitter, reset zoom and Y, and obtain
velocity through the true far Pascal `vector2` API. This uses the frozen full
26-byte particle, canonical motion/Boss/custom-entity types and unchanged
actual API declarations from `background2.hpp`.

The retained 476-byte candidate already has the original single common X
store. Its entire sixteen-byte instruction-size difference is four in-place
compound shifts, each four bytes shorter than the original scalar-result
scale. The earlier 498-byte candidate independently had a six-byte named-X
spill/reload and four same-size signed multiplications. Those saved failed
producers remain unchanged; neither is accepted or relabelled.

This single candidate changes only four ordinary expressions from
`frame <<= 3` to `frame = frame * 8`. Each relative frame lies in `0..127`,
so signed multiplication is in range and preserves the algorithm. All eight
branches, angle writes, scalar locals, common jitter and actual foreign APIs
remain intact. There is no conditional-expression rewrite, named X surrogate,
register hint, physical-register alias, barrier, instruction body or flag
change. Code generation remains unproved before a focused producer.

`particle_init.cpp` is a genuine independent translation unit, guarded so the
coherent `background2.cpp` can include both this body and the unchanged accepted
`stage2_update.cpp` once. Its standalone source closure excludes the combined
parent and update body. No accepted header or update source was modified.
The new symbol-only binder supplies only actual RNG/IRand/vector2 addresses,
the real stage-frame word and holes outside this one complete contribution.
It supplies no update instructions, values, stack or padding.

Private `.analysis/stage2-init-factor-proof.json` pins the pre-factor snapshot
and shows that reversing exactly four scalar assignments restores the old
476-byte producer's function source verbatim. The original boundary review
and `.analysis/stage2-init-field476-diff.txt` preserve native evidence.
`.analysis/stage2-particle-init-candidate.json` proposes this whole492 scope
and a real compiled zoom mutation from 8 to 9 inside the new CPP. Full raw
bytes, original ordered fixups, two fresh producers and the independent negative
remain mandatory; no exact credit is claimed by this preparation.

Focused `main-stage2-particle-initializer-a` now passes two fresh complete492
byte producers, raw equality and original ordered fixups `[484,441]`, plus its
own rejected zoom8-to9 mutation. The four scalar rvalue assignments are the
only algorithm-expression changes from the saved476 body. The accepted
updater653 and shared full ABI header remain unchanged.

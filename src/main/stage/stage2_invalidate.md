# Stage-two particle invalidation

The complete MAIN function `[116CD,11700)` is51 instruction bytes, no NOP,
table, padding, relocation or owned DATA/BSS. Its end is the start of the
already accepted particle initializer. The old reference next-public distance
of543 was only a routing hint and included a large interval after the RET.

Natural C++ reuses the complete26-byte `s2particle_t`,12-byte Motion and64-slot
custom pool. It sets the canonical two-word dirty box to8x8, traverses all64
particles and invalidates each active particle's previous point. The actual
two-word Pascal y/x tile API is the same one used by the accepted TH04-derived
midboss invalidator. No shared header changes or instruction body is supplied.

CODE is near `0AE1`/`main_01`, DS `209D`. Dirty box is DS3502 and custom pool
DSB3F4. The tile helper remains foreign at `0AE1:0CC2`; symbol-only bindings
retain all actual empty segment group contexts.

`main-stage2-invalidate-a` passes two deterministic producers, valid OMF,
all51 raw bytes and the original empty relocation list. The shared compiled
width8-to9 control is rejected. Receipt:
`.analysis/unit-replays/main-stage2-invalidate-a/receipt.json`, SHA-256
`411d87a8be3ea0120654c259bc652b3eef129c3f5f8fe5a3f772e5f725a27745`.
Native boundary/type review: `.analysis/stage2-invalidate-boundary-review.json`.

## Exact shared Stage 2 particle footprint (2026-11-12)

The independently accepted complete 51-byte invalidation leaf now
uses the same compile-time 8-pixel particle tile-footprint definition
as the original eight-track particle initializer and Stage 2 update.
The true 25-frame/64-slot loop and original Pascal invalidation
interface are untouched, with original machine bytes, fixups and the
compiled footprint mutation rejected:
`.analysis/unit-replays/gpt-web-stage2-bg-three-code-scopes-a/receipt.json`.

# Stage-two orbit and attack helpers

Natural TH05 behavior is reconstructed in three complete functions, retaining
the accepted stage-two header and canonical Boss, midboss and template layouts:

| Function | Original MAIN load-image interval | Bytes |
| --- | --- | ---: |
| Orbit movement |15CC1–15D43|130|
| Stack and random pattern |15D43–15DB8|117|
| Final blue stacks |15DB8–15DEB|51|

The complete contribution is298 bytes and87 decoded instructions. Every
function ends in a true RET immediately before the next genuine prologue.
The first prologue at15CC1 is independently addressed by the stage-two update;
the previous stage-one semantic table ends at precisely15CC1. There is no gap,
post-RET switch table or alignment padding. The sole MZ relocation site is
15CE4, the segment operand of the genuine VECTOR2_AT far call14AB:03B0.

The orbit center is the full accepted four-byte SPPoint at DS3726. Its X speed
uses signed-char interpretation of the actual statebyte14; statebyte15 marks
radius contraction, and the actual velocity.x field holds the radius. The
position updates preserve whole-point assignment and the canonical external
vector interface. The two attack helpers retain the original frame-modulo
counters, near Pascal tuning callback, HP thresholds, and packed stack setters.
No foreign helper bodies, initialized DATA, assets or synthetic state are added.

TH04 maintained `src/main/midboss/m2_update.cpp` was reviewed for reusable
conventions, but its attack behavior differs. Pinned ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` TH05 disassembly and independently
read original bytes provide actual behavior and ABI evidence. Neither donor
nor reference acceptance transfers. No compiler instruction body is transcribed
into assembly, and there are no pseudoregisters, inert expressions or barriers.

The private original-boundary packet is
`.analysis/midboss-stage2-patterns-boundary-review.json`. The maintained symbol-only
scaffold is `probes/units/midboss_stage2_patterns_bindings.asm`; the private
focused entry is `.analysis/midboss-stage2-patterns-unit-proposal.toml`. The single meaningful
negative moves the orbit's left correction boundary from128 to129 pixels.
Source presence and native review alone provide no exact authored credit;
root must verify fresh producer pairs, original raw bytes and ordered fixups.

The root focused replay `main-midboss-stage2-patterns-a` subsequently passed
both fresh producers against all298 original bytes and the single ordered
relocation. The orbit-boundary128→129 negative passed. Root imported three
complete functions and298 authored instruction bytes. Source, header and
symbol binder remained unchanged after freeze.

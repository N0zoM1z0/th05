# Yumeko movement and first attack helpers

This natural C++ candidate reconstructs three complete original MAIN algorithms:

| Function | Load-image interval | Bytes |
| --- | --- | ---: |
| Random-direction bouncing movement |1EED5–1EF59|132|
| Alternately mirrored sword fan |1EF59–1EFEE|149|
| Red ring from random points around Yumeko |1EFEE–1F088|154|

The complete contribution is435 bytes and139 independently decoded instructions,
without inline tables or alignment padding. Every final RET immediately precedes
the next true prologue. The accepted stage-five setup binds the original Yumeko
update at1F782; its actual near call at1F8BC routes independently to movement
entry1EED5. Ordered MZ relocation sites are1F072,1F068,1F036,1EFBD,1EEF7.
Source presence and boundary evidence grant no exact authored credit: the root
focused producer pair and meaningful negative remain authoritative.

The behavior is recovered from the actual pinned TH05 target and ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` TH05 disassembly. Original anonymous
helpers receive semantic local source names; no claim is made that these were
original source identifiers. The disassembly is behavior evidence, not an ASM
instruction template. Motion uses normal signed coordinate arithmetic and
bounds, the fan uses the real unsigned angle and mirror state, and the ring
retains real gather timing, random origins, tuning and sound calls. There are
no pseudoregisters, emitted bytes, inert expressions or compiler barriers.

The full24-byte Boss,14-byte bullet template, geometry and canonical26-byte
custom slot are reused unchanged. The complete sword record is26 bytes with
every true field and unused scalar retained. Its template is genuinely25 bytes
and fits the26-byte slot; there is no invented trailing field. Both records
preserve origin/position2, twirl14, sprite18 and speed24 offsets, with the
entity's true unused scalar at25. Sixty-three swords occupy custom slots1–63,
while slot0 is the genuine template overlay. Full size/offset/pool assertions
verify this independently when compiled. Provenance is the complete reference
`th05/main/bullet/sword.hpp`, `th04/main/custom.hpp` and actual foreign sword
allocator/update operands; only the accepted single custom_t definition is used.

The external sword allocator at1ED41 remains a real near Pascal API, with no
helper body or credit supplied here. VECTOR2 at14AB:0008 takes two genuine far
references, a byte angle in its word Pascal stack slot and a word length.
VECTOR2_AT at14AB:03B0 uses the canonical near-point reference and four word
arguments. The far sound service, RNG, gather and tuning callback retain their
actual ABI and group frames. All parameter changes use integral quantized
values; this owner introduces no unsigned-byte helper for negative floats.

The private original-boundary packet is
`.analysis/yumeko-patterns-boundary-review.json`. The private symbol-only binder
and entry proposal are `.analysis/yumeko-patterns-bindings.asm` and
`.analysis/yumeko-patterns-unit-proposal.toml`. The single meaningful negative
moves the right bounce boundary from336 to335 pixels. No accepted/shared header,
core configuration or existing source is changed.


The first435-byte producer isolated two swapped gather colors in the ring:
the original Pascal packed argument requires(frame,7,6), while the candidate
passed(frame,6,7). The unchanged real gather implementation establishes these
roles. Correcting only these two semantic arguments yields
`main-yumeko-patterns-b`: two fresh deterministic full435-byte raw/ordered
positives and a rejected bounce336→335 control. Credit is three complete
functions and435 instruction bytes; no template/slot DATA, tables or padding
receive credit. The earlier two passing sibling bodies were not imported
through the failed aggregate.

# Stage-four midboss disappearance and reappearance

Natural C++ restores the complete original208-byte function at MAIN
1527:0D04, load15F74..16044 (ReC98 sub_1AFD4). All79 instructions, fourteen
local branches and the final near RET are independently decoded; the next
real pattern function begins at16044. There is no table or padding.

After the initial16 frames the function alternates horizontal displacement
around a saved center. Displacement above20 is compressed with signed integer
halving. At the halfway point it chooses a new center and Y through the real
near modulo RNG; the new X is consumed on following frames. Completion sets
the actual state byte and returns true. It preserves the original lack of
previous-position updates and does not clamp calls after the normal duration.

The canonical22-byte midboss/motion declarations remain unchanged. Center X
is a real two-byte external coordinate at DS372A (the next independently named
word is372C); stage parity is the real byte at5766. No new state values or
owned DATA/BSS are emitted. Sound is far14AB:0232, RNG near1527:0050, DGROUP209D.
The binder supplies only real addresses and outside-owner context holes.

`main-midboss-transition4-a` accepts all208 bytes and the sole original ordered
fixup at relative40 in both independent fresh deterministic producers. The
compiled sound13→14 negative is rejected. Credit is one complete function and
208 instruction/authored bytes. Private reviewed branches, boundaries, target
identity and real fields/calls are in
`.analysis/midboss-transition4-boundary-review.json`.

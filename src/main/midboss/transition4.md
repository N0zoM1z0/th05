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

## Named transition clock and typed vulnerability latch (2026-11-14)

The natural 208-byte leaf now names its ten compile-time parameters without
changing its machine code: motion begins at phase frame **16**, the midpoint
is internal frame **32**, the slowdown threshold is **20**, and the return
completes at internal frame **64** (phase frame **80**). Horizontal movement
uses **32 subpixel units = 2 pixels** per motion frame. Once the magnitude
exceeds 20, integer halving compresses it: 21 becomes 20, 31 becomes 25.
This happens on both halves, so the outbound and inbound peak is 25 steps,
not 31. The signed arithmetic and truncation are intentional.

At phase frame 16 the function disables vulnerability, plays sound 13 and
captures the current X center. At phase frame 48 it chooses a new X in the
half-open range **[64, 320)** pixels and a new Y in **[64, 96)** pixels; that
middle update changes the saved center and Y but leaves the current X alone.
The following update starts the return curve around the new center. At phase
frame 80 it returns X to the saved center, reenables vulnerability and returns
true. The caller immediately resets `midboss.phase_frame` to zero before
selecting the next pattern; the leaf itself deliberately has no post-duration
clamp.

The two vulnerability writes now use the same typed byte-15 view as the
stage-four controller (`Midboss4Scratch::shot_vulnerable`). This is an alias
clarification only: the original 16-byte Boss scratch storage, external DS
address and callback ABI are unchanged. `tests/test_midboss4_transition.py`
pins the complete 16/32/48/80 frame schedule, signed parity movement, both
integer-halving bands, random center ranges, shared byte-15 latch and caller
reset order. The 208-byte `main-midboss-transition4` owner was replayed with
two native Borland/TLINK producers after the change; all original bytes and
the ordered relocation remain exact, and its compiled negative was rejected.
Receipt: `.analysis/unit-replays/910a0d064d0644ed9a7aa82cd041b5a5/receipt.json`.

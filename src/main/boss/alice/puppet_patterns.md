# Alice puppet pattern candidate

Five contiguous complete callbacks cover original MAIN `1E209..1E435`,
556 instruction bytes and170 instructions. Their sizes are113,114,117,117
and95 bytes. No compiler tables, padding, owned DATA or BSS occur. Original
ordered relocation offsets are `[366,249,135,22,483]`; that stream is retained
in its original order.

The initial pattern fires random bullets during charging. The other patterns
emit one aimed spread/stack, repeated aimed fans, repeated aimed rings, and
a persistent seven-way fan. Each produces the real shrinking charge circle
at frame16. Their unsigned frame thresholds, sprite states and completion
results follow the original behavior. Packed assignments describe the actual
adjacent bullet spread, angle delta, stack count and speed-delta fields.

The frozen beam header supplies the canonical full26-byte Puppet, Boss,
motion, player and bullet types. The real dispatcher pushes a near puppet
reference and consumes AL. Every callback loads its argument from BP+4 and
returns RET2, establishing the near Pascal reference-taking bool interface.
No pseudoregister arguments, ASM template or hidden-register shim is used.

Near random generation and bullet emission share frame1527. The actual
shrinking-circle producer is far Pascal at AE1:34C6 and returns RETF4.
DS209D supplies the real frame counters, complete bullet template and near
tuning callback. Only these foreign declarations and symbols are provided.
The binder preserves even empty foreign compiler segments, anchors the
paragraph tail after1E440 and ends it at209D0. It supplies no instructions,
initialized values, stack or hole within the full556-byte contribution.

ReC98 `th05_main.asm` lines11214..11466 supplies the semantic reference.
Cached calibration contains the same complete instruction shapes for all
five callbacks. Original returns, all local branch destinations and ordered
fixups were independently checked against the pinned MAIN image. These are
preparation evidence, not source acceptance.

Private metadata `.analysis/alice-puppet-patterns-boundary-review.json`
contains the proposed whole unit and a unique staged negative changing the
stacked spread from aimed to fixed-angle. Two fresh focused exact producers
and compiled rejection remain required. No compiler was run during preparation.


`main-alice-puppet-scopes-a` accepts five individually complete function
scopes, totaling556 instruction bytes. One actual TU is compiled per fresh
round; both deterministic producers pass each full raw scope and its original
relative ordered fixup[22]. The compiled aiming-mode mutation belongs to the
second spread scope and supplies the shared control for this scope group.
No separate mutation is claimed for each sibling. Whole-contribution global
fixup order is not claimed or normalized. Every scope ends at its immediate
actual next function public or contribution end; no table or padding is skipped.

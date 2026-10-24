# Exact oracle contract

The objective is at least 98% authored bytes exact. Before claiming a percentage,
review the entire code/data ownership partition, retaining unknown extents.
Separate game-authored code, third-party libraries, compiler runtime, data,
packing stubs, metadata and genuine original handwritten assembly. Publish the
denominator and exclusions with their evidence; do not reduce it to accepted units.

An exact unit requires all of:

1. Size, SHA-256, format and structural target checks.
2. Reviewed complete boundaries and artifact/segment ownership.
3. Tool identity, executable compiler/assembler/linker probes and valid OMF.
4. Two independent clean builds with deterministic accepted bytes and fixups.
5. Raw zero-difference comparison of the entire unit, including relocations.
6. A negative control proving that changed output is rejected.

Ghidra is an analysis view, not an independent truth source. ReC98 names,
successful compilation, semantic equivalence and normalized matches cannot
satisfy raw byte exactness. Target-derived bytes or instruction listings,
padding and compiler-runtime/library bytes cannot inflate authored progress.

Packed executable exactness is distinct from decoded-image exactness. A
decoded match must name the unpacking method and target digest. It does not
claim the original packed container was regenerated. Whole-program exactness
requires complete layout, relocations, headers, overlays and packing equality.

Bounded C++ units may use explicit, target-observed external-symbol bindings
in a symbol-only linker scaffold. Such an oracle compares unmodified output
bytes and relative fixup sites at reviewed target extents. It does not accept
whole-program placement or standalone linkage. All scaffold origin holes and
explicitly reproduced alignment bytes receive zero authored instruction credit.

Compiler-generated CODE switch tables count as authored code when generated
by maintained semantic C++ switches and the complete contribution passes the
same raw comparison. Report their bytes separately from instruction bytes.
Explicitly reviewed padding receives no authored credit, regardless of its
value. Classification never masks bytes or relaxes the full raw/fixup gate.
Game assets and opaque target-derived arrays do not qualify as compiler tables.

Function-scoped units use the actual compiler contribution and demangled TLINK
function publics. The scope ends at the immediately next distinct function
public in that contribution, including idle or unaccepted functions; the final
function ends at the contribution end. Aliases, data labels, skipped neighbors
and boundaries outside the real contribution are rejected. Acceptance recomputes
these boundaries from both saved MAP files rather than trusting receipt fields.
Multiple accepted functions in one TU share one compilation per cold round;
their complete extents and ordered fixups are still compared separately.

A mixed-result replay is never relabelled successful. Explicit subset import
can accept independently passing complete units from its unchanged receipt,
retaining the aggregate verdict and selected subset as provenance. Every saved
result is rechecked, including excluded mismatches; the compiled negative-control
owner must be included. Default import remains all-or-nothing. Relocation-site
ordering is compared as emitted, even when identical raw code bytes differ only
in the ordering of loader metadata.

For an explicit CP932 owner, maintained inputs and frozen snapshots remain
UTF8. Positive and mutated compiler inputs are independently transcoded and
recorded with their actual byte identities. Acceptance reconstructs expected
compiler bytes from the canonical snapshot and checks every consumed file,
including the assembler input alias. Encoding never changes compared target
bytes or transfers credit to source literals without a complete raw scope.

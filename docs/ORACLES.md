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

Initialized semantic DATA is an explicit unit opt-in:
`extent_kind = "initialized-data"`, `functions = 0`, a natural C/C++ producer
origin, and reviewed `data_semantics` roles. Supported roles are `state`,
`filenames`, `ui-text`, `function-pointers`, `string-pointers` and
`semantic-tables`. These declarations require a source ownership review;
labels alone do not prove that an asset array is authored semantic DATA.
Asset payloads, BSS, CODE switch tables and function-scoped slices cannot use
this lane. Historical units default to CODE without changing their identities.

Explicit C static initializers use `origin = "compiler-generated-c-semantic-data"`
with both a `.c` source and `.c` compiler wrapper. This origin cannot claim CODE
or functions. The pinned driver selects C through the wrapper extension, with
unchanged compiler flags; producer guards reject accidental C++ mode. C DATA
receives a separate ownership kind and the same whole-contribution, two-producer,
raw-byte, ordered-fixup and own compiled-mutation gates. A semantic field-bank
model does not authenticate a historical struct or complete caller integration.

A DATA unit must cover one complete actual MAP `C=DATA` contribution, backed
by one real compiler DATA SEGDEF with every byte supplied exactly once by
LEDATA. The first implementation rejects LIDATA, COMDAT, patch and 32-bit data
transformations. Both saved MZ/MAP/OMF producers are re-read on import. Every
DATA byte, including pointer words and explicit uncredited padding, undergoes
the same raw comparison and original ordered MZ-fixup comparison as CODE.
No normalization or field masking is permitted. BSS reserves no initialized
target bytes and receives no credit through DATA metadata.

The text-renderer assembly DATA review is a separate lane in
`replay_text_fx_data.py`. It does not relabel assembler output as a natural
C/C++ producer. Two complete symbolic DATA contributions per artifact require
two fresh deterministic TASM producers, their actual complete OMF/MAP scopes,
full raw bytes, original ordered relocations and an own assembled mutation per
scope. Import revalidates saved aliases, argv/logs, target views, public
boundaries and DGROUP frames. Inferred handwritten origin remains explicit:
these bytes receive zero C/C++ and zero global authored credit, remaining
unknown in the global partition. CODE, raster resources and scaffold reserves
receive no credit from this review.

An explicit subsequent native assembly ownership review may adopt only its
named complete scopes. `review_text_fx_asm.py` pins the semantic assembly
sources, native origin evidence, complete CODE/DATA receipts, bounded vendor
investigation, classifications and review notes. A separate versioned adoption
decision is required; the original inferred replay records remain unchanged.
The renderer's CODE lane requires two fresh complete TASM/OMF/MAP/MZ producers,
symbol/operand readback and an own assembled semantic CODE negative. Its six
dummy runtime-patched operand bytes and one EVEN byte per artifact are compared
normally with zero credit. Two actual hardware-delay NOPs remain instructions.
Reviewed ASM instructions and DATA stay separate from C/C++ counters; no rule
here promotes compiler-generated code, raster resources or the ZUN inference.

The complete enemy VM family uses `replay_enemy_vm.py`: five procedures and
their real 59-word symbolic CODE dispatcher form one complete ASM contribution.
Native hidden SI/CF/ES contracts and independent source review establish its
assembly origin. Both positive producers and the own minimum-interval negative
retain complete OMF/MAP/MZ, aliases, actual argv/logs and the ordered original
fixup at909. Its 118 semantic ASM table bytes are separate from ASM instruction
bytes and compiler-generated switch tables. Two EVEN bytes and the original
two-byte branch to its own fall-through compare normally with zero credit.
`reviewed_enemy_vm_unit.json` explicitly adopts only that complete scope after
acceptance; unknown neighbors and foreign helper code cannot receive credit.

Other opt-in complete ASM families use `replay_asm_family.py`. Per-entry source,
typed include, symbols, binder and semantic ABI identities support incremental
planning; unrelated manifest entries do not force recompilation. Each entry
needs its own two fresh producers, complete ordinary CODE SEGDEF/LEDATA/MAP
coverage, native instruction/handler review, CS/DGROUP frames and actual
entry/table/patch publics, full raw/ordered-fixup checks and own assembled
semantic negative. Multiple replacement receipts import atomically. Original
verifier snapshots stay archived; a stricter current verifier may re-read
unchanged actual producers without claiming fresh compilation. Explicit
per-record/source-note adoption remains separate from exact replay. ASM dispatch
tables, alignment, inert branches and runtime placeholders retain their distinct
classifications and never change C/C++ counters or mask compared bytes.

Each DATA acceptance needs its own compiled negative DATA mutation. A mutation
that only changes CODE is insufficient. Select one DATA contribution per
focused replay; CODE units from the same owner can share its one TU compilation
per round. Canonical source snapshots, explicit CP932 staging, actual dependency
closures, wrappers, binding aliases and tool identities retain the existing
gates. No previous accepted CODE producer needs replay for this extension.

Mathematically generated inputs explicitly declare `generated_sources` with
`generator` and `output` paths. The output must be an actual compiler include,
and the maintained Python generator joins the frozen source snapshot without
pretending to be a compiler dependency. Replay and import run its bounded
`--check`, reject stale or modified output, and verify both saved identities.
Generator changes select only affected owners. The shot-velocity generator
reads mathematics alone; the compiler specializes its Q8 directions to the
game's speed with explicit signed fixed-point quantization.

`authored_data_bytes` is separate from `authored_code_bytes`, instruction bytes
and CODE-table bytes. `authored_bytes` is their code-plus-data sum, with explicit
padding excluded. The gapless inventory names these bytes
`accepted-cxx-initialized-data` or `accepted-c-initialized-data`; vendor decisions
and unknown spans are retained.
These counters do not establish the complete authored denominator or a global
percentage, and decoded OP/MAINE DATA grants no packed-file exactness.

Whole DATA may also be reviewed from the two actual archived positive producers
of an original bounded CODE replay, with one fresh compiled DATA negative.
`review_saved_data.py` rejects review-of-review parents and requires matching
source/module/flags/bindings/binary/encoding, saved actual compiler argv, complete
source closures and deterministic compiler objects. It archives and revalidates
the entire original parent, including excluded failures. Import mechanically
re-derives the DATA boundaries, full raw bytes, ordered fixups, producer identity
and negative outcome from saved artifacts. This lane explicitly reports two
retained cold producers and one new compiler invocation.


A batched CODE receipt has one explicitly named compiled negative owner; other
selected units share that oracle control. Do not describe the batch as compiling
each owner's own mutation. A `supplementary-compiled-code-negative` report can
supply a fresh owner-specific rejection while retaining the two already checked
positive producers. This is additional evidence, with zero new positive
compilations and zero authored credit; it neither rewrites the parent receipt
nor changes its acceptance. The supplemental checker revalidates actual saved
inputs, compiler arguments, OMF, MZ/MAP and the unchanged pinned tool receipt.

Reviewed ASM semantic CODE data is distinct from near-dispatch tables and DATA
segments. The first narrow role is `piano-key-horizontal-positions`: 12 word
coordinates derived from left/key width and diatonic white/half-key geometry.
The native proof must cover the whole modeled table without overlap, agree
with every derived word and maintain the complete raw/ordered-fixup gate.
Arbitrary literal banks, raster resources and unregistered models are rejected.
Source/model review and explicit adoption remain mandatory. Report semantic
CODE-table bytes separately from instructions, symbolic near-dispatch words,
C/C++ tables and initialized DATA; an embedded 90h data byte is not a NOP.
Existing unchanged objects may be revalidated by the stronger verifier without
recompiling or rewriting their archived verifier snapshots.

Explicit resource classification is separate from exact-source acceptance.
The registered `th05-zun-cg-256-glyphs-16x16-1bpp` model admits only the complete
8,192-byte native-consumed font bitmap, with a separate hash-bound adoption.
The native gate checks the immutable COM/directory, complete reader and DF path,
geometry, full reference-tile bytes and scope digests. Public CI checks metadata
without claiming native replay. Resources receive zero authored/instruction
credit; code, messages, alignment candidates and other children remain unknown.
No image payload is published. This does not establish the global denominator
or waive any source unit's two-build/raw/OMF/relocation/negative requirements.
See [font resource review](reconstruction/ZUN_FONT_RESOURCE.md).

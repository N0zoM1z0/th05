# Circle fill from unchanged original Master source

This separate decision adopts only GRCG_CIRCLEFILL at MAIN 100E..10A4 as
150 bytes of vendor CODE, with zero authored credit. It uses complete actual
producers of the unchanged original source file. Existing literal-candidate,
private-rename and EGC/EMS proofs are not broadened or rewritten.

The primary author archive's GC_CIRCF.ASM explicitly selects `.186`,
`.MODEL SMALL`, `.CODE` and the original FUNC.INC. The author's MAKEFILE
supplies `/mx /t /q /w2 /jJUMPS /DFARMODEL`. Although the physical model is
SMALL, FAR macros set CALLMODEL=FAR and RETSIZE=2. Both helper EXTRNs occur
inside CODE. The original includes and every source byte, including CP932
comments, line endings, private names and unsized PUSH operands, are preserved.

The candidate body in the older monolithic reference differs by seven private
names and two added `word ptr` annotations. It remains a mismatch under the
old name-only rule. This new proof does not transform that body or interpret
the annotations as a normalization permission. Instead, the genuine original
context compiles the untouched original source successfully and resolves its
word operands and same-CS far calls directly.

## Actual whole-unit gates

Two independent original-source producers each yield one complete ordinary
150-byte CODE contribution, with empty DATA. Both have a true far public at
offset zero and five self-relative16 EXTDEF fixups at 40/61/92/113/142. These
encode four-byte PUSH CS/near CALL sequences while retaining the real FAR
helper interfaces. The symbolic before/after scaffold preserves the actual
common _TEXT/CS0000, entry 100E and FAR helpers at 0000:1690 and 0000:1A44.
No helper bodies, initialized bytes, stack or entry are supplied.

All 150 linked bytes match the pinned native scope, SHA-256
`b15c3ea64d3ecc0a30c173ccff95c138f0f9be7a816f1e4bdc020f1fc37583c5`.
The original and both candidates have empty ordered MZ fixups. Complete native
decode covers 77 instructions, including two RETF6 paths and no instruction
NOPs, tables, padding or owned DATA/BSS. The own assembled negative changes
only the staged initial Y-offset literal from zero to one; byte 19 changes,
the full 150-byte extent and fixup context stay intact, and raw comparison rejects it.

The original source objects, MAP files and whole linked MZ files are byte
identical across positives. Raw binder-object hashes are retained separately;
only their dependency timestamp comments differ. Existing timestamp handling
establishes binder metadata identity, with no payload or fixups in those
objects. No target/linked byte, own source object or relocation is normalized.

The author's original command profile emits no translator-version COMENT.
The new separate guard therefore checks its exact CRC-valid 15-record profile,
word-aligned CODE of 150 bytes and empty DATA, names, group/comments/no-entry, full single LEDATA,
public, helper names and five relocation fields, plus the actual pinned
assembler/tool receipt, source bytes, arguments and successful logs. The old
game-ASM producer check remains unchanged. Quiet metadata is not permission
to accept an unidentified producer or an incomplete CODE interval.

## Reuse, limitations and explicit adoption

The first new source object was assembled and linked before the read-only
proposal writer was completed. It is retained with its verified source,
tool, argument, object and log identities. Only the independent second and
negative are then compiled. Total work is three original-source assemblies,
six symbol-only binding assemblies and three links. Two reader-only metadata faults
were corrected without rebuilding: the original quiet COMENT profile and
binding dependency timestamps. No source, instruction or option variants occur.

The new native check also revalidates the inherited original archive and
frozen source/macro provenance. It rereads all actual saved producers; public
structural CI needs no private source, compiler or game. Focused tests reject
CRC-valid bad CODE/DATA/relocation/coverage profiles, source/flag/result changes,
reviewer edits, nonunique controls and widened or credited adoption decisions.

`config/reviewed_master_primary_circlefill.json` binds the entire separate
proof and adopts only this complete library procedure. No historical game
project, historical original assembler identity, whole executable or packed-file equality
is claimed. The other five circle procedures and the intervening byte remain
unknown; their source/context and DATA/BSS relocation blockers are not repaired
by this result. Source and artifact payloads remain private.

Independent current source/gate/actual review:
`.analysis/vendor-review/circlefill-primary-source-gate-independent-review.json`,
SHA-256 `df1b36d73df04af4083a1f134326f7efed9040f251150e09e9013d2ef7b2cfff`.
That report's test-fixture item is resolved by the subsequent test addendum;
no production-source or byte gate was relaxed to resolve it.
Tests-only final addendum:
`.analysis/vendor-review/circlefill-primary-final-tests-addendum.json`, SHA-256
`ba973e87ff3a6ad52af70601e74081a756e6b37b498c0b036020f4dabed7d3be`.

Final independent adoption audit:
`.analysis/vendor-review/circlefill-primary-final-adoption-independent-review.json`,
SHA-256 `74bb2f17a7208bdcce46b32ff5860ff308123291ec6871e8a5ab6664afaaaeb6`.
It confirms exactly 150 unknown bytes become vendor CODE, all 51 prior
tracked configuration files remain byte-identical and the other three artifact
views are unchanged. The handoff now distinguishes the 346-byte OMF files from
their 150-byte CODE contributions. Full CI passes 352 tests; all four C/C++
incremental plans and the ASM plan are empty. Ownership target verification,
generated progress and the public structural check pass.

Root final review:
`.analysis/vendor-review/circlefill-primary-root-final-review.json`, SHA-256
`2ae1b23bdc03d06ce64e864701ad5385fa0223f6941fd35fafdf5ed7e69b3bdb`.

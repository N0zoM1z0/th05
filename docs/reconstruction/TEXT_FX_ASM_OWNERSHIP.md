# Reviewed text renderer assembly ownership

This decision adopts six complete source scopes in OP and MAINE as reviewed
game-specific assembly reconstruction. It is distinct from the original
standalone DATA receipt, which deliberately carried no global ownership credit.
The C/C++ ledgers, functions and counters remain unchanged.

| Scope, per artifact | Compared bytes | Authored ASM bytes | Checked, zero credit |
| --- | ---: | ---: | ---: |
| Whole self-modifying renderer and private glyph helpers | 346 | 339 | 1 EVEN byte, 6 dummy operand bytes |
| Two CALL-delta arrays and four near resource pointers | 28 | 28 | 0 |
| Mutable effect/spacing defaults | 4 | 4 | 0 |

Across OP and MAINE this adds **678 ASM instruction bytes and 64 semantic ASM
DATA bytes**, separately reported. All 756 bytes in these complete scopes pass
raw comparison; 14 are uncredited. The 32 raster-mask bytes between dispatch
and state in each artifact remain unknown and receive no authored credit.
The observed universe stays 319,268 bytes, with no global denominator or
percentage claim. The inferred ZUN memory-child origin is not promoted.

## Why this is an assembly reconstruction

Native review observes five intentional CS writes in each renderer: two CALL
displacements, two spacing immediates and an FS mask displacement. Its two
five-entry dispatch arrays store assembler-level differences between private
helper addresses and interior CALL operand labels. The glyph helpers have a
custom AX/CH/DX/BP contract and deliberate fall-through. These native features
support a handwritten assembly implementation, rather than an ordinary
compiler-generated C/C++ function being reclassified for convenience.

`src/shared/graphics/text_fx_render.asm` implements the complete Shift-JIS/ANK
iteration, CG/GRCG port protocol, glyph weight operations and self-modification
with symbolic local labels, named stack parameters, hardware constants and
macros. It contains no emitted opcode directives, code arrays, target-byte
includes, absolute local CODE addresses, fake helpers or synthetic prefix.
Its DS includes bind real semantic DATA boundaries. Effect and spacing are
word-typed external variables, preserving actual memory access and OMF linkage.
The separate DATA source uses symbolic address differences and near pointers.

Both the implementation and this ownership interpretation received an
independent read-only source/native review. Native assembly evidence and
maintainable semantics justify the explicit decision below; a passing assembly
alone would not justify it. No permission or inference here applies to any
compiler-generated owner.

The candidate reference is ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, specifically
`th04/hardware/grppsafx.asm` and the documented hardware macro definitions.
Its reconstructed code supplies semantic hypotheses, not transferred target
acceptance or literal historical source. Each TH05 artifact has its own native
boundary, source producer and full raw-byte proof.

The bounded vendor investigation verifies pinned `masters.lib`, SHA-256
`6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6`,
273721 bytes and 640 structurally valid members. GRAPH_PUTSA_FX, GRPPSAFX and
GLYPH_WEIGHT identifiers are absent, and neither native position-independent
20-byte callback-delta bank occurs anywhere in the archive. This supports a
game-specific helper rather than that library's ordinary text API. It does
not exclude every possible historical vendor derivation.

Literal historical source, the original assembler version, and independently
proved pristine target provenance remain unknown. The supplied copy stays
candidate-local-attested. The classification is reviewed native reconstruction,
not a claim of recovered historical text or independently authenticated authorship.

## Boundaries and exclusions

| Artifact | CS frame | Complete CODE | Dispatch DATA | State DATA |
| --- | --- | --- | --- | --- |
| OP | 0D30 | D436..D590 | F982..F99E | F9BE..F9C2 |
| MAINE | 0E80 | E91A..EA74 | 10790..107AC | 107CC..107D0 |

Ends are exclusive decoded load-module offsets. CODE includes the final helper
RET and the EVEN byte between renderer and helpers. It is one actual complete
TASM SEGDEF and one actual complete TLINK contribution in each producer.
No function-prefix or instruction-window acceptance is used.

Relative to each 346-byte CODE start:

- Explicit port-delay NOP instructions at 173 and 261 retain ASM instruction credit.
- EVEN alignment at 299 is compared but receives zero credit.
- Dummy runtime-patched operands `[222,224)`, `[293,295)` and `[343,345)` are
  compared normally and receive zero credit, even though their surrounding
  instructions and patching behavior are genuine assembly semantics.
- Symbolic default bold CALL operands express a real helper target and retain
  their instruction credit; they are not the dummy `1234h` values.

All original relocation streams within these CODE/DATA scopes are empty. The
actual OMF nevertheless contains the real local CS and external word fixups;
its complete unchanged records are validated and linked normally. No MZ fixup
sorting, masking, output editing or placeholder normalization occurs.

## Exact evidence and explicit adoption

`config/text_fx_render_acceptance.json` records two independent fresh CODE
producers per artifact, with full raw/OMF/MAP/MZ and public/operand boundary
readback. Each artifact's own negative changes both glyph-loop heights from
16 to 15; the complete contribution stays 346 bytes and raw comparison fails.
The saved producers are `.analysis/textfx-render-native/replay-a/`.

The unchanged DATA acceptance remains
`.analysis/textfx-data-native/asm-c/receipt.json`. Its source and actual
dependencies were checked, and its accepted two-producer/own-negative evidence
was reused rather than recompiling unchanged DATA. Both receipt validators
re-read their actual archived inputs, successful argv/logs, objects, linked
outputs, target proofs and tool identities before the ownership proposal.
Installed tool execution probes were reused after identity checks.

The first CODE diagnostic measured 344 bytes because TASM treated EQU state
addresses as immediates. Word-typed EXTDEFs and actual symbol-only DATA binding
resolved that declaration defect; the subsequent complete diagnostic passed.
These diagnostic directories are retained and are not accepted receipts.

`scripts/review_text_fx_asm.py --write-evidence` verifies the native origin
review, bounded library investigation and both unchanged accepted receipts.
It writes `config/text_fx_asm_ownership.json`, pinning maintained source,
verifiers, complete scopes, exclusions, receipts, targets and these review notes.
`config/reviewed_text_fx_asm_units.json` then explicitly adopts exactly those
six units. Neither proposal production nor inferred-origin replay alone grants
ownership credit. Structural CI rejects changed sources, expanded selections,
altered byte accounting or stale evidence/decision digests.

The gapless ownership inventory overlays only still-unknown intervals. It
separates reviewed ASM instructions, reviewed ASM initialized DATA, checked
ASM alignment and checked ASM runtime placeholders. Every other unknown span,
including raster resources, remains in the observation universe. Full executable
linkage, actual game execution, packing and the 98% objective remain unaccepted.

# Master EMS transfer wrappers: source-backed vendor review

This separate decision classifies only two complete MAIN procedures as vendor
CODE. It grants zero authored credit and does not establish the global authored
denominator. The existing literal-source, additions, SIN8 and EGC proofs and
their adoption decisions remain unchanged.

| Procedure | Complete load-image range | Bytes | Return | Ordered MZ fixups |
| --- | --- | ---: | --- | --- |
| EMS_READ | 3F6A..3FCC | 98 | RETF 14 | empty |
| EMS_WRITE | 406C..40CE | 98 | RETF 14 | empty |

All 196 bytes compare normally. Each scope decodes as 40 instructions, with
no instruction NOPs, padding, embedded tables, initialized DATA or BSS. The
active listing supplies complete procedure boundaries; the next procedures
are outside these owners. No foreign helper bytes receive new credit.

## Primary source and the fixed symbol changes

The primary Master 0.23 author archive contains complete EMSREAD.ASM and
EMSWRITE.ASM bodies. In each body, exactly five private stack-frame equates
have an added `@@` prefix in the candidate source:

| Original name | Candidate name | Literal definition | Definition/reference occurrences |
| --- | --- | --- | ---: |
| handle | @@handle | `(RETSIZE+7)*2` | 2 |
| offs | @@offs | `(RETSIZE+5)*2` | 3 |
| mem | @@mem | `(RETSIZE+3)*2` | 3 |
| len | @@len | `(RETSIZE+1)*2` | 3 |
| block | @@block | `-18` | 12 |

The new verifier permits only these five exact substitutions. Every definition
must occur once with its fixed `=` expression; all reference counts are checked,
the new spellings must not collide or be exported, and quoted code is rejected.
The complete resulting procedure text must equal the candidate literally.
Instruction/data/macro tokens, constants, case, whitespace and comments cannot
change. The inherited block reader decodes the original CP932 and candidate
UTF8 text and represents line endings as LF; full raw source identities remain
pinned separately. No linked byte, instruction or relocation is normalized.

These frame expressions have a separate narrow parser. The EGC proof's private
label/self-patch rules and the older literal-source rule are not broadened.
The five names and both complete source block hashes are pinned in the new
proof, with the verifier's own source identities bound by explicit adoption.

## Actual producer, model and native evidence

The unchanged base proof revalidates its primary archives, all 653 extracted
members, frozen candidate/calibration sources, actual listing, saved OMF,
calibration MAP/MZ and independent large-FAR model context. The original
MAKEFILE/FUNC.INC establish the far code and data pointer model, including
RETSIZE. Each wrapper has 14 argument bytes and an 18-byte stack transfer
descriptor. It preserves the transfer result while re-enabling page frame zero.

Both native bodies contain two actual PUSH CS/near CALL pairs, at relative
80 and 88, targeting EMS_MOVEMEMORYREGION at 403C and EMS_ENABLEPAGEFRAME
at 3FF2. The unchanged base proof already reviews those helpers. The complete
98-byte procedures reconstructed from the saved OMF require no link-field
additions or fixups; their
unmodified bytes equal both calibration and native scopes. Original ordered
MZ fixup streams are empty. No fake near declaration or provider is introduced.

Secondary NEAR-model library objects are not claimed to match. This is a
source-backed library attribution, not proof of the historical distribution,
original project, pristine game provenance or whole executable regeneration.
The supplied Japanese game remains candidate-local-attested.

## Adoption and validation

`scripts/review_master_ems_transfers.py --check` re-reads the private primary,
source, OMF and native evidence without assembling, compiling or running Ghidra.
Public `--structural-check` checks the frozen metadata and reviewer identities.
Nine focused tests reject altered frame expressions, definitions, references,
collisions, exports, instructions, comments, whitespace, source identities,
bounds, byte/fixup proofs, calls and adoption policies. Public CI includes the
new proof while retaining every unknown byte outside the explicit scopes.

`config/reviewed_master_ems_transfers.json` binds the complete separate proof
and adopts only these two vendor procedures. C/C++ and ASM source acceptances,
initialized DATA, resources, padding and the null global denominator do not
change. No new toolchain execution probe or target build is performed.

Initial independent routing:
`.analysis/vendor-review/ems-transfer-source-family-routing.json`, SHA-256
`e318482aa429012caa5f35c9652252f73e896d581a8be61afa034656dafb7ead`.
Independent source/native/new-gate review:
`.analysis/vendor-review/ems-transfers-additive-gate-independent-review.json`,
SHA-256 `61383b66fdfed6eaa88388e2da7a7b4f9e36184a74ecb2fbf24652fce364cc0e`.
Independent final adoption/count audit:
`.analysis/vendor-review/ems-transfers-final-adoption-independent-review.json`,
SHA-256 `947583ea6c2e1c177f5c37312b46eac4f7ff72e7794eee4679fd5f696d973995`.

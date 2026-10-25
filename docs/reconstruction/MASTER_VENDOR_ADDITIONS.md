# Source-backed Master additions: ownership proposal

This additive review proposes seven complete original extents totaling **2,152
bytes**. Its evidence remains a PROPOSAL and grants no authored credit. A
separate root-authorized decision now selects exactly these seven scopes for
third-party library ownership. The existing Master and CL reviewers, their
evidence and earlier adopted decisions remain unchanged.

| Scope | Artifact | Original complete extent | Classification proposed |
| --- | --- | --- | --- |
| `main-pfgetc` | MAIN | `[0x227C,0x228C)` / 16 bytes | Library instructions and one assembler EVEN byte |
| `main-assignall` | MAIN | `[0x2442,0x2448)` / 6 bytes | Library instructions |
| `main-sound-joy` | MAIN | `[0x3668,0x3679)` / 17 bytes | Library instructions |
| `main-sajout` | MAIN | `[0x3686,0x368F)` / 9 bytes | Library instructions |
| `main-str-ieq` | MAIN | `[0x45B0,0x45E8)` / 56 bytes | Library instructions |
| `op-rottbl` | OP | `[0x1C88,0x2088)` / 1,024 bytes | Library pixel-rotation constants in OMF CODE |
| `maine-rottbl` | MAINE | `[0x1E22,0x2222)` / 1,024 bytes | Library pixel-rotation constants in OMF CODE |

The five MAIN procedures contain 103 instruction bytes and one library alignment
byte. The two tables contain 2,048 semantic data bytes. All seven scopes grant
zero authored credit, including library padding. A CODE-class table is not an
instruction contribution.

## Verification

Public validation requires no game, compiler or private cache:

```sh
python3 scripts/review_master_additions.py --structural-check
python3 -m unittest discover -s tests -p 'test_master_additions_review.py'
```

With retained private evidence, revalidate actual inputs natively:

```sh
python3 scripts/review_master_additions.py --check
```

The command runs with one CPU, nice priority and a 384 MiB address-space limit.
It invokes no compiler, linker, assembler, Wine, download or target execution.
`--write` writes a PROPOSAL only. These vendor ownership checks use one retained
link per context; they do not claim the two fresh producers required for authored
source acceptance.

The public metadata is
[`master_vendor_additions.json`](../../config/master_vendor_additions.json).
Its `proposed_decisions` contain explicit per-artifact scope lists with
`PROPOSAL_ONLY_LISTED_SCOPES`, authored credit zero, a null denominator and unknown
policies for every other procedure or gap. They are not active adoption files. The separate
[`reviewed_master_additions.json`](../../config/reviewed_master_additions.json)
uses `ADOPT_ONLY_LISTED_SCOPES` and pins this complete evidence file, all seven
scope IDs, every artifact's separate packed/payload identities, zero authored
credit and a null denominator. `ownership.py` consumes that explicit decision;
missing decisions yield no claims. Native inventory replays the whole additive
review once for all three contexts. Only unknown intervals can receive a claim;
overlap with accepted source or earlier vendor claims rejects the inventory.
The inventory keeps `verified-vendor-code` for these actual CODE-class extents,
with `content_kind: library-code-data` for the tables,
`content_kind: library-instructions` for the five procedures, and the actual
proof `scope_id` on every claim. The tables are not counted as instructions.

## Primary source and actual producer evidence

The verifier pins the complete existing MAIN Master proof and actually replays
its frozen reviewer. That rechecks the independently pinned author MTSRC023 and
stored SRC.LZH archives, checksums/CRCs, all 653 literal extracted files, all 395
retained source dependencies, the actual historical listing producer, original
macro alternatives, large-model FAR/data2 context, complete original MAP/MZ and
saved/listing/calibration OMF identity. The old twenty procedures are context
validation only; they receive no duplicate proposed extent here.

For the five additions, the checker separately extracts each complete active
listing PROC/ENDP scope, including original EVEN padding. Each complete source
block must occur literally and uniquely in the author's archive and the retained
candidate. Strict CP932 versus UTF-8 decoding and line-ending conversion are the
only source conversions. Case, whitespace, comments, identifiers and operands
are not normalized. Actual OMF LEDATA and supported link actions reconstruct the
whole scope. Original and calibration bytes and their literal ordered relocation
lists, including a relocation crossing the lower boundary, must match.

For RotTbl, the whole named initializer consists of 256 original dword constants.
The exact complete symbolic source block is compared literally, and its declared
values are serialized according to the original dword little-endian semantics.
No target bytes are used to generate source. The checker validates each actual
OP/MAINE monolithic object, all 192/170 unique source files in actual OMF dependency order
(193/170 path occurrences), the real
SEGDEF, actual PUBDEF offset, gapless nonoverlapping LEDATA and absence of any
intersecting FIXUPP field. MAP public entries in both the Name and Value sections
must have the original literal frame:offset; duplicate contributions or duplicate
entries within a section fail. The source values, OMF scope, retained executable
and original decoded target must agree completely. Original packed identity,
decoded payload, decoder receipt, ordered relocation stream and historical
two-load proof are pinned independently; no synthetic MZ is created.

The retained SMALL-model `masters.lib` member is corroboration only. Its complete
library/member hashes and actual records remain visible in the evidence. The
ReC98 original-distribution claim is secondary binary provenance; the independent
author source archive supplies the primary ownership evidence. Unknown archive
record `0x8E` is retained and is not declared harmless or silently discarded. No
individual library-member MAP contribution is invented: the actual linked
objects are mixed monolithic game/library objects.

## Remaining limits

The original supplied game remains candidate-local-attested. Root's explicit
adoption covers only these seven scopes; native inventory validation remains a
required publication check. Existing source-mismatch procedures, raw-inexact
candidates, unsupported link transformations, surrounding gaps and other
unreviewed data remain unknown. Neither this evidence nor the retained binary
member permits a blanket Master prefix exclusion or an authored-byte denominator.

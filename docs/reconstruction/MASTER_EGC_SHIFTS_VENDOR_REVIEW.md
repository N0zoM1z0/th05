# Four source-backed Master EGC shifts

This separate reviewed decision classifies four complete MAIN procedures as
vendor code, with zero authored credit. It does not replace the earlier literal-
source proof, rewrite its40 textual-mismatch records, accept an executable, or establish
the global authored denominator.

| Procedure | MAIN half-open extent | Full bytes | EVEN NOPs |
| --- | --- | ---: | ---: |
| EGC_SHIFT_DOWN | 08AA..09B0 | 262 | 3 |
| EGC_SHIFT_LEFT | 09B0..0AB2 | 258 | 2 |
| EGC_SHIFT_RIGHT | 0AB2..0BC2 | 272 | 2 |
| EGC_SHIFT_UP | 0BC2..0CC2 | 256 | 4 |

The total1048 bytes comprise1037 nonpadding bytes and11 assembler EVEN NOPs.
All are vendor-classified bytes, including padding; none is authored source
credit. Native decoding enumerates every instruction NOP and agrees exactly
with the active listing's EVEN sites. Each procedure ends with its real far
Pascal RETF10; every local branch reaches an instruction boundary. Ordered
original and candidate MZ fixup lists are empty.

The primary authority is the independently pinned author's Master0.23 source
archive, not ReC98 acceptance. Complete EGCSFTD/L/R/U.ASM procedure bodies differ
from the frozen candidate bodies only in seven named private identifiers each:
four local branch labels and three self-patch EQU symbols. The reviewed map
prefixes branch labels with@@ and gives each patch symbol a file-specific name.
All definitions and references agree one-to-one; none is an exported public.
The verifier applies only those exact named substitutions outside comments,
then requires literal complete-body equality. It preserves every other character,
including instruction/data tokens, constants, case, whitespace and comments.
It does not strip comments, fold case, normalize instructions or accept arbitrary
renaming. As in the frozen base proof, strict CP932/UTF8 decoding and line-ending
conversion precede this comparison. No proprietary procedure source is published.

The original source's FARMODEL build surface and the inherited frozen FUNC.INC
macro proof support the actual large/far context, with RETSIZE2 and five word
arguments. The alternate secondary library's NEAR-model objects differ in stack
offsets and return encoding and are not claimed to match. Original historical
project and precise library-distribution identities remain unproved; this is
source-backed provenance for the four observed bodies.

Native checking rereads the primary stored archive and all frozen source
identities, actual active TASM listing, checksum-valid saved/listing/calibration
OMF, complete MAP and linked MZ, and the locally attested target MZ. It reuses
the old macro/closure verifier unchanged. Each complete LEDATA scope is gapless;
its three real local_TEXT offset fixups are independently reconstructed using
the actual0x272 MAP contribution. Reconstructed bytes must equal the unchanged
linked bytes, which must equal every original byte. No original/candidate byte,
OMF record, fixup list or linked output is rewritten.

`config/master_egc_shifts_ownership.json` is the frozen proposal. The separate
`config/reviewed_master_egc_shifts.json` explicitly adopts only its four named
scopes and pins the entire proof, source reviewers and target identity.
`ownership.py` overlays only unknown extents and grants no authored credit.
All earlier vendor/ASM/C++ decisions and source identities remain unchanged.

Public checks require no private targets or tools:

```sh
python3 scripts/review_master_egc_shifts.py --structural-check
python3 -m unittest discover -s tests -p test_master_egc_shifts.py
```

That mode reports `byte_proof_replayed: false`. With retained private inputs,
`python3 scripts/review_master_egc_shifts.py --check` revalidates actual native
proofs. Neither mode starts Wine/Ghidra, compiles, downloads tools, or claims two
new source builds. These are vendor ownership checks, not authored-unit gates.

Independent source/native review:
`.analysis/vendor-review/egc-shifts-source-native-independent-review.json`,
SHA-256 `f0b649c17748b42276a2f0a3c171d873509d687b56eba4d5ac047a4492f58c04`.
Independent additive-gate review:
`.analysis/vendor-review/egc-shifts-additive-gate-independent-review.json`,
SHA-256 `7eea2ec4190f2a0aaca81e6e818b024730bbc70c7fbe9c0965aa862040a54034`.

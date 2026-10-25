# SIN8 initialized vendor DATA proposal

The independent proof in
[`master_sin8_ownership.json`](../../config/master_sin8_ownership.json)
proposes three complete 640-byte initialized DATA scopes, totaling **1,920
bytes**. Its evidence remains a PROPOSAL. A separate root-authorized decision
now adopts exactly these three scopes as `verified-vendor-initialized-data`.
Instruction credit and authored credit are zero; the authored denominator remains
null. The frozen reviewer and its evidence are unchanged.

| Artifact | Original physical extent | Actual retained calibration extent |
| --- | --- | --- |
| MAIN | `[0x20DEC,0x2106C)` | `[0x20E0E,0x2108E)` |
| OP | `[0xF570,0xF7F0)` | `[0xF570,0xF7F0)` |
| MAINE | `[0x1038A,0x1060A)` | `[0x1037A,0x105FA)` |

The author archive's complete initializer contains 320 signed 16-bit words.
`_SinTable8` exposes the first 256 words. `_CosTable8` starts 64 words (128
bytes) later and exposes 256 words, sharing 192 words with the sine view. The
physical extent is 640 bytes, rather than two independent 512-byte arrays. This
DATA is distinct from the authored 1,024-byte shot-velocity initializer and the
1,024-byte CODE-class RotTbl in each applicable artifact.

Run public checks without proprietary games or tools:

```sh
python3 scripts/review_master_sin8.py --structural-check
python3 -m unittest discover -s tests -p 'test_master_sin8_review.py'
python3 -m unittest discover -s tests -p 'test_master_sin8_adoption.py'
```

With retained evidence, replay actual inputs natively:

```sh
python3 scripts/review_master_sin8.py --check
```

`--write` writes a PROPOSAL only. The native CLI uses one CPU, nice priority and
a 384 MiB address-space limit. It runs no compiler, assembler, linker, Wine,
download or target. There is one retained calibration link per context, with no
claim of the two fresh producers required for authored-source acceptance.


The separate decision is
[`reviewed_master_sin8.json`](../../config/reviewed_master_sin8.json), with
`ADOPT_ONLY_LISTED_INITIALIZED_DATA`, exactly three reviewed scope IDs, the full
proof SHA-256, each artifact's packed/payload identities and payload size, zero
authored/instruction credit, null denominator and unknown policies for everything
else. Missing decisions yield no claims. Native inventory replays this entire
SIN8 review once for all three views. Every claim uses the original physical
extent and preserves its actual proof scope ID, `content_kind:
library-initialized-data` and zero instruction bytes. The overlay rejects overlap
with accepted source or previous vendor ownership and rejects CODE kinds or
instruction tags for this initialized DATA. Public CI runs the frozen structural
review without private inputs.

The verifier pins the unchanged full Master-additions context proof and its
reviewer closure. It actually replays that context, including the independently
pinned original MTSRC023 and stored SRC.LZH, all 653 literal extracted files,
the retained MAIN listing/macro/source context and the full OP/MAINE source
closures. These inherited code scopes receive no duplicate ownership claim.

The complete original SIN8 symbolic initializer is compared literally with each
actual retained `sin8[data].asm`. Only strict CP932 versus UTF-8 decoding and
line-ending conversion are allowed. The declared signed words are serialized
according to their original 16-bit little-endian semantics. Source is not
generated from target bytes, and mathematical sine approximations are not the
ownership authority.

For each artifact the verifier independently checks:

- Original packed identity and payload identity, plus the actual OP/MAINE
  decoder receipt, ordered relocation stream and historical two-load proof.
- The actual startup DS immediate and relocated word, and the startup DS load,
  in both original and retained link. Original DS frames are 209D, 0EFE and
  1011; retained frames are 209E, 0EFE and 1010 respectively.
- The real DATA contribution in the complete MAP, both Name/Value public
  sections and their literal frame:offset aliases. No original target MAP or
  individual library-member contribution is invented.
- The real DATA SEGDEF/PUBDEF and gapless nonoverlapping LEDATA for the complete
  initializer. Any intersecting FIXUPP field, including one crossing the lower
  boundary, rejects. LIDATA expansion is bounded and any scope intersection
  rejects; unrelated iterated DATA is not granted ownership.
- Complete original, calibration, symbolic-source and OMF scope bytes. The
  table must occur uniquely in each full image. Both literal ordered relocation
  lists must be empty, including crossing-boundary relocation fields.

Original and calibration positions and frames remain separate. No operand,
byte, relocation, table phase or frame normalization occurs. The alias offsets
come from the complete named primary initializer, its unique physical occurrence
and actual startup DS; original symbol names are not claimed as shipped MAP data.

The supplied game retains candidate-local-attested provenance. Every unreviewed
scope, surrounding gap and other data remains unknown. The explicit decision
covers only these three physical scopes; native inventory validation remains a
publication check. Existing CODE-only vendor decisions cannot adopt this DATA.

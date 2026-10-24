# Master 0.23 procedure ownership proposal

`config/master_vendor_ownership.json` proposes twenty individually bounded
vendor procedures in the mixed MAIN `th05_main.asm/_TEXT` contribution. Their
complete extents total376 bytes:367 instruction bytes and9 assembler EVEN
padding bytes. Every complete extent compares literally to the original with
the same empty ordered MZ relocation list. This is an ownership **PROPOSAL**,
with authored credit0 and no denominator or ownership decision in the proposal.
The separate reviewed adoption is documented in
[MASTER_VENDOR_ADOPTION.md](MASTER_VENDOR_ADOPTION.md).

Run the public, private-input-free structure check with:

```sh
python3 scripts/review_master.py --structural-check
```

That mode validates the frozen reviewed scope, public reviewer identities,
boundaries, accounting and proposal/deferred policies. It explicitly reports
`byte_proof_replayed: false`; it does not claim to read unavailable game,
toolchain or vendor files.

With the retained private inputs, run the actual native evidence replay:

```sh
python3 scripts/review_master.py --check
python3 -m unittest discover -s tests -p test_master_review.py -v
```

The checker does not execute Wine, assemblers, compilers, linkers, downloads or
private helper scripts. It rereads and independently checks:

- The pinned original MAIN MZ and payload, saved linked MZ and complete MAP.
- The byte-identical saved, listing and calibration OMF streams, including
  record checksums and actual `_TEXT` SEGDEF/MAP alignment and extent.
- The historical bounded single-listing producer identity, actual TASM binary,
  all395 frozen source dependencies and the actual OMF dependency ordering.
- All174 active address-bearing PROC/ENDP pairs. False conditional rows,
  macro-definition ENDPs and wrapped comments do not establish procedures.
- Gapless, nonoverlapping LEDATA coverage for each proposed extent. The one
  observed local `_TEXT` offset fixup is reconstructed from its actual MAP
  contribution; unsupported link transformations fail closed.
- Complete literal procedure-source identity against the author's independently
  pinned MTSRC023 distribution. The only source conversions are strict CP932
  versus UTF-8 decoding and line-ending conversion. Whitespace, case, comments,
  identifiers, labels and instructions are not normalized.
- Original `/DFARMODEL`, actual listing large model, RETSIZE2/DATASIZE2, the
  complete macro alternatives and their active arms, function wrappers,
  whole-file PF.INC identity, WAITREADY and relevant hardware constants.
- Complete original and linked procedure bytes, original padding values and
  ordered MZ relocation fields, including relocations crossing into a boundary.

The source archive and all proprietary inputs stay private. Public metadata
contains identities, filenames, boundaries, counts, source line ranges and
context arguments, without procedure source text or target instruction bytes.
The outer compressed distribution is rehashed but not decompressed again;
the independently pinned stored inner archive is parsed with header checksum,
member CRC, bounds, duplicate/path and terminator checks. All653 extracted
files must still equal those literal inner members.

The preserved listing producer is a single historical producer, not a pair of
fresh DOS builds. The original upstream macro files are not separately
assembled: their contextual equivalence is a native source/listing argument
backed by the actual OMF/link and original-byte checks. The original game copy
remains candidate-local-attested, without an independent pristine claim.

Forty first-proposal candidates have absent, ambiguous or differing complete
upstream source blocks and remain DEFERRED. The196 uncovered bytes remain
UNKNOWN, as do all other unadopted procedures. The standalone module also
contains game-specific helpers and modified library code. Neither the whole
module nor a broad Master prefix may be excluded using this proposal.

The synthetic tests exercise source/comment drift, inactive listing rows,
nested macros, FAR/data2/model drift, archive corruption, OMF checksums,
unsupported fixups, byte gaps/overlaps, boundary-crossing fixups, original MZ
relocations and padding, stale input hashes, and forbidden policy changes.
No ownership script, reviewed-vendor decision, progress denominator or CI hook
is changed by this work. Any adoption requires a separate explicit review.

# Reviewed CL.LIB initialized DATA

Twenty-four complete vendor DATA contributions,619 bytes in each of MAIN, OP
and MAINE, are now explicitly classified as third-party initialized DATA.
This adds **zero authored exact bytes**. The complete authored denominator and
percentage remain unreviewed; all other unknown intervals remain present.

Each contribution is backed by a complete ordinary `_DATA` SEGDEF from the
pinned Borland CL.LIB, with complete nonoverlapping LEDATA coverage. No selected
OMF fixup is present. Its unmodified bytes agree with the retained calibration
MZ at the actual MAP contribution, then with exactly one occurrence in the
original artifact's stored DATA region. Original ordered MZ relocation streams
are independently checked and empty. OMF integrity, whole-library identity,
complete member program records, actual source/target bounds, decoded-view
proofs, and verifier/parser/toolchain identities are pinned and rechecked.

| Complete member DATA | Bytes per artifact | MAIN start | OP decoded start | MAINE decoded start |
| --- | ---: | --- | --- | --- |
| `_abort` | 31 | 22A56 | 11836 | 118EA |
| `files2` | 42 | 22C14 | 119F4 | 11AA8 |
| `ioerror` | 91 | 22C3E | 11A1E | 11AD2 |
| `ctype` | 257 | 22CB4 | 11A94 | 11B48 |
| `signal` | 38 | 22EE2 | 11CC2 | 11D76 |
| `xx` | 18 | 22F22 | 11D02 | 11DB6 |
| `strings` | 102 | 22F38 | 11D18 | 11DCC |
| `loadprog` | 40 | 22F9E | 11D80 | 11E32 |

Coordinates are half-open load-module extents, with end=start+size. These
members supply runtime diagnostics, file/error support, character
classification, signal defaults, exception support, Borland string support and
process-loading support. They are actual vendor-provided contributions, not
newly authored game string tables or graphics assets. DATA is an OMF class;
this review does not reclassify any associated CODE, BSS or linker padding.

The source pins and both calibration/native coordinate sets are in
`config/cl_data_sources.json`. Public proof is
`config/vendor_data_ownership.json`; an independent explicit decision in
`config/reviewed_vendor_data_units.json` selects the24 reviewed rows by ID and
pins the exact evidence file. The ownership inventory overlays those complete
ranges only on unknown spans. Overlap with accepted source, tables, padding or
another vendor claim fails closed. The observation universe and every authored
counter remain unchanged;1857 bytes move from unknown to vendor DATA.

## Scope and rejected routes

No byte normalization, relocation masking, guessed all-zero range, contribution
slice or transferred reference acceptance is used. Other CL DATA is not silently
included: relocation-bearing members such as `files`, `exit` and `xxv` require
their own linkage proof; incomplete DATA such as `new` is rejected; small or
all-zero ambiguous templates remain unknown. Even the single inter-member
alignment bytes are outside these whole-object claims. Unknown game, library,
asset and original-assembly ownership is not inferred from this scan.

The private input is the existing attested CL.LIB, SHA256
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
The existing three vendor CODE proofs pin each retained MAP/MZ calibration and
target view. Their identities are inherited without altering or rebuilding
those producers. Their CODE acceptance is not transferred to DATA; the actual
complete member DATA and all three actual native copies are compared anew.

## Replay and validation

```sh
python3 scripts/review_vendor_data.py --check
python3 scripts/review_vendor_data.py --structural-check
python3 scripts/ownership.py --check --verify-targets
python3 scripts/ci.py
```

The first command requires the private pinned library and retained MAP/MZ files.
The structural command requires public files only and deliberately makes no
claim to replay private bytes. Public CI checks the source pins, target/source
identities, complete boundaries/record coverage, zero authored credit, decision
hash and ownership consistency. Tests reject mutated, duplicate, transferred,
relocated, partial, stale or ambiguous evidence and preserve prior authored
ownership. Native review invokes no compiler, Wine, Ghidra, unpacker or game.
It does not claim two fresh compiled producers or whole-executable equality.

Private discovery evidence is retained in `.analysis/vendor-data-routing/`.

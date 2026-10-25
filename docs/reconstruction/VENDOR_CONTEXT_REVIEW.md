# Artifact-specific CL.LIB ownership review

`review_vendor_context.py` extends the existing MAIN library-ownership review to
OP and MAINE. The public evidence files remain **PROPOSAL** records. Separate,
explicit reviewed decisions now adopt the listed complete contributions below
as third-party library code. Authored credit remains zero and the authored byte
denominator remains null.

| Context | Complete adopted CODE contributions | Bytes | Retained link producers |
| --- | ---: | ---: | ---: |
| OP | 63 | 23,708 | 1 |
| MAINE | 55 | 20,870 | 1 |

This is a distributed-library ownership test. It reconstructs each complete
CL.LIB OMF contribution through its actual link context and compares it with the
original target. It does not claim original C source recovery or two fresh
compiler producers. Authored-source acceptance retains its separate gates.
`CODE` is an OMF segment class; these complete contributions can contain data and
library alignment bytes.

## Revalidation

Public checks require no game, compiler, or private cache:

```sh
python3 scripts/review_vendor_context.py --context op --structural-check
python3 scripts/review_vendor_context.py --context maine --structural-check
python3 -m unittest discover -s tests -p 'test_vendor_context_review.py'
```

Private native checks reread all actual inputs without running DOS tools:

```sh
python3 scripts/review_vendor_context.py --context op --check
python3 scripts/review_vendor_context.py --context maine --check
python3 scripts/review_vendor_context.py --check  # unchanged MAIN contract
```

`--write` refreshes evidence only. It cannot adopt members. MAIN delegates to
`review_vendor.py`; that verifier and its existing proof and decision remain
unchanged.

The OP/MAINE verifier pins the original packed artifact independently from the
retained decoded payload, decoder receipt, relocation stream and canonical
historical two-load proof. It consumes `DecodedUnitImage` directly and creates
no synthetic MZ. Relocation rows retain their observed order and original
frame:offset identity. Two relocated-byte hashes alone cannot distinguish a
permuted relocation stream.

Each context also pins its actual calibration executable and MAP, distributed
CL.LIB, toolchain manifest, and the public verifier/loader/parser source closure.
Nomination requires complete original/calibration byte identity and ordered MZ
identity. Verification then reconstructs the complete original OMF CODE SEGDEF
with gapless LEDATA, actual FIXUPP bindings and observed linker transformations.
Duplicate MAP contributions, ambiguous byte occurrences, unsupported records,
unwritten gaps, overlapping writes and unexplained bytes reject the member.
Structural checks validate public hashes and proof consistency; they explicitly
do not report a replay of private byte evidence.

## Explicit adoption boundary

`ownership.py` consumes the separately reviewed decisions in
[`reviewed_vendor_units.op.json`](../../config/reviewed_vendor_units.op.json)
and [`reviewed_vendor_units.maine.json`](../../config/reviewed_vendor_units.maine.json).
After independent review and all three native context checks, these decisions
explicitly adopted only the 63 OP and 55 MAINE verified members. The proof
records themselves remain unchanged PROPOSAL records. An absent optional
decision still yields zero claims, including during native inventory checks.

Each decision uses schema 1 with artifact `th05-op` or `th05-maine`, decision
`ADOPT_ONLY_LISTED_MEMBERS`, classification `third-party-library-code`, the
complete evidence-file SHA-256, separate packed and payload SHA-256 values, and
a nonempty unique `members` list. Each states
`authored_credit: 0`, `authored_denominator: null`,
`other_members_policy: "unknown"` and `uncovered_gaps_policy: "unknown"`.
Unknown or deferred members cannot be selected. Stale evidence and wrong-context
decisions reject. Adopted extents use the existing overlap checker, which rejects
conflicts with accepted source or other vendor extents. With
`verify_targets=True`, adoption replays the actual private review and compares
its complete result with the reviewed proof.

OP's `xxas`, `farheap`, `signal`, `exec` and `setenvp` remain deferred. MAINE's
`farheap`, `exec` and `setenvp` remain deferred. Their unsupported fixup methods,
incomplete LEDATA or unexplained reconstructed bytes are retained in public
reason records. All uncovered gaps, DATA/BSS and other members remain unknown.
Existing MAIN Master decisions do not transfer to either artifact.

The subsequent root-run `ownership.py --write --verify-targets` passed with
47,855 verified vendor bytes across all contexts and 189,074 unknown bytes.
Authored recovery stayed at 82,266 bytes; its denominator remains null. These
are adoption-time inventory observations, not permanent totals or proof bounds.

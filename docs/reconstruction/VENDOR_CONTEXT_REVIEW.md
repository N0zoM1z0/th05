# Artifact-specific CL.LIB ownership review

`review_vendor_context.py` extends the existing MAIN library-ownership review to
OP and MAINE. The public evidence files remain **PROPOSAL** records. Separate,
explicit reviewed decisions now adopt the listed complete contributions below
as third-party library code. Authored credit remains zero and the authored byte
denominator remains null.

| Context | Original gapless-lane adopted contributions | Original gapless-lane bytes | Retained link producers |
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

The earlier gapless review deferred OP's `xxas`, `farheap`, `signal`, `exec`
and `setenvp`, plus MAINE's `farheap`, `exec` and `setenvp`. Subsequent focused
original-OMF review now **resolves `farheap` and `exec` in both OP and MAINE**
without altering that first, still-valid proposal: all four complete original
CODE segment images (1,115 and 933 bytes per executable) match both original
and calibration native links and all 70 ordered OMF CODE FIXUPP actions per
executable. Exactly **2,040 byte-wise source-written CODE bytes** are adopted
per artifact, while the original **6-byte and 2-byte writable `CS:` state
slots remain `unknown`**, not invented source. The verified source records
include `exec`'s authentic 255-byte LIDATA. There is no authored C++ credit.

Independent [OP](../../config/vendor_reserved_context.op.json) and
[MAINE](../../config/vendor_reserved_context.maine.json) proofs and explicit
adoptions in `config/reviewed_vendor_reserved_context.{op,maine}.json` are
checked with:

```sh
python3 scripts/review_context_reserved.py --context op --check
python3 scripts/review_context_reserved.py --context maine --check
```

## Complete original OMF recovery for the remaining deferred CODE

All four formerly deferred gapless CODE contributions are now source-verified
from actual CL.LIB members, original CODE LEDATA and ordered OMF FIXUPP:

| Artifact | Member | Target load interval | Complete CODE |
| --- | --- | --- | ---: |
| OP | `xxas` | `4457..44E6` | 143 B |
| OP | `signal` | `4D86..5087` | 769 B |
| OP | `setenvp` | `9C30..9C88` | 88 B |
| MAINE | `setenvp` | `9E0C..9E64` | 88 B |

OP's `xxas` and `signal` were deferred because their real OMF sources
contain **GRPDEF target-method 1** bindings to the original DGROUP. The
existing general vendor verifier did not support those bindings. Their
complete original CODE records now resolve directly through the genuine
group frame, without copying instructions or treating any fixup field as
a wildcard. The `signal` member has **55 ordered CODE FIXUPP actions**.

Both `setenvp` instances contain the original TLINK five-byte same-segment
far-JMP lowering (`NOP; NOP; JMP near`), in addition to the known
same-segment far-CALL lowering. Their original and retained-calibration
CODE is identical, with all ten CODE OMF FIXUPP actions resolved. The
different MAIN DATA-frame layout is not imported into either context.

The separate [OP proof](../../config/context_remaining.op.json) and
[MAINE proof](../../config/context_remaining.maine.json), explicit
source-ownership decisions and [native verifier](../../scripts/review_context_remaining.py)
adopt **1,088 complete CODE bytes** with zero game-authored credit.
The checks use the original OMF CODE LEDATAs, actual symbol binding,
full raw original/calibration bytes, ordered original MZ relocations
and unique whole extents:

```sh
python3 scripts/review_context_remaining.py --context op --check
python3 scripts/review_context_remaining.py --context maine --check
```

`--structural-check` validates the public proof without private native
inputs; the ownership map overlays only explicitly selected CODE intervals.
The source members' DATA/BSS/INIT records remain outside these claims.
All other uncovered ranges, runtime writable variables, vendor DATA/BSS
and game sources remain unknown pending their own review.

The original gapless-lane root adoption passed its then-current native
`ownership.py --write --verify-targets` check. Its historical global totals
are **superseded** by later source reviews of `farheap`, `exec`, `setenvp`,
CRT DATA and additional authored functions. Use the generated
[`resources/ownership.json`](../../resources/ownership.json), not old
adoption-time totals, for the current unknown/vendor breakdown. The global
authored denominator remains unreviewed.

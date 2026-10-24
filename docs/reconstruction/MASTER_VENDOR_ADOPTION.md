# Reviewed Master procedure adoption

The twenty procedures in the frozen public Master proposal were independently
reviewed and replayed before their explicit third-party ownership classification. `config/reviewed_master_procedures.json` records that separate
decision. The original proposal, its verifier and its proof hash remain
unchanged; the decision pins the complete public proof file and original
artifact/payload identities.

Only the twenty listed names are adopted. Their376 complete bytes become
`verified-vendor-code`, including9 vendor-owned EVEN padding bytes alongside
367 instruction bytes. This grants0 game-authored bytes. It does not publish
an authored denominator or percentage. Every other Master procedure, the forty
absent/ambiguous/different source candidates, modified library/game code,
DATA/BSS and uncovered gaps remain unknown. The mixed standalone prefix is
not classified as a whole.

`ownership.reviewed_master()` is optional when no explicit decision exists.
When present, it validates the immutable public proof and requires all twenty
unique, explicitly reviewed names. Unknown/deferred names, partial or duplicate
lists, stale proof/target/artifact/classification, changed accounting or policies,
and attempts to grant credit are rejected. With `verify_targets=True`, it calls
the actual `review_master.review_inputs()` native input replay. A saved PASS
record is not a substitute.

MAIN combines CL.LIB and Master claims in a single existing overlay operation.
Any overlap with accepted source, source tables/padding or another vendor claim
fails. The existing CL.LIB decision and `vendor_review_sha256` are unchanged;
Master uses its own `master_vendor_review_sha256` decision digest. Other target
views receive no Master claims.

Public CI adds only `scripts/review_master.py --structural-check`. Private byte
replay remains available through ownership's `--verify-targets` path. The new
decision tests use public/synthetic fixtures and cover optional absence, exact
full extents, unknown gaps, stale identities, unapproved names, accounting and
credit policies, native dispatch, overlap rejection, separate inventory digests,
and the public-only CI command. The adoption helper also completed a real retained-input native replay for all
twenty procedures without compilation, Wine or downloads.

Regenerate the gapless inventory with `scripts/ownership.py --write
--verify-targets`. The reviewed vendor total is3,277 bytes (2,901 CL plus376
Master); authored source counters are unchanged. Public CI checks the saved
inventory and structural evidence without requiring proprietary inputs.

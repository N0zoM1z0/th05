# Reconstruction workflow

1. Read the handoff; inspect `git status --short`.
2. Run `python3 scripts/preflight.py` and attest the selected analysis view.
3. Choose one reviewed function or coherent translation unit. Record artifact,
   segment:offset, complete extent, origin and confidence.
4. Recover semantics and declarations as C/C++; preserve original Borland ABI.
5. Compile in two fresh workspaces with the pinned toolchain. Inspect OMF records,
   segment layout and fixups; compare all bytes in the declared extent.
   Compile only the selected new/affected units. Reuse unchanged accepted units
   and successful tool execution probes after identity checks; use
   `scripts/replay_units.py --plan` or `--units ID...`. Importing a new receipt
   merges it into existing acceptance without rebuilding unrelated units.
6. Reject mismatches. Store compiler experiments privately and retain concise
   replayable observations. Separate source-present from exact acceptance.
7. Run affected checks, public CI, and `git diff --check`. Update progress and
   the handoff and gapless ownership inventory (`scripts/ownership.py --write`);
   commit with `gpt-6.1-sol: ...` and push.

Use one CPU and low scheduling priority for heavy tools. Keep Wine writers
serial and Ghidra's heap bounded. Never modify the original HDI or executables.

OP and MAINE use `--artifact op` / `--artifact maine` on replay and acceptance,
with separate `exact_units.*.toml` and `accepted_units.*.json` files. Their
retained decoded view is pinned by receipt and canonical proof hashes. Replay
and acceptance verify original packed identity, decoded bytes, ordered fixups
and historical two-load observations without running the decoder again. Public
summaries verify the same pinned proof without requiring private game files.

Default compiler binary contexts are M/O/E; a new unit may explicitly set
`binary` for a genuine exception. MAINE's reference build mixes all three
contexts, so follow its real producer rather than forcing every shared TU to E.
`build_reference.py op` or `maine` builds only that artifact's calibration
closure. Calibration and shape surveys are routing evidence with zero credit.

Retained-producer scope review can project complete functions from multiple real
CODE contributions of the same saved replay. It may carry the identical complete
negative-control owner, with unchanged identity, to prove the same strict oracle.
All original results are validated, including excluded failures. A scope must
belong to exactly one original whole contribution; overlaps, changed controls
and stale source/producer identities fail. No new compilation is claimed.

Retained whole DATA review uses `review_saved_data.py --artifact ARTIFACT
--from-receipt PATH --unit DATA_ID --output PATH`. It revalidates two archived
original whole-CODE producers with identical actual compiler argv and complete
source/binding/tool identities, then compiles exactly one fresh DATA mutation.
It never claims fresh positive compilations. Original aggregate failures stay
in the archived parent, and all parent results are rechecked. A parent lacking
saved actual argv needs a focused normal replay instead.

A focused replay checks the first producer's actual complete MAP extent before
starting its second producer. An invalid boundary or size stops immediately,
retaining the first build artifacts and avoiding the unnecessary second build.
Accepted scopes still require both independent cold producers and their real
compiled negative. Raw/fixup mismatches with valid extents continue to retain
both producer results for strict subset and retained-scope review.


Compiler wrapper modules use explicit relative DOS8.3 paths, including directory
components. Replay validates these before target access or tool execution.
A nine-character stem can silently compile under a Wine short-name alias,
leaving the intended object name absent. Maintained source paths remain their
normal descriptive paths; only the small generated wrapper uses the DOS alias.


A normal multi-owner replay compiles one configured negative owner. Its shared
oracle control does not imply a separate mutation was compiled for every owner.
Use `scripts/supplement_negative.py --parent RECEIPT --unit ID --output PATH`
when an additional owner needs its own mutation: it first revalidates every
saved parent result and actual source/OMF/MAP/MZ dependency, retains both existing
positive producers, and compiles exactly one negative. It changes no acceptance
or authored-byte counts. `--check PATH/receipt.json` rechecks the parent, source
mutation, actual argv, OMF, linked output, pinned tool receipt and rejection
without compiling. Failed/stale parents stop before new compilation or output creation.

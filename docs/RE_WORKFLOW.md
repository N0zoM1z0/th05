# Exact reconstruction workflow

1. Read the current handoff, inspect `git status --short`, and run preflight.
2. Choose one function or coherent source unit. Confirm the pinned target,
   complete extent, ABI and source ownership.
3. Recover maintained C/C++ and replay only the new/affected unit. Inspect its
   actual OMF/MAP, complete bytes and original ordered fixups. Stop after a
   first-producer boundary/size failure; revise the source instead of adding tests.
4. Import a passing receipt. Reuse unchanged accepted evidence; refresh only
   the demonstrated dependency closure when a shared input changes.
5. Update progress/ownership for acceptance changes, run `git diff --check`,
   write a short handoff and commit/push substantive work.

Typical commands:

```sh
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/RUN
python3 scripts/progress.py --accept .analysis/unit-replays/RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
```

Use `--artifact op`, `--artifact maine` or `--artifact zun` for their own
manifests and ledgers. ASM uses `scripts/replay_asm_family.py` and remains a
separate source classification. Run Wine/Borland and Ghidra serially on one CPU.

The exact replay is the primary check. Ordinary function recovery does not
require new unit tests, CPU models, allocation-failure/null-pointer cases,
exhaustive inputs, fault injection or whole-game validation. A focused semantic
experiment is useful only when it resolves a concrete recovery question.
Do not expand it into another completion requirement.
Preserve the original error handling and unchecked operations; defensive fixes
are outside ordinary exact recovery.

`python3 scripts/ci.py` is the lightweight public consistency check. Run relevant
tooling tests when changing the oracle/build scripts; `--full` is available for
an intentional full tooling regression. Do not run the full suite after each
source candidate. Existing receipts can share their compiled oracle control;
additional per-function controls are optional investigations.

Documentation and test cleanup need no compiler replay or generated progress
refresh when source, build inputs and acceptance are unchanged. Retired one-off
diagnostics remain in Git history; they are not part of the active workflow.

[Acceptance](ORACLES.md) defines exactness. The optional
[receipt format reference](reconstruction/ORACLE_FORMATS.md) documents special
DATA, ASM and retained-producer lanes; it is not a checklist for every target.

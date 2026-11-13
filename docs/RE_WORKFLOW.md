# Exact reconstruction workflow

Follow the priority rules in [AGENTS.md](../AGENTS.md) and the current
[agent handoff](RE_HANDOFF.md). Prefer the shortest useful loop and preserve
original source, ABI and relocation behavior.

1. Inspect `git status -sb` and the current handoff. Run preflight when starting
   in a new environment or when target/toolchain identity needs re-attestation;
   documentation-only work does not need it.
2. Choose one function or coherent source unit. Confirm its complete original
   extent, ABI, foreign interfaces and physical ownership.
3. Recover maintained C/C++ and replay only the new or affected complete units.
   Inspect OMF/MAP boundaries, full raw bytes and the original ordered fixups.
   Recheck consumers of changed shared inputs.
4. Import a passing receipt into the correct artifact ledger. Reuse unchanged
   accepted evidence after dependency identity checks.
5. Update progress/ownership only for acceptance changes, inspect
   `git diff --check`, update the handoff when priorities change, and commit
   locally. Push only with explicit permission.

Typical focused commands:

```sh
python3 scripts/replay_units.py --plan
python3 scripts/replay_units.py --units UNIT_ID --output .analysis/unit-replays/RUN
python3 scripts/progress.py --accept .analysis/unit-replays/RUN/receipt.json --write
python3 scripts/ownership.py --write
python3 scripts/ci.py
```

Use `--artifact op`, `--artifact maine` or `--artifact zun` for their own
manifests and ledgers. ASM uses `scripts/replay_asm_family.py` and remains a
separate ownership lane. Serialize Wine/Borland and Ghidra work.

Documentation and knowledge edits require no compiler replay or generated
progress refresh when source, build inputs and acceptance are unchanged.
Ordinary function recovery does not require new CPU models, allocation-failure
or null-pointer tests, exhaustive inputs, fault injection or whole-game
validation. `python3 scripts/ci.py` is the lightweight public consistency
check; run relevant tooling tests when changing the oracle/build scripts.
`--full` is an intentional full tooling regression, not a per-function gate.

[ORACLES.md](ORACLES.md) defines acceptance. The optional
[receipt format reference](reconstruction/ORACLE_FORMATS.md) documents
special DATA, ASM and retained-producer lanes; it is not a checklist for every
unit.

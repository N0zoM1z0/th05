# TH05 reconstruction

The goal is at least 98% **authored bytes exact**, built from maintained source.
Commit messages use `gpt-6.1-sol: ...`. Keep code and documentation in English.

Read `docs/RE_HANDOFF.md`, `docs/RE_WORKFLOW.md` and `docs/ORACLES.md` first.
Run `git status --short` and `python3 scripts/preflight.py` before target work.

- Attest targets against `config/targets.toml`. The supplied Japanese copy has
  candidate-local-attested provenance, not independently proved pristine status.
- Preserve 16-bit Borland ABI, near/far pointers, Pascal cleanup, memory model,
  segment groups, relocation ownership and linker order.
- Source belongs under `src/{main,op,maine,zun,shared}/`, by subsystem.
- ReC98 and TH03/TH04 are candidate references; their acceptance never transfers.
- Never count copied target bytes, target-derived instruction transcriptions,
  placeholders, padding or normalization as authored exact source.
- Classify reviewed genuine original assembly separately. Compiler-generated
  code must be recovered as C/C++ before counting as authored C/C++ bytes.
- Source presence, semantics, exact units, decoded bytes, packed bytes and whole
  executable acceptance are separate claims. Never combine their percentages.
- Unit acceptance requires pinned target/toolchain, reviewed complete boundaries,
  two fresh deterministic builds, OMF integrity, full raw-byte comparison and
  relocation agreement. Unknown ownership stays in the denominator until reviewed.
- Keep proprietary tools, games/assets/images, databases and outputs private in
  ignored directories. Ghidra projects use `ghidra-project/`, not `.analysis/`.
- Serialize Wine/Borland builds and Ghidra. Use one CPU, nice priority and bounded
  heap/memory; avoid duplicate tool downloads and unbounded process pools.
- Run affected checks, `python3 scripts/ci.py`, and `git diff --check` before
  committing; update the handoff and generated progress. Commit and push often.

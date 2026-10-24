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

## User-directed incremental work

The user explicitly requested faster progress on 2026-10-24: replay only the
necessary units. Reuse accepted unchanged evidence and objects after checking
their actual dependency identities. Compile/replay new or affected units;
do not automatically cold-replay the entire accepted set. Reuse successful
toolchain execution probes when all relevant installed surfaces and the pinned
manifest remain unchanged. Shared ABI, flags, binding or layout changes require
only their demonstrated affected closure, with broader replay when necessary.

## Borland context checks before replay

- Keep `#pragma option -zC/-zP` before all C/C++ tokens. Use `#pragma codeseg
  SEG GROUP` for selectors after includes. Preserve the actual first declaration
  context for every near callback.
- `.model large` already declares word-aligned `_DATA` and `_BSS`; do not
  redeclare them byte-aligned. Keep every individual ORG below 64 KiB.
- Bind actual compiler EXTDEF names (including Borland's 31-character truncation).
  Place even empty foreign compiler SEGDEFs at their real group context: a
  differently named scaffold segment can leave an empty segment beyond the
  group's 64 KiB window. Check actual OMF GRPDEF before changing source ABI.

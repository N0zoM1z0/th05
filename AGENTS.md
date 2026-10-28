# TH05 reconstruction

Goal: at least 98% **authored bytes exact** from maintained source.
Commit messages use `gpt-6.1-sol: ...`. Code and documentation stay in English.
Read `docs/RE_HANDOFF.md` for current work and `docs/ORACLES.md` for acceptance.
Run `git status --short` and `python3 scripts/preflight.py` before target work.

## Work priority

- Spend time recovering C/C++ and matching original bytes. Run only new or
  affected units; reuse unchanged accepted objects, evidence and tool probes
  after dependency identity checks. Do not cold-replay the whole accepted set.
- Do not add allocation-failure, null-pointer, defensive-behavior, exhaustive
  input, fault-injection or whole-game tests to ordinary reconstruction work.
  Use a small semantic check only when a specific source/ABI ambiguity blocks
  exact recovery; it is not an additional acceptance gate.
- New C/C++ functions do not need new Python tests or CPU behavior models.
  Test the oracle/build tools when those tools change. `scripts/ci.py` checks
  source/configuration and progress; `--full` is an explicit tooling test run,
  not a requirement for every function or commit.
- Keep evidence concise: target extent, source/ABI decision, byte/fixup result
  and receipt. Historical investigations are reference, not recurring tasks.
- Run the affected exact replay and `git diff --check`. Update generated
  progress/ownership when acceptance changes, leave a short handoff, and
  commit and push substantive progress.

## Exactness and source

- Pin targets/toolchain and review complete boundaries. Acceptance needs two
  deterministic builds, valid OMF, full raw bytes and original relocation order.
  Keep the replay's shared oracle control; extra per-function negatives are
  unnecessary unless the oracle itself is under investigation.
- Preserve the 16-bit Borland ABI, near/far pointers, Pascal cleanup, memory
  model, segment groups and linker order. Source belongs under
  `src/{main,op,maine,zun,shared}/`, by subsystem.
- ReC98 and TH03/TH04 are references; their acceptance does not transfer.
  Do not count target-byte copies, instruction transcriptions, placeholders,
  padding or normalization as authored exact source. Review original ASM
  separately; recover compiler-generated code as C/C++.
- Compare padding normally but give it zero authored credit. Keep source,
  semantics, exact units, decoded/packed files and whole EXE claims separate.
  Unknown ownership remains unknown; the global denominator is not yet reviewed.
- The supplied Japanese copy is candidate-local-attested, not independently
  proved pristine. Keep proprietary inputs and outputs in ignored directories;
  Ghidra projects use `ghidra-project/`.
- Serialize Wine/Borland and Ghidra. Use one CPU, nice priority and bounded memory.

## Borland details that affect bytes

- Put `#pragma option -zC/-zP` before C/C++ tokens; use `#pragma codeseg SEG GROUP`
  after includes. Preserve the first declaration context of near callbacks.
- `.model large` already declares word-aligned `_DATA`/`_BSS`. Keep each ORG
  below 64 KiB, bind actual EXTDEF names including 31-character truncation,
  and place empty foreign SEGDEFs in their actual group context.

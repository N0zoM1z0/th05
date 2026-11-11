# TH05 reconstruction

## Highest priority: lightweight exact reconstruction and useful knowledge

These are the user's current workflow requirements. They override older
instructions that mandate broad CI, repeated preflights, document/source-pin
refreshes, per-checkpoint audits or extra workflow machinery. Preserve the
actual exactness, target identity, natural-source and state-isolation rules.

- Prioritize exact reconstruction and reusable knowledge. Use the shortest
  useful loop: inspect relevant state, analyze/edit, compile and compare the
  affected scope, retain useful learning, and create a coherent checkpoint.
- Use existing repository scripts and composable Bash. Add only the smallest
  change needed for an observed problem. Do not introduce a framework, schema,
  registry, state machine, generalized validator, test family or reporting
  process merely to make a local reconstruction task look more engineered.
- Documentation, knowledge and handoff edits require no compiler, analyzer,
  full CI, cold replay or receipt refresh. Inspect the diff. Check syntax only
  for machine-readable inputs actually changed.
- Source changes need the complete affected exact comparison, including its
  owned extents and relocations. Recheck known consumers of changed shared
  inputs. Tool changes need relevant positive/negative cases and a bounded
  real smoke. Run a broad suite only for an explicit request or a demonstrated
  impact that cannot be narrowed; state that reason first.
- Do not add tests or live freshness gates for prose hashes, prompt wording,
  progress totals, handoff source-SHA tables or ordinary source spelling.
  Bind exact evidence to executable inputs and relevant verification settings.
  Keep Git metadata as provenance. A document genuinely consumed by a build
  remains a build input. Never edit historical receipts to manufacture a pass.
- Plain Markdown is sufficient for knowledge: record the finding, applicable
  target/compiler/scope, evidence links, useful failed attempts and open
  questions. No mandatory JSON conversion, promotion workflow or test per note.
  Search relevant sections; do not read an entire large knowledge journal.
- Write documentation and knowledge in natural, fluent English. Lead with the
  concrete finding and connect the evidence and next action clearly. Remove
  filler, circular restatements, repeated conclusions and unnecessary jargon.
  Do not add defensive-claim boilerplate. State a real uncertainty or scope
  limit once when it changes a decision; do not repeat disclaimers about what
  a note does not prove, certify or authorize. Prefer a small useful note over
  an exhaustive report that is difficult to read.
- Keep handoff focused on current work, evidence references, blockers and the
  next useful action. Generate progress from canonical ledgers; avoid manual
  duplicate counts, recurring full reports and unrelated documentation chores.
- Retain necessary inputs, current source/ledgers/replay tools and concise
  knowledge. Remove superseded builds, duplicate evidence, historical archives
  and cleanup reports; a document reference alone is not a retention reason.
  Keep a difficult compiler context only while it helps an unresolved problem.
- Default CI checks the complete public checkout without originals or private
  tools. Run specialized tooling tests only for the affected change.
- Preserve dirty/untracked work, targets, useful evidence, game-specific Wine
  prefixes and analyzer projects. Exactness still requires a complete strict
  comparison; knowledge and successful commands alone confer no exact credit.


Goal: at least 98% **authored bytes exact** from maintained source.
Commit messages for this workstream use `gpt-web: ...` as requested. Code and documentation stay in English.
Read `docs/RE_HANDOFF.md` for current work and `docs/ORACLES.md` for acceptance.
Run `git status --short` and `python3 scripts/preflight.py` before target work.

## Work priority

- Spend time recovering C/C++ and matching original bytes. Run only new or
  affected units; reuse unchanged accepted objects, evidence and tool probes
  after dependency identity checks. Do not cold-replay the whole accepted set.
- Preserve original behavior, including unchecked allocations and pointers.
  Do not add defensive fixes or require new error handling during reconstruction.
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
- Replay affected units when source or build inputs change; documentation and
  test cleanup need no compiler run. Run `git diff --check`, update generated
  progress/ownership only when acceptance changes, leave a short handoff, and
  commit substantive progress locally. Push only with permission and remote access.

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

## Shared Factory runtime

Follow [the shared tools instructions](docs/SHARED_TOOLS.md). Ghidra/JDK and
Wine executables are shared through Factory; repository scripts also work
without MCP. Use `scripts/shared_runtime.py` and the existing compiler/analysis
frontends. Keep this game's prefix, analyzer project, Java home/cache, target
and compiler profile isolated. Do not install duplicate tools or inherit
another game's `WINEPREFIX`. This shared-runtime procedure supersedes older
per-repository installation instructions; pinned versions/hashes still apply.

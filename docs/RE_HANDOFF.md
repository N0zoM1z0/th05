# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Public repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: 10 bounded C++ units, 52 complete functions, 9,088 compared
bytes and 9,072 authored code bytes: 8,796 instructions plus 276 bytes of
semantic compiler switch tables. Sixteen checked padding bytes receive no
credit. `config/accepted_units.json` records each source-current scope.
Global percentage remains unmeasured pending complete ownership review.

## Retained evidence

| C++ scope | Private replay under `.analysis/unit-replays/` |
| --- | --- |
| Player angle, bullet tuning, Boss movement, resident CFG | `boss-cfg-a` |
| Boss explosion | `boss-explosion-a` |
| HUD overlay | `hud-overlay-a` |
| Reimu shots | `reimu-shots-a` |
| Marisa shots | `marisa-shots-a` |
| Yuuka shots | `yuuka-shots-a` |
| Mima shots | `mima-shots-b` |

Every accepted scope has two isolated deterministic producers, full raw/fixup
comparisons, pinned tools, actual OMF dependencies and a compiled mutation
control. Acceptance re-reads saved MZ/MAP/OMF producers and frozen inputs.
Bindings preserve actual ABI and original frames; no whole-program linkage
claim is made. Per-owner notes describe the interfaces and boundaries.

Standalone ZUN `-M` is separately accepted: 311 complete COM bytes (142 code,
169 data) from semantic ASM with inferred original style. Evidence:
`.analysis/zun-memory/first-b`, `config/zun_memory_acceptance.json` and
`src/zun/memory/README.md`. It is not C++ credit or complete outer ZUN exactness.
The launcher parser validates all 18,116 bytes as a physical partition.

## Incremental work

The user requested faster progress: replay only new or affected units.
`python3 scripts/replay_units.py --plan` exits before tools when no work is
needed. `--units ID...` selects a focused replay; importing a receipt merges
only those scopes. Successful execution probes are reused after checking
manifest and actual installed compiler/header/library surfaces. Do not rerun
all accepted units, unpackers or Ghidra without a relevant changed dependency.

Complete-function scopes can share one actual translation-unit compilation per
round. Their MAP boundaries must be adjacent real function publics in the same
CODE contribution. Unaccepted neighbors earn no credit. Existing complete-TU
entries and evidence remain valid without recompilation.

Next candidate: `src/main/boss/background.cpp`, 19 functions / 3,254 original
instruction bytes. It is not accepted. Upstream fake-zero codegen helper was
removed; a natural signed-zero comparison is expected to differ by one byte.
Sixteen small compiler probes in `.analysis/compiler-probes/zero-compare-a`
all emitted OR AX,AX rather than original CMP AX,0. Do not add fake zero
symbols, opcode arrays, compiler-body ASM or inert barriers to force bytes.
Diagnose a single natural TU, then recover independently matching complete
functions. Preserve unknown ownership in the denominator.

## Target and tool state

`config/targets.toml` pins the supplied Japanese image and four executables.
Provenance is candidate-local-attested; independent pristine confirmation is
open. Originals and tools are private. MAIN is ordinary MZ with 998 fixups;
OP/MAINE are DIET-packed MZ; ZUN is plain COM. Decoded OP/MAINE payloads and
two-load-segment observations are retained in `.analysis/decoded`.

The first pinned-reference MAIN calibration completed 83 serial steps but
failed whole-program equality. It creates no authored credit. Masked discovery
and vendor-library ownership candidates remain diagnostic; see the ownership
survey. Reference names and accepted TH03/TH04 scopes never transfer acceptance.

Independent Wine state and pinned Borland tools pass executable/OMF probes.
Ghidra 12.1.3 / Temurin 21 pass identity checks. MAIN's loader-only project
`ghidra-project/TH05-main-loader` passes byte/fixup database attestation; bounded
first-unit disassembly checks pass. Full autoanalysis exceeded 768 MiB: use
loader-only defaults and bounded ranges. Failed old projects are not evidence.

Serialize heavy jobs with `.analysis/borland.lock` and `scripts/run_heavy.sh`
(one CPU, 35% quota, 768 MiB, no swap, low priority). TH03 has unrelated dirty
work: never modify it. TH04 is a read-only reference.

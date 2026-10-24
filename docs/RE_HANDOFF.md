# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Public repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: 29 bounded C++ units, 80 complete functions, 13,583 compared
bytes and 13,567 authored code bytes: 13,291 instructions plus 276 bytes of
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
| Bullet generation clipping | `bullet-clip-d` |
| Stage initialization | `stage-setup-a` |
| 17 complete Boss background functions | `boss-background-functions-a` (explicit subset) |

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

Boss background now has 17 accepted complete functions / 2,891 bytes. The
particle renderer remains inexact (natural OR AX,AX versus original CMP AX,0).
A separate CODE contribution follows it; one uncredited origin hole between
actual compiler contributions preserves later function positions. The complete
159-byte original particle scope remains unaccepted. Hexagram drawing's 204
bytes match raw, but its ordered fixup list differs across a compiler LEDATA
boundary, so that whole function also remains unaccepted. No ordering is sorted
or normalized. Both exclusions remain unknown ownership in the global review.

The original 18-function replay receipt honestly records aggregate failure.
Explicit subset acceptance imported only its 17 fully passing functions after
rechecking every saved producer and the compiled negative control. The original
receipt is unchanged. A default acceptance still requires aggregate success.
Use `progress.py --accept RECEIPT --units ID...` for a reviewed subset, including
the negative-control owner; this does not run compilation.

Stage initialization covers ten complete functions / 1,510 code bytes. Its real
far Pascal rank-selector calls naturally link to the original NOP/PUSH CS/near
CALL shape. Its 189 bytes of semantic initialized flag/filename DATA also match
in both saved producers, recorded separately as a private observation with no
additional progress credit. Source notes explain the corrected original end
boundary; the survey's extra score function does not belong to this extent.

Next natural candidate: cheeto spawning and homing update, prepared independently
under the bullet owner. Continue focused compilation and complete-function
acceptance. Do not restore fake-zero helpers or hand-emitted compiler bodies.

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

# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Public repository: https://github.com/N0zoM1z0/th05 .

Current acceptance: 33 bounded C++ units, 89 complete functions, 16,030 compared
bytes and 16,014 authored code bytes: 15,718 instructions plus 296 bytes of
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
| Cheeto allocation and homing update | `cheeto-update-b` |
| Regular and special bullet update | `bullet-update-d` |
| Enemy rendering (maintained TH04 donor) | `enemies-render-b` |
| OP decoded sound-driver interrupt | `op-kaja-a` |
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

Cheeto allocation/homing now passes its complete 592-byte contribution and
compiled collision-width mutation. The template view is 25 bytes inside a true
26-byte custom slot; compiler assertions verify all real field offsets.

Regular/special bullet update now passes all five functions / 1,619 code bytes
(1,599 instructions plus 20 compiler table bytes), four ordered fixups and the
compiled reflection mutation. The real sprite enum domain is word-sized; its
partial byte enum was corrected. The cross-segment HUD callback retains main_01
at its first declaration. Neither fix changes an accepted shared header.

Enemy rendering now adds a full 207-byte natural C++ function reused from
maintained TH04 source, with TH05's independently checked 64-byte enemy state,
32-slot pool and two original zero-frame far fixups. Its width mutation fails.
Next natural candidate: OP main menu, 3,291 original bytes. It requires explicit
CP932 staging for maintained UTF8 Japanese UI literals; only that owner opts in. Continue focused compilation and complete-function
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

OP/MAINE unit contexts use separate configs/ledgers with pinned retained decoded
views; MAIN defaults and old evidence stay unchanged. The first decoded unit, OP's complete 29-byte Kaja driver interrupt, now
passes two fresh producers, a compiled MIDI-routing mutation and saved artifact
revalidation. The original following NOP is outside the accepted function.
MAIN's ledger is unchanged by this OP import. OP's first reference calibration completed 47 serial steps at
`.analysis/builds/op-calibration-a`; whole-file equality fails, with zero credit.
The decoded OP survey `.analysis/cpp-candidate-survey-op.json` routes 21 unique
C++ contribution shapes / 12,288 candidate bytes. Investigate its natural main
menu first. No new unpacking run was needed. `survey_th04_reuse.py` separately
routes maintained TH04 function candidates; 63 unique shapes / 4,439 bytes are
only diagnostics and include possible false complete boundaries.

MAINE's first isolated calibration also completes in
`.analysis/builds/maine-calibration-a` (36 steps, complete-file mismatch, zero
credit). Its decoded survey routes 17 unique shapes / 5,678 candidate bytes,
including a 2,848-byte cutscene candidate. Reuse both retained calibration maps;
do not rebuild them or re-decode their unchanged original targets.

New Japanese UI owners may opt into `source_encoding = "cp932"`. Canonical
snapshots remain UTF8; the compiler consumes CP932 files with separately saved
byte hashes. Import reconstructs and checks both positive and mutated producer
inputs, including the assembled bindings.asm alias. Old MAIN entries remain raw
and retain their existing evidence; a legacy saved producer was rechecked
without compilation after this validator change.

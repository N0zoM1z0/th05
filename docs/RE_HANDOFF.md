# TH05 handoff

Read [workflow](RE_WORKFLOW.md) and [acceptance](ORACLES.md), then run
`git status --short` and `python3 scripts/preflight.py`. Continue recovering
both major boss functions and their leaves. Old failed attempts are evidence,
not proof that a different natural source context cannot work.

## Accepted state

328 bounded C/C++ CODE/DATA units, 513 complete function occurrences:
**102,687 authored bytes exact** = 87,350 CODE + 15,337 initialized DATA.
CODE is 86,558 instruction + 792 compiler-table bytes. Complete compared
extents total 102,774, including 87 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 394 | 66,164 | 3,091 |
| OP | 62 | 11,251 | 8,649 |
| MAINE | 56 | 9,613 | 3,597 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 7,020 instruction + 210 dispatch-table + 24 semantic
CODE-coordinate + 64 DATA bytes; 7,388 compared bytes include 70 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. Unknown ownership remains
**123,333 bytes**, including MAIN 43,623. The global authored denominator and
percentage are unreviewed; the at-least-98% goal is not complete.
[Generated progress](PROGRESS.md) and [ownership](../resources/ownership.json)
are authoritative.

Latest exact recovery: `main-yumeko-swords-render`, MAIN `[143E0,14422)`,
66 instruction bytes/one complete function, accepted in `5c3466b`. No NOP,
table, padding or relocation. Receipt:
`.analysis/unit-replays/main-yumeko-swords-render-a/receipt.json`, SHA-256
`b1bd8679efe138790eec8986c303143b5a1194a3f664f1ce7873f409882ea5e0`.
Later compiler trials add no exact credit; maintained source was restored.

## Useful next work

| Complete native scope | Current evidence | Details |
| --- | --- | --- |
| Yumeko sword updater (283 bytes) | Natural C++ emits 280; two merged jumps and a one-byte-longer Y calculation explain the gap. `-O-` and control-flow variants fail. | [Updater](../src/main/boss/yumeko/swords_update.md) |
| Yumeko aimed swords (354) / laser-swords (428) | Both raw-equal; original relocation order differs standalone. Genuine allocator/updater/pattern context restores aimed order but starts three bytes early. `-y` does not fix the standalone order. | [Attacks](../src/main/boss/yumeko/laser_swords.md) |
| Dialog opcode (456 bytes) | Direct compiler emits 455; unchanged compiler-generated ASM assembled with TASM reproduces 456 raw bytes, but reverses original fixup order. No acceptance. | [Interpreter](../src/main/dialog/opcode.md) |
| Staff updater (626) / renderer (861) | Current full-family output 623/858. Declaration, class API, expression and scoped-option trials do not recover the pointer loads; source restored. Fifteen other functions remain accepted. | [Staff family](../src/maine/staff/full.md) |
| Staff controller (991 bytes) | All raw bytes match; standalone fixups form one descending run instead of the original two. Bitmap predecessor (126) still compiles to 211. | [Controller](../src/maine/staff/controller.md) |
| Shinki wing (386) / ball updater (220) | Wing raw-equal with wrong order; ordinary scalar ball candidate 232. | [Wing/balls](../src/main/boss/shinki/wing_preparation.md) |
| B4 ball updater (273 bytes) | Natural 278; eager-delta 290 and cleanup-label 278 alternatives fail. | [B4](../src/main/boss/mai_yuki/b4ball_render.md) |

Generic boss collision (43) and Shinki particle renderer (159) also remain inexact.
Other retained candidates are indexed in
[UNACCEPTED_COHORTS.md](reconstruction/UNACCEPTED_COHORTS.md).
The major boss update callbacks already have accepted owners; do not replay
those unchanged functions while investigating their remaining neighbors.

## Continue incrementally

`python3 scripts/replay_units.py --plan` reports the necessary MAIN closure;
use `--artifact op`, `maine` or `zun` for those manifests. Replay new/affected
units only. Reuse unchanged accepted dependencies and tool execution probes
after checking their identities. Preserve the complete ABI, raw bytes and
original relocation order; never sort or patch the output.

Normal recovery needs no new Python tests, CPU behavior models, allocation
failure/null-pointer checks or per-function supplementary negatives. The normal
replay's shared compiled control is sufficient. Preserve original unchecked
behavior. `python3 scripts/ci.py` is lightweight; `--full` is opt-in for tooling
work. Documentation cleanup needs no compiler replay or progress regeneration.

## Workspace and evidence

No compiler or Ghidra job is running. Current baseline and raw-equal diagnostics
remain under `.analysis/native-producers/`. The private
`single_main_producer.py` / `single_native_producer.py` run one diagnostic
producer, never an acceptance receipt. Wine/Borland/Ghidra remain serialized.
All four incremental plans are empty after cleanup; no compiler was run.

Handoff cleanup archived 24 terminal alternative producers plus duplicate
backups and unused assembler extraction. The two obsolete combined wrappers
and their binders were removed; semantic bodies and accepted owners remain.
See [local storage](LOCAL_STORAGE.md) for the archive, restoration commands and
the current 328-record/232-receipt inventory. All accepted evidence stays live.
Retired zero-compare, boss-background and supplemental-negative tools remain
in Git at `3af324e`; they are not part of the active workflow.

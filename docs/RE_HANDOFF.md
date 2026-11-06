# TH05 handoff

Read [workflow](RE_WORKFLOW.md) and [acceptance](ORACLES.md), then run
`git status --short` and `python3 scripts/preflight.py`. Continue recovering
both major boss functions and their leaves. Old failed attempts are evidence,
not proof that a different natural source context cannot work.

## Accepted state

341 bounded C/C++ CODE/DATA units, 528 complete function occurrences:
**104,046 authored bytes exact** = 88,565 CODE + 15,481 initialized DATA.
CODE is 87,757 instruction + 808 compiler-table bytes. Complete compared
extents total 104,134, including 88 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 407 | 67,337 | 3,235 |
| OP | 63 | 11,272 | 8,649 |
| MAINE | 57 | 9,634 | 3,597 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 7,020 instruction + 210 dispatch-table + 24 semantic
CODE-coordinate + 64 DATA bytes; 7,388 compared bytes include 70 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. Unknown ownership remains
**121,973 bytes**, including MAIN 42,305. The global authored denominator and
percentage are unreviewed; the at-least-98% goal is not complete.
[Generated progress](PROGRESS.md) and [ownership](../resources/ownership.json)
are authoritative.

Latest exact recovery:63 instruction bytes across three complete occurrences
of the shared FAR Pascal `frame_delay(int)`, with no DATA or padding credit:

| Unit | Native load scope | Bytes | Receipt under `.analysis/unit-replays/` |
| --- | --- | ---: | --- |
| `main-frame-delay` | `[15102,15117)` | 21 | `main-frame-delay-exact/receipt.json` |
| `op-frame-delay` | `[E15E,E173)` | 21 | `op-frame-delay-exact/receipt.json` |
| `maine-frame-delay` | `[F288,F29D)` | 21 | `maine-frame-delay-exact/receipt.json` |

The signed argument retains its unsigned-word wait semantics. DOS `peek`
transports it from the genuine SS:SP+4 boundary; the volatile counter comparison
is C++. The old survey's22nd byte is outside the function and uncredited.
Each artifact passes its own two deterministic builds, valid OMF, complete raw
bytes/ordered fixups and compiled reset-to-one mutation. No old function or
shared header changed. See [source/ABI review](../src/shared/hardware/frame_delay.md).

The previous dialog resource bank133 and far script pointer4 remain accepted.
Their [resource review](../src/main/dialog/resources.md) records all17 semantic
fields and original pointer fixup `[2]`; intervening graphics remain foreign.

The stage-two boundary was missed by the old prefix survey's543-byte reference
public spacing: original RET ends at116FF and the accepted initializer begins
at11700. The refined short-prefix routing stays private and is not acceptance.
Its only purpose is to identify complete scopes for native review.

The Cheeto renderer established documented `-G` speed generation as the natural
source context for the original PUSH BP/MOV BP,SP/SUB SP prologue. This also
resolved the former bullet-rendering blocker with ordinary register-qualified
pattern/pointer locals. Shared headers, full types, semantics and hardware
interfaces remain unchanged. [Compiler notes](reconstruction/BORLAND_NOTES.md)
and each source's adjacent Markdown record complete scopes, ABI and receipt
hashes. The previous five explosion-creation functions remain accepted.

Alice's independent callback trials avoid compiling the accepted puppet owner.
Ordinary register declarations restore the native pattern/left allocation;
the joined byte-frame version still emits146 because of a six-byte store/load,
and a simple inline quarter-frame helper emits148 with duplicated division.
An ordinary register-byte declaration also leaves146 unchanged.
Both failed first producers are retained, experimental files removed and
baseline source unchanged. The earlier conditional helper's543-byte combined
failure is historical. [Details](../src/main/boss/alice/foreground.md).
No new Alice credit is claimed; defeat/collision is unchanged.
One new ordinary-register collision diagnostic still emits46 versus43; the
maintained source and binder were restored exactly. A CDG-free-all loop emits15 versus14 because
the genuine far external call retains a relaxation NOP. It is also unaccepted
and its experimental source was removed. Both frozen diagnostic inputs remain
under `.analysis/native-producers/`; no signature or output is patched.

## Useful next work

| Complete native scope | Current evidence | Details |
| --- | --- | --- |
| Yumeko sword updater (283 bytes) | Natural C++ emits 280; two merged jumps and a one-byte-longer Y calculation explain the gap. `-O-` and control-flow variants fail. | [Updater](../src/main/boss/yumeko/swords_update.md) |
| Yumeko aimed swords (354) / laser-swords (428) | Both raw-equal; original relocation order differs standalone. Genuine allocator/updater/pattern context restores aimed order but starts three bytes early. `-y` does not fix the standalone order. | [Attacks](../src/main/boss/yumeko/laser_swords.md) |
| Dialog opcode (456 bytes) | Direct compiler emits 455; unchanged compiler-generated ASM assembled with TASM reproduces 456 raw bytes, but reverses original fixup order. No acceptance. | [Interpreter](../src/main/dialog/opcode.md) |
| EMS boss-face preload (154) | Full natural family is raw-equal. Original scoped fixups `[71,24,133,114]` differ from compiler `[133,114,71,24]`; a fresh `-y` diagnostic changes neither. | [EMS cache](../src/main/ems/ems.md) |
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
The MAIN/OP/MAINE incremental plans are empty after the three focused VSync
replays. No whole accepted-set replay was run.

Handoff cleanup archived 24 terminal alternative producers plus duplicate
backups and unused assembler extraction. The two obsolete combined wrappers
and their binders were removed; semantic bodies and accepted owners remain.
See [local storage](LOCAL_STORAGE.md) for the archive, restoration commands and
the prior cleanup's 328-record/232-receipt inventory. Subsequent recoveries add
thirteen records/twelve receipts; all accepted evidence stays live.
Retired zero-compare, boss-background and supplemental-negative tools remain
in Git at `3af324e`; they are not part of the active workflow.

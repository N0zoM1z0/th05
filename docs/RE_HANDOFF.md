# TH05 handoff

Read [workflow](RE_WORKFLOW.md) and [acceptance](ORACLES.md), then run
`git status --short` and `python3 scripts/preflight.py`. Continue recovering
both major boss functions and their leaves. Old failed attempts are evidence,
not proof that a different natural source context cannot work.

## Accepted state

349 bounded C/C++ CODE/DATA units, 533 complete function occurrences:
**104,276 authored bytes exact** = 88,741 CODE + 15,535 initialized DATA.
CODE is 87,933 instruction + 808 compiler-table bytes. Complete compared
extents total 104,364, including 88 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 410 | 67,419 | 3,253 |
| OP | 64 | 11,319 | 8,667 |
| MAINE | 58 | 9,681 | 3,615 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 7,020 instruction + 210 dispatch-table + 24 semantic
CODE-coordinate + 64 DATA bytes; 7,388 compared bytes include 70 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. Unknown ownership remains
**121,743 bytes**, including MAIN 42,205. The global authored denominator and
percentage are unreviewed; the at-least-98% goal is not complete.
[Generated progress](PROGRESS.md) and [ownership](../resources/ownership.json)
are authoritative.

Latest exact recovery:the complete11-byte `pointnums_init()` in MAIN, with
no DATA, BSS, table or padding credit:

| Unit | Native load scope | Bytes | Receipt under `.analysis/unit-replays/` |
| --- | --- | ---: | --- |
| `main-pointnums-init` | `[E16E,E179)` | 11 | `main-pointnums-init-exact/receipt.json` |

The procedure ends at RET E178; native E179 is a separate EVEN NOP after ENDP,
outside the complete11-byte compiler contribution. It remains unknown and
uncredited, with no masking or padding copy. Two deterministic builds, valid
OMF, all raw bytes/ordered fixups and the compiled white-cursor mutation pass.
The canonical body is shared with the retained family, whose init/update
prototypes now preserve the published near Pascal interface. No old accepted
unit consumed that header. See [boundary/ABI review](../src/main/pointnum/init.md).

The previous24-byte ring fill remains accepted with its original fixup `[7]`;
see [source/ABI review](../src/main/math/randring_fill.md).

The previous three18-byte sound extension/mode banks remain accepted with54
initialized C DATA bytes. Their compact bank and cross-field mode3 read remain
unchanged; see [resource review](../src/shared/sound/load_resources.md).

The previous three MMD detectors remain accepted with141 instruction bytes.
The adjacent PMD candidate emits51 versus46; `register` and the C frontend
both leave DX allocation unchanged. The C trial also confirms the corrected
outside-only binder's original DS positions. See [resident review](../src/shared/sound/resident.md).

The previous shared `frame_delay` remains accepted in all three programs,
with63 instruction bytes and no padding credit. Its [ABI review](../src/shared/hardware/frame_delay.md)
records the genuine SS:SP+4 word transport and unsigned comparison.

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
| Staff updater (626) / renderer (861) | Current full-family output 623/858. Archived global `-Z-` MAP confirms630/879 without another build. Other declaration/API/expression trials fail; source restored. | [Staff family](../src/maine/staff/full.md) |
| Staff controller (991 bytes) | All raw bytes match; standalone fixups form one descending run instead of the original two. Bitmap predecessor (126) still compiles to 211. | [Controller](../src/maine/staff/controller.md) |
| Shinki wing (386) / ball updater (220) | Wing raw-equal with wrong order; ordinary scalar ball candidate 232. | [Wing/balls](../src/main/boss/shinki/wing_preparation.md) |
| B4 ball updater (273 bytes) | Natural 278; eager-delta 290 and cleanup-label 278 alternatives fail. | [B4](../src/main/boss/mai_yuki/b4ball_render.md) |

Generic boss collision (43) and Shinki particle renderer (159) also remain inexact.
The independent point-popup updater is reduced from126 to114 and then111
bytes with natural field assignment, signed countdown and byte/unsigned
comparison domains. Its size now agrees with the complete111-byte native
procedure body, but raw bytes/register allocation and merged tails differ.
It remains outside acceptance; see [updater](../src/main/pointnum/update.md).
The splash memset initializer still emits24 versus26 under one new `-G`
diagnostic. It grants no credit, and that same profile need not be repeated.
The newly routed spark updater `[E086,E0D2)` has a complete ordinary C++
candidate:72 versus76, with merged remove stores and a Y copy. A named Y plus
early-continue loop emits84; the72-byte source is restored, and its outside
binder alignment correction remains uncompiled. There is no new spark credit.
See [candidate and ABI evidence](../src/main/effects/spark/update.md).
A new standalone stage-switch defeat trial emits411 versus414, still merging
all-clear calls; its experimental source/binder were removed. A named-word
frame-loop counter emits451 versus445; baseline442 was restored. Shinki wing's
standalone `-v` emits384 CODE/four DATA and needs new float helpers, so it
cannot resolve the original386-byte order problem. All are failed diagnostics,
with unchanged accepted source and no credit; per-owner notes pin evidence.
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
The MAIN/OP/MAINE incremental plans are empty after the focused point-init
replay. No whole accepted-set replay was run. Update/Spark proposals stay private.

Handoff cleanup archived 24 terminal alternative producers plus duplicate
backups and unused assembler extraction. The two obsolete combined wrappers
and their binders were removed; semantic bodies and accepted owners remain.
See [local storage](LOCAL_STORAGE.md) for the archive, restoration commands and
the prior cleanup's 328-record/232-receipt inventory. Subsequent recoveries add
twenty-one records/twenty receipts; all accepted evidence stays live.
Retired zero-compare, boss-background and supplemental-negative tools remain
in Git at `3af324e`; they are not part of the active workflow.

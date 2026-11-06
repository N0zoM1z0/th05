# TH05 handoff

Read [workflow](RE_WORKFLOW.md) and [acceptance](ORACLES.md), then run
`git status --short` and `python3 scripts/preflight.py`. Continue recovering
both major boss functions and their leaves. Old failed attempts are evidence,
not proof that a different natural source context cannot work.

## Accepted state

353 bounded C/C++ CODE/DATA units, 536 complete function occurrences:
**104,410 authored bytes exact** = 88,811 CODE + 15,599 initialized DATA.
CODE is 88,003 instruction + 808 compiler-table bytes. Complete compared
extents total 104,498, including 88 uncredited padding bytes.

| Artifact | Functions | CODE | Initialized DATA |
| --- | ---: | ---: | ---: |
| MAIN | 413 | 67,489 | 3,317 |
| OP | 64 | 11,319 | 8,667 |
| MAINE | 58 | 9,681 | 3,615 |
| ZUN | 1 | 322 | 0 |

Separate reviewed ASM: 8,412 instruction + 210 dispatch-table + 24 semantic
CODE-coordinate + 64 DATA bytes; 8,799 compared bytes include 89 uncredited.
Vendor CODE/DATA: 73,804/3,777; font resource: 8,192. Unknown ownership remains
**120,198 bytes**, including MAIN 40,660. The global authored denominator and
percentage are unreviewed; the at-least-98% goal is not complete.
[Generated progress](PROGRESS.md) and [ownership](../resources/ownership.json)
are authoritative.

Latest recovery: the complete consecutive player-shot helper family MAIN
E38C..E40E (130): allocation56, angle velocity30 and power-level update44.
Two fresh ASM producers match full ordinary OMF/MAP, every raw byte and the
empty original fixup stream; their shared primary-sprite mutation is rejected.
Explicit adoption adds128 instruction bytes. The allocator's alignment NOP
and the actual HUD far-call relaxation NOP compare with zero credit. The
preincrement scan, hidden angle write through the point pointer and the real
near/Pascal/far interfaces remain intact. Pool, player, cursor, tables and
HUD provider are foreign; no accepted caller/header/table was changed. See
[source/ABI/receipt review](../src/main/player/shot_helpers.md) and
`.analysis/asm-replays/main-shot-helpers-c/receipt.json`. The original routing
distance74 after shot_velocity_set includes the independent44-byte level
updater; the velocity function itself is30. No C/C++ bytes or full EXE claim
is added, and no whole replay was run.

Previous recovery: both complete MAIN random-reader families, C700..C73E (62)
and 1529C..152D9 (61), pass two fresh ASM producers, raw bytes, empty ordered
fixups and their normal high-cursor-byte mutation. Explicit adoption adds118
instruction bytes; five NOPs compare with zero credit. The shared byte ring
and full WORD cursor remain foreign, including the index255 overlapping read.
Their near/Pascal stack interfaces are preserved without a BP frame. See
[family/ABI/receipts](../src/main/math/randring_readers.md). Final receipts:
`.analysis/asm-replays/main-randring-{1,2}-a/receipt.json`.
The two actual no-op callbacks at C73E/C740 are independently exact ordinary
C++ definitions, adding two complete functions and two instruction bytes;
their neighboring NOPs remain foreign. Both share one normal compiled return-
distance negative. See [callbacks](../src/main/runtime/null_callbacks.md) and
`.analysis/unit-replays/main-null-callbacks-a/receipt.json`. No other accepted
source was changed or recompiled, and no full replay was run.

Previous recovery: the complete MAIN scrolling strip copier BC6E..BD24 (182)
and dirty half-tile redraw BDAE..BE1A (108), separately reviewed handwritten
ASM. Both pass two fresh producers, full ordinary OMF/MAP, raw bytes and
original ordered fixups ([] / [103]), with rejected visible-column mutations.
There is no padding or new DATA/BSS. Strip height/scratch state, the complete
cache/flag arrays and real EGC providers remain foreign. The redraw stops at
BE1A; the following 32-byte C++ motion method is excluded. Source-language
inference uses the complete hardware/register protocols, independently of C++
failures. See [strip](../src/main/tile/scroll_strip.md) and
[redraw](../src/main/tile/redraw.md). Final receipts under `.analysis/`:
`asm-replays/main-tile-scroll-strip-a` and `asm-replays/main-tile-redraw-b`.
No unchanged accepted source was recompiled and no full replay was run.

Previous recovery: the complete 64-byte C section-offset table MAIN 218DA..2191A
and the independent tile-cache fill BB9E..BBEC (78) / full renderer BBEC..BC2E
(66). The table is generated as 32 section IDs times a 320-byte MAP section,
with its own compiled DATA mutation. Explicit ASM adoption credits 143
instruction bytes plus one compared, uncredited loop-alignment NOP. Each
kernel has two independently built objects, valid OMF/native frames and
original ordered fixups ([] / [61]), with rejected visible-column mutations.
The renderer's first valid object is reused after correcting only its MAP
public locator to TLINK's `tiles_render_all()` display spelling; no source,
ABI, generated object or fixup was changed. EGC setup/off providers, cache,
MAP/script inputs and sprites remain foreign. See
[source/ABI/receipt review](../src/main/tile/sections.md). Final receipts:
`unit-replays/main-tile-section-offsets-exact`, `asm-replays/main-tile-fill-a`
and `asm-replays/main-tile-render-b`, each under `.analysis/`.

The previous complete color tiny kernels MAIN BF62..C07C (32x32,
282 bytes) and C07C..C180 (16x16, 260 bytes) remain accepted. Two fresh final-source producers
per kernel reproduce all 542 raw bytes, native frames/publics and empty ordered
fixups; each phase-mask mutation is rejected. Explicit adoption adds 535 ASM
instruction bytes and seven compared, uncredited EVEN NOPs. The positive
Master ancestry is documented: these game adaptations have hybrid near
interfaces and caller-owned graphics state, rather than the unchanged library
entry. The 32x32 CS coordinate at BF60..BF62 remains foreign and unknown;
handles, sprites, C++ callers and the accepted monochrome kernel are unchanged.
See [native/source/receipt review](../src/shared/graphics/tiny.md).
Final receipts: `.analysis/asm-replays/main-tiny32-b/receipt.json` and
`main-tiny16-a/receipt.json`. The earlier 32x32 packet predates a corrected
comment only and is not adopted; no failed source producer is claimed.

Latest C++ recovery: complete 68-byte `map_load()` MAIN E5C2..E606, with
original ordered fixup `[41]`, no padding or DATA/BSS. The TH04 MAP format and
flow remain canonical; TH05 uses direct DOS transfers and frees the old
segment first. The initial 70-byte diagnostic reloaded the stored segment;
consuming the allocator's still-live actual AX return restores the original
68 bytes without changing its complete segment-pointer ABI. Two deterministic
builds, valid OMF/native CS/DS placement, all bytes/fixups and the compiled
filename mutation pass. The accepted adjacent release is unchanged. See
[source/ABI review](../src/main/formats/map_load.md) and
`.analysis/unit-replays/main-map-load-exact/receipt.json`.

The previous complete 182-byte Cheeto mask kernel MAIN DE72..DF28 is
separately adopted as 178 reviewed ASM instruction bytes plus four compared,
uncredited EVEN NOPs. Two fresh producers reproduce all raw bytes, valid OMF,
native frames/publics and original empty ordered fixups; the 31-row mutation
is rejected. Private CH/ZF row-worker and packed register protocols support
the handwritten-ASM inference. TH04/ReC98 and three pinned primary Master
sources inform the review without proving literal historical source or
excluding adaptation. The 2048-byte bank, adjacent loader/scroll provider and
already accepted C++ caller receive no extra credit. See
[source/ABI/receipt review](../src/main/bullet/cheeto_put.md).
Receipt: `.analysis/asm-replays/main-cheeto-put-a/receipt.json`.

The previous complete 11-byte `pointnums_init()` remains accepted in MAIN, with
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
| B4 ball updater (273 bytes) | Natural 278; eager-delta 290 and cleanup-label 278 fail. New jump-optimization-off profile emits274 with different first branch, Y lowering and loop tail; baseline restored. | [B4](../src/main/boss/mai_yuki/b4ball_update.md) |

Generic boss collision (43) and Shinki particle renderer (159) also remain inexact.
Two new scalar C++ candidates stay outside all live manifests. Near vector
has a complete 55-byte procedure plus a separate unknown EVEN NOP; narrowing
samples/results and reusing a real table offset reduces 106 to 92, still inexact.
No ASM ownership is inferred from its 32-bit native arithmetic. Scroll-coordinate
conversion emits 47 versus 40 due to DX allocation; an inline form emits 51 and
was reverted. Its corrected empty foreign SEGDEF context is verified by
relinking the saved 47-byte object, without another compiler invocation.
See [vector](../src/shared/math/vector2_near.md) and
[scroll ABI/diagnostics](../src/main/scroll/coordinates.md). No new credit.
A read-only Staff OMF review confirms one 991-byte controller CODE record;
the existing full family uses roughly 1-KiB chunks. This supports a context
explanation for the original two fixup runs without proving its TU or allowing
an artificial prefix. A new segment-qualified bitmap capture reduces its
69-byte output to 58 versus native 43; ordinary pointer register hints also
emit 58 and were reverted. No controller or restore was recompiled, no new
exact credit is claimed, and the candidate stays outside live manifests.
See [capture and ABI evidence](../src/maine/staff/bitmap.md).
The newly prepared OP score decoder has a complete 169-byte native boundary.
Ordinary C++ with a named byte-rotate primitive emits 181; a register byte key
emits 182. The 181-byte source is restored, outside all live manifests, and
neither trial grants credit. The two extra key store/load pairs across the
rotation explain the first 12-byte gap. No fixed-AL algorithm was introduced;
see [decoder evidence](../src/shared/score/decode.md).
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
One new ordinary gather-template assignment emits a valid 27-byte object,
matching the native helper's size but using stack-passed far pointers and
F_SCOPY@ instead of the inline seven-WORD copy. The link stops at that real
unresolved provider; no placeholder, second producer or negative was added.
The source stays outside live manifests and grants no credit. See
[copy diagnostic](../src/main/gather/copy.md).
The random raw-reader C++ candidate emits21 bytes with a natural local,
15 with a register local, and19 with prefix increment, versus13 native bytes.
The compact15 source remains outside manifests; ASM origin is reviewed
independently of those failures. EMS compiler `-S` plus unmodified TASM output
remains684 raw-equal but emits ascending fixups, so it cannot accept the boss
preload. ZUN main's nine-byte gap is three merged message calls; a targeted
`-O-` source profile emits262 versus269, and the260 baseline is restored.
Per-owner notes retain all three findings; do not repeat these same trials.
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
The MAIN/OP/MAINE incremental plans remain empty after the focused tile
replay. No whole accepted-set replay was run. Update/Spark proposals stay private.

Handoff cleanup archived 24 terminal alternative producers plus duplicate
backups and unused assembler extraction. The two obsolete combined wrappers
and their binders were removed; semantic bodies and accepted owners remain.
See [local storage](LOCAL_STORAGE.md) for the archive, restoration commands and
the prior cleanup's 328-record/232-receipt inventory. Subsequent recoveries add
twenty-three C/C++ records/twenty-two receipts, one Cheeto ASM receipt, two
adopted tiny ASM receipts and two tile ASM receipts; all accepted evidence stays live.
Retired zero-compare, boss-background and supplemental-negative tools remain
in Git at `3af324e`; they are not part of the active workflow.

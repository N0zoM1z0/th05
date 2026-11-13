# Shinki wing preparation and ball-update evidence

The complete wing transition MAIN1ADDE..1AF60 is accepted from maintained
C++ through the explicit `tcc-s-tasm32` compiler recipe. All386 instruction
bytes and the original ordered MZ fixups `[76,305]` match. There is no table,
padding, initialized DATA or BSS. Canonical Boss, Laser, templates, palettes,
geometry, return type and foreign interfaces remain unchanged. The C++
algorithm and headers did not need instruction, type or behavior changes.

## Compiler recipe and acceptance

The former direct TCC object matches every raw byte but emits `[305,76]`.
The new recipe compiles the same C++ with `-S`, then assembles the unmodified
compiler output with the pinned TASM32 and links the normal symbol-only
binder. Its natural object fixup stream yields `[76,305]`; no instruction,
object record, relocation list or linker output is edited or sorted. This is
C++ recovery, with no new handwritten-ASM ownership claim. The historical
producer and literal historical source remain unknown.

TCC emits GROUP members for foreign first-declaration contexts without
emitting all corresponding empty SEGDEFs in its assembly text. The consumer
wrapper supplies only those absent CODE declarations, checked against the
real binder's classes and groups, then includes the compiler file verbatim.
It supplies no executable instruction, initialized data or artificial stack.
Actual MAP readback retains CS15270, DS209D0 and main_03. Complete ordinary
OMF/LEDATA ownership excludes every other nonempty source segment.

Both fresh producers preserve the compiler-generated assembly hash before
and after TASM and reproduce the same assembly text, normalized OMF, MAP and
whole comparison MZ. Input mtimes are fixed build metadata; compared bytes
and ordered fixups are never normalized. TCC's actual E9 dependency records,
C++ wrapper, consumed source/header bytes, binder, recipe code, toolchain
execution proof and actual compiler/assembler/linker commands are frozen.
Saved-receipt import independently reads those artifacts and rejects changed
compiler text, context, command, object, linked code or aliased producer paths.
The default direct-object recipe and existing acceptance remain unchanged.

The normal shared source negative changes shake duration8 to9. It changes
only byte311, keeps the complete386-byte extent and ordered fixups, and is
rejected. No additional game behavior model or per-function test is added.
Only the new pipeline's focused tooling checks and existing incremental
replay tests run; no full CI or accepted-set cold replay is required.

## Affected replay after adding decoded artifact contexts

The recipe now supports explicit OP/MAINE binary and decoded-target proofs.
Its source identity therefore changed for this accepted wing owner. Only this
accepted owner was replayed: two fresh unchanged C++ chains still match all386
bytes and `[76,305]`, with the same shake-duration negative rejected.
The replacement adopted receipt is
`.analysis/unit-replays/main-shinki-wing-artifact-context-c/receipt.json`,
SHA-256 `cf074f3e7ad481533070945dc10777f56576091105fd4fc5f6d32000d1ae7655`.
Coverage stays386 bytes;
this receipt replacement adds no function or authored byte.

## Earlier inexact ball-update producers (superseded)

The original ball update1AACF..1ABAB is220 instruction bytes, no NOPs, table
or MZ fixups. An older register-backed candidate emits216, merging two jumps;
its bounded jump-optimization-off diagnostic emits224. Neither is an owner.
The ordinary scalar candidate in balls_update.cpp limits register reads to
the genuine DX:AX Point return, borrows it for clipping and unpacks at the
collision consumer. Immediate and later unpacking both emit232, using a
stack delta and longer conditional branches. No failed compiler body is
promoted to ASM. These observations do not require repeated builds.

The existing full-pool semantic evidence remains reference, not an additional
acceptance gate: `.analysis/shinki-balls-semantic-model.json`, SHA-256
`ea2bd3684eda5abb2a63ac9e9e8796c3317a7a02915e9e1dc843a9ebc8a54b53`.
Earlier native/source/actual review: `.analysis/shinki-wing-balls-root-review.json`,
SHA-256 `273fdda668ee1168da244a77f903094842d335cf183f3007af8a1ff90e28c39d`.
Only the separate wing function gains386 C++ bytes and one complete function.

## 2026-11-10 220-byte ball controller codegen investigation

A new bounded first-producer series confirms optimized natural `b6balls_update`
216 bytes and no-optimization source 224 bytes versus the native complete
220. The best ordinary `-O-` branch control encloses the active ball body in
`if(p->flag != B6BF_FREE)` and reverses the cloud transition predicate, without
changing the full canonical Ball/Motion/return types. It emits **221 bytes**, no
fixups, versus native 220. Target and candidate have identical algorithmic
collision/decay instruction shapes and return semantics, but at target relative
`+23` the native four-byte near `JGE` becomes the producer's two-byte short
`JL` plus a three-byte `JMP` to the loop tail, leaving one extra byte. Native
DATA offsets then drift due the failed contribution size. Twelve additional
branch/goto and scoped option variants stay at 221 or 223; none is exact.

These early 221-byte/branch-profile trial outputs were pruned for storage
on 2026-11-11. Their codegen observations remain historical and inexact; **not** changes to accepted C++ or new source credit. The
current maintained scalar candidate, all other Shinki accepted functions and
the existing vendor and hardware interfaces remain unchanged. A future owner
must match the full 220-byte function and ordered relocations without compiler
padding or instruction surgery.

## 2026-11-10 additional ball-update codegen trials

The complete native 220-byte Shinki ball updater remains a hard C++ lowering
gap. Sixteen real noopt/register/speed/jump-profile variations on the
221-byte cloud-branch candidate emitted 216, 220, 221, 222 or 224 bytes.
The one 220-byte form changed the real forward traversal into a countdown,
which is not a valid general semantics-preserving replacement; its compiled
raw bytes also fail. The other variants never reproduced the native
long conditional branch at relative `+23`. No accepted Boss unit or target was modified by those failed experiments.
Their one-producer private build directories were pruned for storage; see the
later accepted original-ball and wing results in this note.

## 2026-11-10 real preceding add/update compilation context

A fresh single native producer also compiled the full real `b6balls_add()`
source in its original MAIN03 translation unit directly before the natural
ball updater. The accepted allocator retains its true 81-byte start at
`1AA7E`; the updater then starts at the exact native `1AACF`, but the real
compiled complete updater remains **221 bytes versus native 220**, with no
relocations and the same cloud-state short-JL/near-JMP one-byte lowering
difference. Thus the real preceding function/source context does not fix that
specific compiler branch choice. The untouched first producer and every source
input are frozen at `.analysis/gpt-web-shinki-b6-real-context-a/`; source and
linker controls did not supply an interior function byte. The experimental
standalone file was removed after confirming it was byte-identical to that
frozen input. The accepted 81-byte add and all following Shinki callbacks are
unchanged, no new Boss byte is credited and no full cold replay was run.

## 2026-11-10: exact native 220-byte ball update from genuine C++

**`b6balls_update()` is now accepted as a complete original 220-byte
source-owned C++ function at `[1AACF,1ABAB)`.** The authentic source
`_reference/ReC98/th05/main/bullet/b6ball.cpp` includes two calls to
`optimization_barrier()`, a genuine empty inlined false-returning function
from the same pinned ReC98 `decomp.hpp`. Earlier candidates omitted them on
the assumption that they were unnecessary. In reality those two source calls
prevent Turbo C++'s jump threading from shortening four bytes of clipping and
collision branches. Enabling its normal jump optimization simultaneously
preserves the native **four-byte near JGE** out of the cloud state. The
original scalar ball fields, real DX:AX motion return, C++ state machine,
unmodified pointer geometry and near-callback ABI are unchanged. Neither
barrier generates its own runtime instructions, branch operands or NOP bytes;
no physical-register assembly or target-byte emission is introduced.

The maintained body now has one canonical implementation in
`balls_update_body.inl`, included by both `shinki.cpp` and the standalone
`balls_update.cpp` wrapper. The old four-byte outside-function binder gap
that separated natural 81+216 from original 81+220 is **removed**, not
credited. The real combined `B6_BALLS_TEXT` is now **301/301 raw bytes**
(81 adder, 220 updater), and its following genuine 271-byte pattern cohort
stays at `1ABAB` with unchanged ordered fixups. The original `main_03` frame
is `1527` and DS remains `209D` under the source-free binder.

The new unit `main-shinki-balls-update` passed two independent Turbo C++/TLINK
builds, literal raw comparison 220/220, empty native ordered relocation
stream, complete OMF/MAP boundaries and its own compiled real motion-age
negative (`p->age++` to `+=2`), which was rejected. Receipt:
`.analysis/unit-replays/gpt-web-main-shinki-balls-update-220-20261110/receipt.json`.
Nine previously accepted same-translation-unit Shinki units were locally
refreshed after the source and binder changes; all retain their exact native
code, original ordered fixups and compiled negative results in
`.analysis/unit-replays/gpt-web-main-shinki-b6-neighbor-refresh-20261110/receipt.json`.
Only **220 new C++ instruction bytes** are credited; accepted adjacent
functions are not counted again. The earlier 216/221/224-byte experiments in
this document remain useful historical evidence, not unresolved blockers.

## Six-beam wing opening and 50-shot burst geometry (2026-11-12)

The original **386-byte** `pattern_wing_preparation()` now uses the
compile-time-only `wing_preparation_rules.hpp` to identify the actual
six-beam wing opening. The six real laser slots are emitted in order
with directions **0x50, 0x48, 0x40, 0x40, 0x38, 0x30** at the 16th
Boss phase frame. The two middle beams intentionally share 0x40; no
array, synthetic loop, or lookup data was inserted to hide that order.
The initial palette tone is 100, the cast sound is 8, and the original
state overlays remain `boss_statebyte[14]` for tone and `[15]` for the
post-sweep wing frame.

On alternating global frames the outer three beam angles increase and
the opposite three decrease by one byte unit, while the current tone
increases through the original direct byte `tone++`. This phase ends
when center laser 2 reaches **0x80**. Only then does the actual
source generate its fixed **50** blue bullets, with angular range
`[0x10,0x70)` and speeds **1.5–5.5 pixels/frame**, before growing the
six existing lasers. The original first wing sprite, sound 15, and
8-frame screen shake are preserved. During the next eight wing frames,
tone alternates 100/150; at expiry all six lasers are stopped before
the callback returns `true` to the complete Shinki controller.

The 386-byte standalone function and its real 10-unit Shinki
translation-unit mirror were edited together. The standalone is
reconstructed by the already accepted **natural TCC -S → TASM32**
source pipeline, which reproduces its original two ordered relocations.
Both compiler rounds match every one of the 386 source bytes; the
compiled screen-shake mutation from eight to nine is rejected:
`.analysis/unit-replays/gpt-web-shinki-wing-milestones-b/receipt.json`.
The independent ten-unit same-TU replay at
`.analysis/unit-replays/gpt-web-shinki-wing-milestones-cohort-a/receipt.json`
confirms all other affected Shinki functions' complete raw bytes,
OMF/MAP placements and fixups. No new runtime fields, optimizer barriers,
inline instructions, binary assets or duplicate accepted CODE credit are
introduced. This is not a full game cold replay.

## Original six-slot wing beam ownership and large Boss phase reset (2026-11-12)

The source-visible six-beam preparation now names **six distinct real laser
slots** in the same original spawn, per-frame angle-update, grow, and final
stop order: right outer/inner/center = 0/1/2 and left center/inner/outer
= 3/4/5. The sweep-completion comparison deliberately inspects the
right-center laser **slot 2**, not an averaged or synthetic angle. During
the animation, the source retains the original byte-wide `+= 0x01` and
`-= 0x01` operations, which produce the correct Borland writeback forms;
only the slot selectors now use explicit compile-time role names.
The first wing animation frame remains byte zero in the canonical
scratch field, and the original six-slot source includes no newly
allocated arrays or extraneous laser state.

The two independent source copies (`wing_preparation.cpp` and its
historically adjacent body inside `shinki.cpp`) are now verified with
one consistent six-slot protocol. The entire **386-byte** standalone
wing pattern still compiles via its required genuine
**TCC `-S` → TASM32** route, including complete raw byte equality, true
ordered relocations and the compiled screen-shake control rejected:
`.analysis/unit-replays/gpt-web-shinki-wing-named-six-slots-a/receipt.json`.

The complete **959-byte** original Shinki Boss controller now also uses
the explicit same first-wing pattern index for the post-white-wing
and post-purple-wing transitions. These are independent real Boss
wave counters; the existing 3,000-frame timeout and 16-bit enum width
are unchanged. All **eleven** affected `shinki.cpp` / updater CODE
scopes, including the original compiler switch table, checked padding
and literal ordered relocations, match under two native Borland rounds:
`.analysis/unit-replays/gpt-web-shinki-six-slot-boss-cohort-a/receipt.json`.
No prior accepted CODE byte is credited twice and no whole executable
cold replay is involved.

The tone and animation frame are now explicit members of the shared
`ShinkiSpiralOrDevilInnerAngle` / `ShinkiSpiralOrDevilOuterAngle` byte views at
physical offsets 14/15. The standalone wing source and the duplicate callback
inside `shinki.cpp` use the same `ShinkiWingPreparationScratch` view; the
complete phase-role map is in [scratch-byte lifetimes](scratch.md). This is a
source naming/layout refinement only: the existing 386-byte TCC-S/TASM32
acceptance remains exact and receives no duplicate CODE credit.


## 2026-11-14: Yumeko-to-Shinki laser-template width handoff

The six wing-preparation lasers intentionally do **not** initialize
`laser_template.coords.width`. The original Stage 5/6 setup order explains the
state lifetime: `stage5_setup()` installs `yumeko_update`, `stage6_setup()`
installs `shinki_update`, and both call `boss_reset()`. That helper resets the
Boss phase/mode/clock and explosions, but does not touch `laser_template`.
There is no laser-template reset in the Stage 6 setup either.

In Yumeko, the second approach installs `yumeko_pattern_laser_swords`; the
second stationary phase calls it, and its frame-16 charge writes
`laser_template.coords.width.nonshrink = YLS_LASER_WIDTH`, where the exact
value is **6**. The later sword sweep, final approach and final ring do not
rewrite the template width. Shinki's controller updates only the laser origin
before the wing callback. At its frame-16 startup, the six calls to
`laser_manual_fixed_spawn()` copy the inherited template width into each
laser's `grow_to_width` while starting current width at 1.

This is gameplay-significant, not merely stale scratch: the global loop runs
`lasers_update()` before `boss_update()`. Once the wing sweep finishes,
`laser_manual_grow()` starts the eight-frame visible window. Fixed lasers gain
2 pixels on odd ages, become `LF_FIXED_ACTIVE` when their width reaches the
copied target, and only hit-test on a later update. Modeling both possible age
parities across those eight updates gives width 6 **two or three active hit
updates**, while width 8 gives **zero or one**. The inherited value 6 therefore
leaves actual collision time before the wing callback stops the lasers; the
commented-out local assignment would mask the real inter-stage protocol.

`tests/test_shinki_yumeko_laser_handoff.py` pins the Stage 5/6 callback order,
Yumeko's phase-7 width write, absence of a Stage 6 reset, the manual-spawn copy,
and both age-parity growth schedules. The accepted 386-byte wing callback is
replayed locally after the comment-only source clarification; no CODE bytes or
new storage are claimed.

# Stage-three midboss update candidate

The original stage-setup far callback at load146D1 identifies MAIN
**1527:6A92**, load **1BD02..1BE4E**, **332 bytes / one complete function**.
Native decoding establishes98 instructions covering323 bytes through both
RETF paths, one real compiler zero at offset323, and a four-word switch table
at offset324. All14 direct local branch destinations and all four indirect
switch destinations are instruction starts. The next original function begins
at1BE4E; its body is external. Original ordered relative MZ fixups are **[280]**.
Classification is331 authored-code bytes, including8 compiler-table bytes and
323 instruction bytes; the zero receives no credit. The accepted result is recorded below.

ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` still retains the function as
`@midboss3_update$qv` in `th05_main.asm`. This source recovers the phase and
pattern algorithm in ordinary C++ using the full canonical22-byte midboss,
14-byte bullet template,14-byte gather template and real point/motion types.
It contains no instruction transcriptions, pseudo-register loops, opaque
target-derived data or fake helper bodies. No maintained shared interface was
modified. Ordinary `-a2` is applied only after those complete ABI declarations:
the original word table has a real even boundary and preceding compiler zero.
The compiler must still produce and verify that complete extent naturally.

Every frame publishes the current midboss position to the bullet and gather
templates. Phase0 performs real movement and invulnerable shot handling until
192 frames, then resets the phase timer, angle and orbit state and initializes
pattern1 and completed-pattern count1. Phase1 copies current position to the
previous position and dispatches its real pattern state. State0 waits32 frames,
chooses `(patterns_done % 3) + 1`, increments the byte counter and resets the
phase timer. Once the counter reaches13 it goes directly to the shared defeat
transition, without HP rewards. The three actual pattern helpers remain
foreign no-argument near functions.

Damage is processed only while sprite<212, with the real returned damage byte
stored before subtraction from signed HP. Surviving HP exits that case. HP
defeat activates the real bullet zap, grants15 bonus units and creates the
actual1UP item; the timeout route skips those actions. Both enter phase254,
sprite4, zero the timer, emit48 circle sparks at8 pixels and play SE12. Default
phases call the real defeat updater and render HP before returning; live
phases also publish the homing point. The shared `explode` label represents
this actual gameplay transition across the nested switch, not an artificial
compiler barrier. Total HP is1400.

Foreign interfaces retain their real1527 near frame:

| Interface | Original load destination |
| --- | --- |
| `PlayfieldMotion::update_seg3()` | 1527C |
| circle sparks | 16EE8 |
| three stage-specific pattern helpers | 1BB41 / 1BBD8 / 1BC77 |
| HP render / score bonus / defeat updater | 1C4F6 / 1C54E / 1C628 |
| item addition / shot damage | 1CC2B / 1FA90 |

The sound interface is genuine C Pascal far14AB:0232. Its uppercase Pascal
public and the full uppercase sparks mangling are anchored exactly; helper
bodies remain external. The binder places only address labels and outside
contribution gaps, preserving the full compiler source slot and real DS209D.
A separate PARA context begins at1BE50 for the original complete end1BE4E;
no compiler table, zero or instruction is supplied by that context. Every ORG
is smaller than64KiB, and there is no `.stack` or initialized context value.

Foreign globals are homing_target DS3F8A(4), bullet_zap3F96(1),
bullet_template577E(14), midboss5AA4(22), gather_template9EA6(14), and
boss_statebyteC682(16). State bytes13/14/15 remain members of the complete
canonical Boss state array. No DATA or BSS is defined by this owner.

`.analysis/midboss-stage3-boundary-review.json` pins the original target and
extent hashes and records complete branch/call/table/global evidence.
`.analysis/midboss-stage3-candidate.json` proposes one complete-contribution
entry, module `th05/midboss3.cpp`, B4_UPDATE_TEXT/main_03, and its meaningful
compiled negative changing only entrance duration192→193. Native source-closure
and classification checks pass. Preparation invoked no compiler or Wine;
two actual cold producers, full raw/ordered comparison and rejected compiled
negative remain required before any authored credit.


## Accepted complete callback

`main-midboss-stage3-a/receipt.json` passes both independent cold producers for
the complete332-byte contribution. Every raw byte, including the generated
zero and all eight compiler-table bytes, agrees with the original; both rounds
also preserve the original ordered loader fixup list[280]. The separately
compiled entrance-duration negative192→193 changes actual code bytes and is
rejected. The ledger accepts `main-midboss-stage3-update`: one full callback,
331 authored-code bytes comprising323 instruction bytes and8 compiler-table
bytes. The one compiler zero is excluded from credit; DATA/BSS remains zero.
No source variant, target bytes, fixup normalization or inside-function scaffold
was introduced. CPP, ABI header and binder remained frozen during replay.

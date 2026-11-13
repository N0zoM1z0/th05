# Complete shared Mai/Yuki update: accepted final-pattern context

MAIN `[17FDB,183D5)` is one complete 1,018-byte far Pascal callback:
993 instruction bytes, one checked zero at relative 993, and two compiler
switch tables totaling 24 bytes at relative 994. Native review rereads all
282 instructions, complete returns, direct branches and the six case values
and destinations. The values are 0/1/2/253/254/255. No instruction NOP exists.
Original ordered MZ fixups are `[942,931,915,898,874,723,312,171,123]`.

The standalone source's earlier 1,017-byte failure remains archived.
`update_context.cpp` retains its callback body byte-for-byte, preceded by the
ten genuine adjacent final-pattern bodies from the unchanged canonical
`remaining_patterns.inl`. Those 939 bytes were already accepted separately.
The resulting complete compiler contribution is `[17C30,183D5)`, 1,957 bytes.
It naturally emits the original zero and keeps all nine updater segment
fixups inside its second LEDATA record. This establishes an exact maintained
source context; the literal historical translation-unit boundary is unproved.

The updater preserves both Boss objects, shared homing and movement, pattern
selection, HP gates, damage/timeout defeat selection, explosion and shake
phases, survivor dialog/BGM loading and the actual far survivor-update
pointers. Canonical Boss24, Laser24, custom26, gather14, bullet and dialog
types and the near callback arrays remain unchanged. Storage, assets and
foreign implementations receive no credit. The first real MAIN01 callback
declarations still precede transitively included stage declarations.

The symbol-only binder retains MAIN03=1527, MAIN01=AE1, SHARED=14AB and
DS=209D. Even empty foreign compiler segments stay in their real groups.
Every hole lies outside the entire 1,957-byte source contribution; the
independent paragraph tail begins at 183E0. There is no emitted helper code,
inside hole, initialized storage, stack, source padding, opcode body or
supplied switch-table payload.

Both fresh producers emit ordinary CRC-valid OMF with LEDATA ranges
0..1020 and 1020..1957. Their normalized object identities, whole scaffold
MZ files and MAPs agree. The entire contribution also matches native raw
CODE, but only the complete updater receives new acceptance. Its raw hash
is `501bb630b4a814971feaa87dc117aa86c9f2c3acc151ac62c2b30786f26d5384`.
The own compiled negative changes the combined-HP gate 5500 to 5501,
differs only at relative 509 and is rejected with extent, zero, tables and
ordered fixups unchanged. Actual source snapshots, compiler arguments,
link response, logs, OMF and MAP/frame evidence were reread before import.

Receipt `.analysis/unit-replays/main-mai-yuki-update-context-a/receipt.json`,
SHA-256 `7266d6778d95b7448f1be6fe8d9cb4cbc545967b443d086868fe8523080b4b14`.
Native review `.analysis/mai-yuki-update-context-native-review.json`;
actual producer/source review `.analysis/mai-yuki-update-context-root-review.json`,
SHA-256 `0c7abe509a8a9e26a85b602028a1e1e59ce5f0be4f33a9484b84db8caf9f424b`.

New credit is one complete function and 1,017 authored CODE bytes:
993 instructions plus 24 compiler-table bytes. The zero gets none and the
939-byte prefix is not counted twice. All earlier accepted records, source,
headers and controls stay unchanged; installed execution probes and accepted
objects were reused after dependency checks. No DATA, ASM, packed-container
or whole-game equality is claimed.

## Exact defeat-identity protocol in both maintained controller sources

The real `mai_yuki_hittest_shots()` returns 0/1/2 for no defeat / Mai defeated /
Yuki defeated, as independently corroborated by the accepted `hittest.cpp`.
The complete Boss controller stores a nonzero result **minus one** in
`boss2.phase_state.patterns_seen` for the explosion and survivor-dialogue
stages. Thus the value zero means Mai was defeated and Yuki survives; value
one means Yuki was defeated and Mai survives. Pattern-cycle exhaustion
selects Mai's defeat with hit code one. Four later checks now use the
explicit `MY_DEFEATED_MAI` constant, making the original scratch-value
conversion visible instead of pretending it is still a normal pattern count.

Both `update.cpp` and the actually accepted, adjacent-final-pattern
`update_context.cpp` now use the same source-level hit/defeat constants; these
constants are private to the two controller bodies and do not add dependencies
to the shared public Boss header. The **1,018-byte** complete accepted updater
was recompiled by two independent targeted Borland producers with every
original raw byte, switch table, alignment byte, and ordered relocation equal.
Its compiled HP-gate semantic negative was rejected. Actual receipt:
`.analysis/unit-replays/gpt-web-mai-yuki-defeat-codes-real-context-20261111/receipt.json`.
There is no new authored-byte credit or change in the hit helper's ABI.

## Paired-Boss explosion and survivor transition semantics (2026-11-12)

The 1,018-byte `mai_yuki_update()` controller now names the fight's real
explosion/survivor transition effects in `transition_effects.hpp`. In the
shared fight's setup, gather still uses its two-step angle and eight points.
At each HP gate, the clear-warning sound is 15 and both Bosses' small
explosions still use the diagonal `ET_SW_NE` direction; the defeated
character's later explosion uses `ET_VERTICAL`. These two `ET_*`
constants preserve the existing original enum values and the real
near-Pascal unsigned-argument ABI of `boss2_explode_small()`.

At the end of the first explosion, whichever Boss was defeated receives
sprite 4, the other keeps the original idle sprite, and the sound 12 and
255-frame player invincibility are unchanged. The following animation
still shakes the playfield by exactly four pixels: negative X on even
frame-mod-2 ticks and negative Y through mod-4 values 0 and 1. Its
slowdown factor remains two, while the 8-frame sprite advance and
64-frame transition thresholds retain their previous named clocks.
The survivor's original handoff resets Boss phase to zero, replacing the
shared update callback with the correct Mai/Yuki solo controller.

No new state, helper calls, guards, ABI views, optimizer barriers or
placeholder instructions were introduced. The standalone `update.cpp`
and actual accepted `update_context.cpp` retain identical callback bodies.
The focused native replay at
`.analysis/unit-replays/gpt-web-mai-yuki-transition-effects-b/receipt.json`
passed two independent compiler producers across all **1,018** original
callback bytes, one checked alignment zero, 24 bytes of real compiler
switch tables and the nine original ordered relocation sites. The
existing compiled 5,500-HP gate mutation was rejected. Other accepted
units were not replayed and the already accepted CODE earns no duplicate
credit from this semantic source improvement.

## Coupled defeat index with the real 111-byte collision leaf (2026-11-12)

The full Mai/Yuki shared Boss updater now includes the same canonical
`hit_result.hpp` declaration as its actual `mai_yuki_hittest_shots()`
callee. This unifies the returned `0 = no hit`, `1 = Mai loses`,
`2 = Yuki loses` protocol and the original subtraction-of-one when
transferring the outcome into the existing `boss2.phase_state.patterns_seen`
byte. That byte is a *loser index* during the explosion and survivor
handoff phases, **not** a new pattern counter allocated by this source.
The shared Boss' stage exhaustion still explicitly selects Mai as the
loser so Yuki survives; no return values or rendering/callback swaps
are inferred or rewritten.

The full `update_context.cpp` and the independent `update.cpp` mirror
retain identical Boss function bodies. The companion hittest C++ source
also uses named 24-pixel Yuki combat radius and real hit sound 4.
A bounded real native replay of both accepted units passed their full
**1,018** + **111** source bytes, the controller's checked one-byte
alignment and 24-byte compiler switch table, all original ordered MZ
relocations and both compiled negatives:
`.analysis/unit-replays/gpt-web-mai-yuki-shared-hit-protocol-a/receipt.json`.
Previously accepted compiled code is not double-counted, and no
all-game cold replay was executed.

## 2026-11-12: shared paired-hit tests and HP-gated reposition cycles

The maintained complete `mai_yuki_update()` now uses the explicit
`MY_INVINCIBLE_PAIR_HITTEST()` rule for **both** native setup and ready
phases. The macro preserves the original shot-Boss invincibility call,
Yuki's separate 24-pixel hitbox test, real hit sound, exact call ordering
and no extraneous early return. Both HP crossing thresholds in the
shared combat phase use `MY_ENTER_REPOSITION_GATE()` to set mode, phase
clock and the chosen pattern-gate index as one atomic source-level rule.
The first and second thresholds remain separate and in the original
priority order; only the repeated genuine C++ state assignments were
factored, with no new buffer, branch, or artificial compiler barrier.

The strict, *single-unit* `main-mai-yuki-update-context` replay at
`.analysis/unit-replays/gpt-web-mai-yuki-gates-hittest-source-a/receipt.json`
compiled two independent native Turbo C++/TLINK positives. Each still
reproduces the full **1,018 original bytes** of the far Pascal Boss
controller and all original ordered relocations, and the original
compiled negative is rejected. The shared patterns preceding this
function remain a real compiler context but do not receive a second
source-credit claim. This is a refinement to an existing major Boss CODE
owner, not newly counted bytes, and no full cold replay was performed.

## Shared paired and solo scratch overlay

The paired reversing-ring pair and later Mai/Yuki survivor patterns reuse the same physical Boss scratch bytes. Their complete offset-12..15 and byte-15 lifetime map is documented in [the shared scratch review](solo_scratch.md). The source now names both ring angle/step pairs and all five byte-15 roles without changing any original initializer, turn gate or transition reset. Ten affected complete units passed the focused two-producer replay; the 1,018-byte controller and its 939-byte adjacent pattern context remain exact, with no duplicate CODE credit.

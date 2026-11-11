# Alice update candidate

The complete candidate covers original MAIN `1E957..1ED41`: the genuine
63-byte final spread followed by Alice's full939-byte far callback. The
callback contains908 instruction bytes, one zero alignment byte and a
30-byte compiler switch table after its final RETF. Together the two
functions contain971 instruction bytes and253 instructions. The original
ordered relocation offsets are `[196,59]`.

The spread configures a periodic13-way red fan. The callback handles entrance,
HP thresholds, random movement, puppet initialization, pattern selection,
beam windows and defeat. Shared state and callback tables remain foreign
semantic objects. No asset payload, pointer-table entries, target instruction
arrays or artificial helper bodies are supplied.

The frozen beam header supplies the full26-byte Puppet and canonical Boss,
motion, bullet and player types. The frozen gather header supplies its real
14-byte template. The actual puppet dispatcher pushes a near puppet reference
and consumes AL; all four callbacks load that argument and return RET2.
Their declarations therefore use real near Pascal reference-taking bool
functions. The separate main-pattern callbacks are near cdecl void functions.
The existing4-by3 pattern table stores24 bytes of near function pointers.

All near MAIN03 calls use frame1527; sound is far Pascal14AB:0232 and the
background callback belongs to main01/AE1. Its first declaration preserves
that context before the common stage header. DS is209D. The binder places
only foreign symbols and outside-contribution layout holes. It defines no
instructions, initialized data, stack, or hole within the1002-byte candidate.
The genuine odd-sized prefix and real `-a2` option after canonical types
retain the reviewed source context without changing accepted layouts.

ReC98 `th05_main.asm` lines12019..12355 supplies the semantic reference.
Cached calibration has identical complete instruction shapes at1A005 and
1A044; it provides routing evidence only. Original complete return boundaries,
direct branch destinations, all15 table destinations and ordered fixups were
checked natively. Source acceptance still requires the focused exact oracle.

Private integration metadata is
`.analysis/alice-update-boundary-review.json`, including the proposed whole
unit and a unique staged mutation of the real initial HP threshold7400 to7300.
No compiler, emulator or Ghidra was run during this preparation.

The saved whole-owner oracle `main-alice-update-a` emitted 1001 bytes against
the original 1002. The 63-byte prefix is exact, but the full callback lacks
the original zero immediately before its 30-byte switch table. The table
words and callback instructions otherwise agree up to shifted addresses.
Both functions are in one real nonempty SEGDEF/LEDATA contribution; splitting
same-named segments does not explain this failure. No artificial zero, table
clipping, flag sweep or barrier is used to force agreement. The whole owner
is outside the default replay manifest and receives no callback credit.
The genuine spread now has its own independently accepted 63-byte owner in
`final_spread.cpp`, sharing this unchanged real body through `final_spread.inl`.

The subsequent `update_context.cpp` restores the genuine adjacent three
charge/fire functions before these two natural bodies. Its normal focused
replay passes two fresh complete939-byte updater scopes, the native zero,
all30 switch-table bytes, ordered fixup133 and its own initial-HP7400-to7300
compiled negative. Only the updater adds credit; the562-byte preceding source
context is already accepted. This supersedes the callback's unaccepted status
without altering the old failed receipt or any existing accepted record.
See [complete context and producer review](update_context.md).

The original fifteen ordinary boss phases now distinguish puppet entrance,
four pattern waves, three beam approach/attack pairs and final rings/spread.
The movement and attack submodes retain their observed numeric values.

## Shared typed Alice scratch-state protocol (2026-11-11)

The maintained complete 15-phase Alice Boss controller, both charge-pattern
sources, the stationary puppet beam, puppet motion and real puppet renderer now
refer to one `AliceScratch` **view of the original 16-byte `boss_statebyte`
array**. This is not a new allocation or shared object. Compile-time size and
offset checks cover the actual typed roles: byte 7 is the selected attack wave
(0–3), byte 8 the beam sprite base, byte 9 the beam phase, and byte 15 the
paired-stack/rotating-ring charge angle. The angle is reinitialized to 8 or 0
by each charge pattern; it is never treated as a persistent cross-phase field.

The Ready phase still writes the unchanged byte value 24 to offset 10. That
byte is deliberately named `ready_seed` with no asserted lifetime or new timer
semantics; its use by other patterns remains unproved. The beam's four states
(INACTIVE, CHARGE_CIRCLES, CONTRACTING, SPRITES) continue to use the accepted
`beam_phase.hpp` values without reinterpreting their 8-bit storage. The
complete controller still advances the wave index only after a finished
pattern wave, and the puppet motion/renderers continue to read the same
active beam phase as the beam producer. Neither zero-initialization nor new
phase-transition writes were introduced.

The complete replay of **all six changed source owners**, including the
939-byte Alice update, both charge functions, beam, motion, renderer and the
real foreground compilation context, was twice compiled with the pinned
Borland toolchain. Every original byte and ordered MZ relocation matches,
including the controller's original switch table. The compiled semantic
negative was rejected; the private receipt is
`.analysis/unit-replays/gpt-web-alice-shared-typed-scratch-20261111/receipt.json`.
No new authored byte credit, partial function acceptance, DATA/BSS or game
assets are inferred from the refactor.

## Wave HP ladder and complete beam/final attack clocks (2026-11-11)

The full 939-byte Alice update and its maintained standalone counterpart now
share the same complete controller body. Setup installs the first normal-wave
HP end gate of **7,400**, and each regular-wave completion copies the current
`phase_end_hp` into `boss.hp` before installing the next. The real repeated
2,200 HP decrement produces the sequential normal-wave boundaries **7,400 →
5,200 → 3,000 → 800**, then the final wave installs zero. This is a threshold
ladder, not a direct subtraction from the current Boss health on every frame;
beam approach/attack phases remain interspersed with these four normal waves.

Each normal wave retains the genuine **24 completed attack patterns** and a
three-way source-selected pattern variant after an eight-frame random-flight
lead-in. The original 128-frame setup and 64-frame ready gates, 128-frame
puppet entrance, initial 160-frame beam burst window, and 20-frame minimum
bullet-clear time remain separate semantic clocks. The three puppet beam
attacks still time out on the original strict `< 600` test, while the final
spread remains hittable during the original strict `< 1000` interval. The
original seven-point regular and five-point beam reward scores are also
explicit source constants; no unrelated health or sprite state was reset.

`main-alice-update-context` was rebuilt twice by the actual pinned Borland /
TLINK toolchain. Its whole **939/939 original bytes**, generated switch table,
alignment and ordered MZ fixups matched. The compiled negative now changes
the actual named wave-one HP gate from 7,400 to 7,300 and was rejected. The
focused receipt is
`.analysis/unit-replays/gpt-web-alice-wave-hp-timers-fixed-20261111/receipt.json`.
These are semantics of already accepted game C++ CODE, not newly attributed
or padding bytes; no full cold replay was run.

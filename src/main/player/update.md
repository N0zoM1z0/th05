# Player update lifecycle

This new natural C++ candidate covers one complete original MAIN function,
load `CC3D..CD56`, 281 bytes and 85 instructions. The full decoded range ends
at RET immediately before the separate renderer. All branch destinations are
real instruction boundaries in the same function. There are no native NOPs,
compiler tables, padding, loader relocations or owned DATA/BSS. No prior
maintained definition or failed replay of this function is reused.

Maintained TH04 `src/main/player/update.cpp` provides a natural semantic donor;
ReC98's TH05 `sub_1214A` corroborates the independently read original. TH05
decrements invincibility and clears pending hits together. Otherwise a pending
hit starts the 40-frame deathbomb/miss window, 192-frame invincibility and
72-frame respawn movement. Ordinary movement retries conflicting input once,
optionally halves signed velocity, clamps position and records the new input.

TH05 shot dispatch differs from the donor: a held shot starts the 18-frame
counter only when zero; an out-of-range counter is cleared; each nonzero frame
calls the actual near Pascal character callback and decrements the counter.
It does not use TH04's three-shot dispatch points or extra SE call. Respawn
calls the genuine full-motion method and discards its full-point return.
No register-result extraction or changed return ABI is needed. The option's
complete current/previous points are copied before velocity compensation,
followed by the real bomb and accepted miss-state calls.

The full canonical `PlayfieldMotion`12, `SPPoint`4 and byte movement-result
enum are reused. The near Pascal shot callback has the same complete function
signature as the canonical session selector. All globals remain real foreign
objects with independently recorded DS offsets. There are no shortened views,
instruction templates, physical-register aliases, hints, artificial barriers,
flag experiments or accepted-header edits.

The symbol-only binder anchors main_01 CS `0AE1` and DS `209D`, binds actual
earlier motion/movement/clamp/miss entries and the later bomb entry, and places
all origin holes outside the complete owner. It supplies no foreign bodies,
data values or stack. Every individual origin is below 64 KiB.

Private `.analysis/player-update-boundary-review.json` records instructions,
calls, globals, source identities and the eight-file closure; its reproducible
native-only reader is `.analysis/review_player_update.py`.
`.analysis/player-update-candidate.json` proposes the complete contribution and
a genuine CPP mutation lengthening the miss window from 40 to 41. Compilation,
two fresh raw/ordered checks and that independent negative remain required.
This preparation claims no acceptance and does not revisit parked movement,
invalidation, shot-runtime or renderer candidates.

The first focused producer `main-player-update-a` emits 286 bytes rather than
281, so its boundary gate stops before a second producer or negative. Native
review isolates exactly five extra instruction bytes immediately after
`player_move`: the returned AL byte is stored at BP-2 and compared from that
local, whereas the original tests AL directly. The discarded genuine motion
return and complete DWORD option copies already have the original instruction
sequences. No semantic, field-width, movement-result type or helper-prototype
error was found. The oversized contribution shifts the foreign bomb label by
five bytes and DATA labels by six after alignment; these operand differences
are consequences, not evidence of incorrect state offsets.

Private `.analysis/player-update-a-native-review.json` and its native reader
record the retained object/MAP/MZ/source hashes, exact result spill and explicit
context diagnosis. Diagnostic instruction correspondence does not normalize
the oracle or accept its raw mismatches. Source, header and binder remain
unchanged and frozen; the failed producer receives no exact credit.

The root then made one ordinary direct-expression correction: the existing
condition consumes `player_move(input)` immediately, removing the unused
single-use result object. Its actual byte result and Pascal near prototype
remain unchanged. Focused receipt `main-player-update-b/receipt.json` passes
both fresh producers for all 281 bytes with the original empty relocation
stream. The independently compiled miss-window mutation from 40 to 41 is
rejected. The root imported one complete function and 281 authored instruction
bytes. CPP, header and binder are now frozen accepted inputs; producer a stays
unchanged and failed, and no allocator or physical-register hint was added.

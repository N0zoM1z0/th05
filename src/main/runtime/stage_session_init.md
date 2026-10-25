# Stage-session initialization

Natural C++ candidate for original MAIN load `B237..B55A`, frame `AE1`, DS
`209D`. The complete 803-byte function contains 257 instructions occupying
772 bytes, the original zero at offset 772, and three compiler switch tables:
seven stage entries at `[773,787)`, four second-character entries at
`[787,795)`, and four first-character entries at `[795,803)`. Every table target
was checked against a complete original instruction boundary. No byte is
masked or supplied by the source/binder. The zero receives no authored credit;
potential authored CODE is 802 bytes, including all 30 generated table bytes.
The retained first producer is inexact, as recorded below. This owner is
unaccepted.

The original MZ relocation offsets, in their existing order, are:
`[755,748,668,657,614,576,551,526,501,475,449,401,372,361,352,306,297,288,224,202,191,186,56]`.
The following stage-runtime initializer starts at `B55A` and is a separate
174-byte function; the accepted cleanup function at `B608` is also outside
this owner.

The maintained semantic donor is sibling TH04's
`src/main/stage/session_init.cpp`, with original TH05 `sub_B237` operands,
branches and complete post-return tables reviewed independently. Donor
acceptance does not transfer. The unchanged complete 128-byte `resident_t`
provides every accessed field. No shortened Resident or replacement callback
record is introduced.

TH05 initializes character resources only for a new ordinary or Extra game.
Its debug branch copies the actual debug stage/power, consumes the Resident
debug flag and enables the existing runtime `debug_frame_step_enabled` byte
at DS `91`. Demos select their saved stage, use maximum power except for demo
5, install the real `DemoPlay` hook and seed the existing LCG with 318.
The input-hook type remains the canonical near cdecl no-argument callback;
the real Pascal null callback is explicitly converted between zero-argument
calling conventions, both of which clean up zero bytes. Overlay callbacks
retain their actual near Pascal types.

The setup order preserves the blue-page clear service, page selection,
eyecatch palette, overlay wipe, stage runtime/HUD/eyecatch initialization,
midboss reset and character resource loading. The native conversion loop is
**12 through 171**, ending at the real sprite boundary 172. The three source
switches select real named external filename objects and stage setup functions.
Stage 6 genuinely references distinct copies of `BSS4.CD2`/`st04.bft`, sets
Shinki's normal/bomb background callbacks and skips MPN loading. Extra updates
the real shot level before loading its resources.

All 34 filename objects are external arrays with their original reviewed DS
addresses. No filename payload, pointer table, asset data or byte array is
defined or credited. Existing state globals are reused with their real types,
including the far stage-BGM pointer, full Resident pointer, callback slots,
palette tone and random seed.

Graphics page switching uses ordinary `outportb` macros from the maintained
master API, corresponding to the actual PC-98 ports `A6` and `A4`. No physical
register template or copied graphics kernel is embedded. `vsync_Count2` is the
actual asynchronous interrupt-driven clock, declared volatile for its busy
wait, not an invented optimization barrier. The near blue-page clear service
is the original existing hardware routine at `105CA`; its implementation
remains foreign and receives no credit here.

Library interfaces retain their real far Pascal parameters. HUD rendering,
tile activation and shot-level updating keep genuine far-return ABIs in the
observed same `AE1` frame. Midboss reset remains far in `1527`; sound remains
far in SHARED frame `14AB`. Same-frame transfer shortening is an actual
producer question, never an excuse to declare a far callee as near. The
standard master text, palette, pattern loading and sound APIs retain their
real scalar and far-pointer types.

`probes/units/stage_session_init_bindings.asm` anchors only real foreign CODE
and DATA labels with origin holes outside the complete source contribution.
It adds no stack, code instructions, owned bytes or filename payloads. The
proposed module `th05/stg_sess.cpp` follows DOS8.3 naming. Its own staged
negative changes the pellet bottom color from 9 to 10, affecting real stage
state.

Private `.analysis/stage-session-init-boundary-review.json` records target and
extent digests, original calls/ordered fixups, real interfaces, every filename
identity and the exact input closure. The candidate entry/control is in
`.analysis/stage-session-init-candidate.json`. Acceptance requires the first
actual MAP/OMF extent gate, two fresh complete raw/fixup comparisons and the
compiled negative. If natural output is 802 bytes because the zero is missing,
retain that failure and stop: no flag search, padding insertion or partial
table exemption is proposed.

## Retained first-producer result

`main-stage-session-init-a/group-0/a/source` generated a complete **802-byte**
CODE contribution. It has the same 772-byte instruction region and near RET
at `B53A`, followed immediately by the same 30 table bytes at `B53B..B559`.
The original zero at `B53B` is absent. The tables are byte-identical when
compared at their actual locations; this does not satisfy the complete
803-byte comparison.

There is an independent transfer/fixup mismatch. HUD, tile activation and
shot-level updating use real far CALL instructions in this producer, where
the original uses NOP/PUSH CS/near CALL. Each form occupies five bytes, so the
instruction region remains 772 bytes while its instruction count becomes
251 rather than 257. The candidate contains 26 ordered MZ relocations rather
than 23; the three additional segment sites are offsets **598, 406, 216** in
their actual emission order. None is removed or normalized.

The one-byte shorter contribution also moves all foreign tail CODE symbols
back one byte, changes the three table-base operands and shifts SHARED/main-03
frame coordinates. The actual word alignment restores DATA to `209D:0`, so
the DATA symbol offsets themselves remain correct. These placement effects
do not constitute new source-global discoveries or exact comparisons.

Private `.analysis/stage-session-init-a-forensics.json` pins the actual
object/MAP/MZ and compiler input hashes, table locations, transfer instructions
and both unmodified relocation sequences. CPP, header and binder remain
byte-identical to the saved first producer. The early complete-extent gate
stopped before the second producer and negative control. No authored credit
was imported, and no further flags, padding, source or binder variants are
proposed for this missing-zero owner.

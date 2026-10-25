# Shot motion and collision runtime

The complete shot updater is accepted from `main-shots-update-abi-b`, using
MAIN frame `AE1` and DS `209D`. The two collision functions remain parked
candidates. Historical failed producer observations are retained below;
their byte counts do not establish acceptance.

| Function | Original load interval | Complete bytes | Original ordered MZ offsets |
| --- | --- | ---: | --- |
| `shots_update()` | `133DB..13573` | 408 | `[202,112]` |
| `shots_hittest()` | `13683..13812` | 399 | `[134]` |
| `shots_hittest_laser()` | `13812..138E4` | 210 | `[166,134]` |

The update contains 147 instructions occupying 400 bytes, followed immediately
by its complete four-word compiler switch table at `1356B..13573`. There is no
table-prefix padding. A boundary ending at `1356B` would omit this real table.
The collision pair contains 143 and 73 instructions, without tables or padding.
Its combined 609-byte ordered relocation list is `[134,565,533]`; the order is
not sorted or normalized.

The renderer between update and collision code remains a foreign hardware
owner. Likewise, the genuine existing `hitshot_from` helper remains external;
neither hardware rendering nor helper instructions have been transcribed into
compiler C++.

## Complete types and genuine interfaces

`shot_runtime.hpp` imports the frozen canonical 18-byte `Shot`, 12-byte
`PlayfieldMotion`, 14-byte `BulletTemplate`, player and resident surfaces.
The complete six-byte `shot_alive_t` contains an `SPPoint` and real near Shot
pointer. The complete 14-byte `hitshot_t` contains age, pattern and full motion.
There are 64 shot/cache slots and 24 independent decay slots. Compile-time
size/offset checks cover these new complete layouts.

Update is near cdecl `void(void)`. Both collision entries are far cdecl
`int(void)`, returning AX with RETF. The full four-byte point result of
`PlayfieldMotion::update_seg1()` is the real DX:AX ABI. `shot_velocity_set`
also retains its canonical full point return and near Pascal parameters.
The accepted update retains the real full return type and consumes the
actual packed result immediately through readonly signed AX/DX ABI reads.
Both live-cache coordinates are written before pointer/count changes, and
the second result is dead before age division. This proven DOS-intrinsic
return bridge introduces no fake scalar declaration, record view, register
arithmetic or instruction template. The earlier named-point receiver and
its spills are historical failed evidence, not the accepted implementation.

The collision helper interfaces are genuine: near Pascal `hitshot_from` at
`13617` takes a near Shot pointer and RET2; sparks are far Pascal at
`1527:1C16`; regular reflected bullets use far cdecl `1527:231A`;
`randring1_next16` is near cdecl at `C700`. The character selector at
`AE1:219C` has real far Pascal RETF8. Native packed pushes and the callee's
stack indexing establish bomb contributions **(3,4,15,3)** in formal
Reimu/Marisa/Mima/Yuuka order. Its original call is genuinely relaxed by TLINK
to NOP/PUSH CS/CALL, not declared as a fake near API.

## Preserved behavior

Update clears removed slots, turns live homing shots toward the target using
the unsigned byte angular difference, accelerates the three missile types,
and builds the real live-shot cache. Homing expires at age 16 while retaining
that frame's homing step. Clipped shots become removed. Decay sprites keep
their original three frames per cel, twelve active frames and historical
out-of-bounds age sentinel 18.

Both collision functions perform inclusive unsigned relative-distance AABB
tests. The per-call hit count attenuates subsequent shot damage, with a minimum
of one per hit. A persistent byte counter creates sparks on alternating hits,
then the real helper converts the shot to its decay animation and invalidates
the cached x coordinate with Subpixel None (`-999 * 16`).

Ordinary collision preserves bomb damage, Marisa's upward laser check,
stage/character scaling and the unsigned score increment. The Marisa bomb
check deliberately has a horizontal interval and a single unsigned lower-y
bound, as observed. The laser collision variant emits reflected regular
bullets except on three out of four Easy frames. Its whole-point assignment
uses the legitimate `SPPoint` base of the full canonical `PlayfieldPoint`;
the full four-byte geometry is copied without a shortened fake layout.

## Focused replay packets

Private `shot-collision-{candidate,boundary-review}.json` and
`shot-update-{candidate,boundary-review}.json` under `.analysis/` pin complete
bounds, target/extent hashes, all native calls, original ordered fixups, globals
and source closures. The collision packet proposes a whole 609-byte producer
and optional complete function scopes. Its ordinary compiled negative changes
Marisa's additional bomb damage from 22 to 23; the laser scope has its own
meaningful reflected-bullet scheduling mutation available if needed.

The independent update packet compares all 408 bytes, including its eight
compiler-generated table bytes, and changes missile vertical acceleration from
4 to 5 in a staged negative. Both symbol-only binders preserve real foreign
frames and globals using origin holes exclusively outside owned contributions;
they provide no instructions, owned DATA, target bytes or stack allocation.
The updater passes its complete raw/fixup/dependency gates as described
below. The collision candidates still require their own successful gates.
The frozen canonical record and method headers remain unchanged.

## Initial producer observations

`main-shot-collision-scopes-a` stopped at a missing `bullet_template`
declaration. The consumer now explicitly declares the real complete canonical
`BulletTemplate` object; the shared runtime header and accepted template header
were unchanged. The next first producer, `main-shot-collision-scopes-b`,
generated 400 bytes for ordinary collision and 218 for laser collision, compared
with original 399 and 210. Its ordinary collision loop spilled the local
quotient/clamp temporary, while two compound right shifts shortened later
regions. The apparent one-byte size difference is therefore several independent
instruction differences, not missing padding. Its character selector remained
a far CALL rather than the original relaxed transfer. Far helper and DS offsets
shifted as a consequence of the nine extra bytes in the full contribution.

The corrected collision candidate interprets the canonical byte damage field
as unsigned before promotion, uses the ordinary quotient ternary directly in
the damage sum, and expresses the two unsigned divisions by four as ordinary
rvalue assignments. These are semantic dataflow expressions; no physical
register, padding, fake declaration or fence is introduced. The real selector
declaration is unchanged, and its transfer form remains a producer question.

The next first producer, `main-shot-collision-scopes-c`, generated 419 bytes
for ordinary collision. It correctly zero-extended shot damage and restored
the original AX-based unsigned divisions by four. However, the pure repeated
quotient ternary emitted a second complete IDIV calculation after testing the
first quotient. Those extra 20 bytes exactly explain `419 - 399`. The real
selector still remained far. This producer is retained as a failure. A cached
unsigned quotient would preserve the mathematical range (0..255), but there
is no native evidence that TCC would avoid storage or preserve the original
word-width test. No further quotient variant is proposed; both collision
functions remain parked and unaccepted.

`main-shots-update-a` generated 431 complete bytes instead of 408. Its typed
point receiver increased the frame from six to ten bytes and spilled both
DX:AX returns. The first clipping/cache region grew by 13 bytes and the second
clipping region by 11; signed promotion of the canonical `char type` shortened
the switch setup by one byte. The net difference is therefore `24 - 1 = 23`.
Angle updates also used a different same-length instruction arrangement.
The resulting foreign DS drift is a layout consequence, not a newly inferred
global address. The parked source now explicitly interprets the switch type
byte as unsigned, matching the original zero extension. The canonical accepted
`Shot` definition remains unchanged: ReC98 also declares these fields as plain
`char`, so an unsigned replacement structure is not justified. That initial parking decision was superseded by the independently proven
real return-boundary bridge; it never authorized physical-register algorithm
transcription or fake return types.


## Accepted updater

`main-shots-update-abi-b` passes two fresh deterministic producers for the
complete408-byte updater:400 instruction bytes plus the complete8-byte
semantic switch table, no padding, with original ordered fixups `[202,112]`.
The compiled missile acceleration mutation4-to5 is rejected. The receipt is
`.analysis/unit-replays/main-shots-update-abi-b/receipt.json`; this is one
control for the complete owner, not independent controls for each branch.

The first ABI parent generated the correct408-byte size and ordered fixups
but both raw comparisons failed at homing ADD/SUB placement and the common
AL store. It remains preserved and unaccepted; it was never raw exact.
The accepted source keeps canonical `Shot.angle` as char and uses its real
unsigned-character near-reference storage view at only the +=/-= mutations.
That expresses the genuine modulo256 angle domain and restores direct byte
memory operations without a changed record/prototype, compiler flag, idle
branch, physical-register hint or barrier. Full Motion/Point declarations,
the exact result lifetime and cache stores remain intact. No acceptance
transfers to either collision function or the separately parked renderer.

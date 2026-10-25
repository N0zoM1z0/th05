# B4 custom-ball update candidate

The original complete MAIN function is `[18459,1856A)`,273 bytes and88
instructions. The native final RET is18569; the following real function starts
at1856A. There are no NOPs, compiler tables or trailing alignment bytes.
Original ordered MZ fixups are `[235,156,118]`. The accepted132-byte reset and
allocator end exactly at18459 and are excluded from this owner.

This natural C++ reconstruction follows independently decoded original
operands and ReC98 `b6ba5b0a`'s `th05_main.asm` lines14040..14156 as semantic
reference. It does not transcribe compiler instructions. The unchanged
accepted `b4ball.hpp` provides all26 bytes of every ball, the complete25-byte
template, and the full64×26-byte custom-entity storage. Slot0 is the template;
slots1..63 are live balls. Age, speed, angle, previous position and unused
physical members remain present even when the updater does not modify them.

Each active ball advances its real Motion, clips with a16-pixel margin, and
checks the player's16×16 hit region. Existing shot collision uses the ball's
real current position and8-pixel hitbox radii. Nonsnow balls play sound10 on a
hit. Snow balls take damage, play sound4, and enter decay only below zero HP.
Destruction quarters both signed velocity components with division toward
zero, adds550 score, and optionally emits the existing regular bullet at the
current ball position when revenge is enabled and Y<=240 pixels. Decay advances
one sprite every four age ticks and frees the ball after four cels.

## Actual point return and lifetime

The canonical full method remains
`PlayfieldPoint pascal near PlayfieldMotion::update_seg3()`. Actual1527C..1529C
reads its near this pointer at SS:SP+2, updates the complete12-byte Motion,
returns signed x inAX/y inDX and ends with RET2. The original caller pushes
the genuine near object pointer at18481 and calls at18482.

Both returned coordinates are used for clipping at18485..18499 and then for
the player-relative hit test at184A5..184C3. Neither coordinate survives a
helper call:184C4 reloads the actual ball current position into the separate
shot-hitbox object before the first helper at184CC. The first candidate used a real full `PlayfieldPoint` local assigned from the
unchanged method. The later bounded return bridge below instead consumes the
actual returned words immediately, following the already accepted shot updater.
The full return type, physical fields, method and cleanup remain unchanged.
There is no scalar/void return retag, CF convention, shortened class, assigned
register alias, register allocation hint or instruction template.

The foreign shot-collision provider is real far C++ `int shots_hittest()` at
AE1:8873. Sound is far Pascal `snd_se_play(int)` at14AB:0232. Regular bullet
emission remains the existing no-argument C near routine at1527:1F94. The
symbol-only scaffold places all foreign code/data at their true frames and
retains even empty foreign compiler segment names in the correct groups.
It supplies no helper body, initializer, stack, owned CODE bytes or internal
hole. Source-owned DATA/BSS is expected to be empty and must be checked from
actual OMF/MAP output.

This packet remains unaccepted. The actual first producer below establishes
the complete contribution. Its size failure is retained honestly, without
padding, output patching, flags searches or suppression of a real spill. The proposed own compiled
negative changes the real destruction reward from550 to551. Private
`.analysis/b4ball-update-boundary-review.json` pins target instructions, the
complete class/dependency identities and the true return lifetime;
`.analysis/b4ball-update-proposal.toml` is a registration suggestion only.

## First producer: unaccepted296 bytes

`main-b4ball-update-a` stopped at its first size gate. Its one real compiler
CODE contribution is296 bytes/91 instructions, versus original273/88; no second
positive, compiled negative or acceptance receipt was produced. The retained
MZ/MAP/OMF and compiler arguments remain unchanged under that private directory.

The full Point call ABI is correct. Both callers contain the same six-byte
LEA/PUSH-this/CALL sequence, with no hidden return pointer or extra argument.
The candidate captures returnedDX into `[BP-4]` andAX into `[BP-6]`; its ENTER6
frame holds the real four-byte Point plus the original two-byte damage local.
The original ENTER2 frame keeps only damage. Coordinate signs, clipping bounds,
player-hit comparisons and the first shot-helper boundary are consistent with
the intended semantics. Neither returned coordinate survives a helper call.

The exact23-byte length delta decomposes as follows:

| Lowering difference | Bytes |
|---|---:|
| Two Point-word stores | +6 |
| Memory clip comparisons instead of AX/DX comparisons | +6 |
| Direct long conditional branches instead of the short local remove proxy | +5 |
| Point reloads for player collision, net of accumulator encodings | +4 |
| Damage stack compare instead of testing the returnedAX directly | +2 |

This is not evidence for changing the method's return type, removing physical
fields, imposing register allocation, suppressing spills or adding a register
clipping kernel. That complete first source and its real Point local remain frozen in the
failed producer. The current source has the bounded return bridge below; no
register/flags/source-variant matrix is proposed.
Original fixups are `[235,156,118]`; actual fixups are `[258,179,139]`, retained
in their original order.

The first binder also contained an independent factual object-base error:
`_bullet_template` was anchored at5780, the address of its origin field.
The unchanged complete canonical BulletTemplate has origin at+2 and begins at
DS577E. Only that binder label was corrected to577E at the time; the original CPP/HPP
and all accepted headers remained unchanged. The original actual binding alias and
canonical staged copy are byte-identical and remain frozen, with a separate
copy at `.analysis/b4ball-update-a-actual-bindings.asm`. The corrected binder
has **not** been recompiled and cannot remove the23-byte source-size gap.

The failed first producer's nominal273-byte outside tail also ends24 bytes
later after296 actual CODE bytes and word alignment: `_DATA` starts at209E8,
DGROUP is209E and its actual labels gain8 in DS offsets. This layout drift is
recorded separately; no field/type reinterpretation follows from it. It is
not corrected or accepted by the single object-base fix. The current source
candidate stays outside default replay. Private
`.analysis/b4ball-update-a-native-forensic.json` and
`.analysis/b4ball-update-binder-correction.json` preserve the full paired native
evidence, immutable artifact hashes, frozen unit schema and correction history.

## Bounded full-return bridge: unaccepted278 bytes

A later cross-owner review found a directly applicable precedent:
`src/main/player/shot_update.cpp`, accepted in `main-shots-update-abi-b`,
consumes the genuine packed Point return with readonly Borland DOS `_AX` and
`_DX` intrinsics. B4 has the same full return ABI and bounded lifetime: both
words are dead before the first collision helper. The new candidate removes
only its materialized Point copy, keeps the full canonical method return,
and uses signed reads for clipping and unsigned relative-distance tests.
The damage assignment now appears inside its real condition, so the returned
AX is tested immediately. These are two evidence-based changes, without
inserting ASM, retagging an API or changing any accepted header/source.

`.analysis/unit-replays/main-b4ball-update-return-b/` contains exactly one new
compiler/assembler/linker producer. Its full contribution is278 bytes and88
instructions, against273 bytes and88 instructions in the immutable original.
The actual frame is now ENTER2; neither returned coordinate is stored on the
stack. Actual immediate clips and the intervening memory flag comparison
preserve AX/DX. The x distance is consumed in AX while DX remains untouched;
the y coordinate is then copied from DX into AX after x is dead. Both words
are consumed before the real shot-collision call. The actual damage zero test
now agrees with the original AX test. This establishes the bridge's bounded
lifetime, not exact acceptance of the function.

The complete residual size difference is the clipping region:30 versus25
bytes. Four direct near conditional branches replace the original four short
branches and its local removal proxy. The31-byte player-distance region has
the same length but uses different register lowering. These differences are
not padding. Original and actual instruction NOP enumerations are empty;
there are no tables or trailing alignment bytes in either function.
Original ordered fixups remain `[235,156,118]`; actual is `[240,161,123]`.

The actual comparison link also retains the nominal273-byte foreign tail,
so its five extra CODE bytes plus WORD alignment place DATA at209D:0006.
All bound DATA offsets move by6; template577E becomes5784 and its origin5786.
No whole-function runtime equivalence is claimed for this linked output.
This is separate from the source return lifetime and from the earlier fixed
object-base error. The first complete-size gate rejects the producer, with
no second positive, compiled negative or acceptance receipt. This owner stays
outside default replay selection; no compensating bytes, branch templates,
register arithmetic kernel or speculative source variant is introduced.
Unchanged installed execution proofs and all accepted evidence were reused.

Independent native/lifetime review:
`.analysis/b4ball-return-bridge-review.json`, SHA-256
`5088f2bfb87599834df077b5841dee76d37e9b768e3c9465c92a5c183e1326bb`.
Independent actual OMF/MAP/MZ/code review:
`.analysis/b4ball-return-bridge-actual-review.json`, SHA-256
`973105654a4da84435a633d1a3f7ba56b3ff2a623c7ab570fad408b72c47ebe1`.
Authored units, function counts, C/C++/ASM bytes and ownership are unchanged.

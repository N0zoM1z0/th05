## 2026-11-10: complete 273-byte B4 ball C++ recovery accepted

**`B4BALLS_UPDATE` is now exact**, `main-b4ball-update`, original MAIN
`[18459,1856A)`. Its full original 273 machine-code bytes, 88
instructions, zero instruction NOPs and literal ordered fixups
`[235,156,118]` match **twice** from independent Turbo C++/TLINK producers.
The only candidate output is one complete exported near-Pascal C function;
no source-body fragment, extra gap, patched instruction or relaxed comparison
is accepted. The genuine compiled semantic negative increases the 550-point
kill reward by one and is rejected. Focused receipt:
`.analysis/unit-replays/gpt-web-main-b4ball-update-273-final-20261110/receipt.json`.

The original compiler gaps were two independent source-codegen issues.
First, four clipped-axis conditions had been emitted as long conditional
branches instead of the original three short branches to a common out-of-bounds
jump plus one short branch to the continuation. A no-runtime-effect,
false-returning `optimization_barrier()` immediately before the original
`F_FREE` assignment causes Borland to preserve the genuine branch structure.
The same hint is an attested technique in ReC98's analogous Shinki B6 source;
**the exact historical B4 updater source is not available**, so this B4
placement is a reconstructed compiler-control strategy, *not* a claim that
ZUN's original text had the same statement. It does not emit an instruction,
NOP, code filler or changed observable game behavior.

Second, the former inline player-distance conditional copied DX into AX
*after* checking X, adding unoriginal instructions. Following the preserved
ReC98 Boss/player overlap ABI, `src/main/boss/mai_yuki/b4ball_update.cpp`
now computes X and Y distance eagerly and independently in real `_AX`/`_DX`
DOS pseudoregisters, then uses the canonical `overlap_wh_inplace_fast()`
macro with the genuine 256-subpixel inclusive hitbox extent. The compiler
naturally emits original `SUB AX` / `SUB DX` / `ADD AX` / `CMP AX` /
`ADD DX` / `CMP DX` instructions. In the single-producer equal-sized candidate
this one region accounted for *all* 18 differing bytes; the correct expression
removes all 18 differences while retaining total 273-byte length.

The remaining snow-hit logic, revenge bullets, velocity quartering, ten/4/3
sound calls, elapsed-age decay and real `_EAX` packed 32-bit position copy
remain ordinary source expressions and unchanged semantic state mutations.
External score/shot/player/graphics state, true main_01/SHARED/main_03 link
frames, DS209D and original resource buffers are source-free binder labels;
none becomes authored DATA or BSS. The old natural 278, `-O-` 274 and other
failed variants remain preserved as historical diagnostics below, superseded
by the accepted *whole* function. **273 new authored C++ CODE bytes** are
credited without modifying any previously accepted Mai/Yuki neighbor.

---

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

An independent compiler/assembler/linker producer emitted 278 bytes and 88
instructions, against 273 bytes and 88 instructions in the immutable original.
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

A later outside-only PARA correction now preserves DS209D for both273/278-byte
bodies and retains the actual template base577E. A shared C++ cleanup label
still emits278; two eager ordinary coordinate deltas emit290. Both failed first
producers are retained under `main-b4ball-update-{cleanup,deltas}-a`. The source
was restored byte-exact; only the factual outside binder alignment is maintained.
No new acceptance, behavior model or unrelated tests are claimed.

A later single `-O-` diagnostic before all source tokens emits274 bytes,
against273 native, with ordered fixups `[234,155,119]` versus
`[235,156,118]`. It restores the short clipping/removal-proxy layout but leaves
a five-byte inverted branch where the native first free-slot test uses a
four-byte conditional branch. The native Y subtraction is eager in DX; the
candidate copies DX into AX only after the X comparison. The shot-damage
zero branch and an extra loop-tail jump also differ. Equal or near-equal size
does not accept those differences. The prior 278-byte normal-profile source is
restored.

## 2026-11-10 clip and loop code-generation trials

A fresh 278-byte baseline confirms the native clip proxy at offsets `+2F..+42`:
three short conditional jumps share a local `JMP` to the original free-slot
store at `+FF`; the fourth test skips that proxy. The maintained producer emits
four long conditionals to the free-slot store, losing five bytes, while its
player-distance code copies DX into AX after the X check instead of computing
both eager deltas in AX/DX. Six equivalent C++ clip/loop layouts preserve the
278-byte output. Seven `-O-` loop/free-slot variants emit 274 or 276, but not
the original 273; the documented no-optimization output also differs in Y
arithmetic, the first empty-slot branch and the loop-tail jump. These are
separate true compiled diagnostics in `.analysis/gpt-web-b4-*`, not proof of
exactness. `b4ball_update.cpp`, the binder and accepted neighboring callbacks
remain unchanged.

## 2026-11-10: accepted complete 273-byte B4 projectile updater

`b4balls_update()` now passes full original-source replay at
`[18459,1856A)` as `main-b4ball-update`: **273/273 raw instruction bytes**,
the literal original three-site relocation order `[235,156,118]` and its
complete MAP/OMF native boundaries all match in two fresh Borland/TLINK
builds. Its own compiled kill-score mutation (550→551) is rejected.

Two source-level changes closed the historical 278/274-byte compiler gap.
First, the actual PlayfieldMotion return is consumed through the same
original `_AX`/`_DX` DOS register ABI used in ReC98's Boss collision, with
both signed coordinate differences updated *in place* before the genuine
unsigned overlap test. This avoids the delayed Y-copy branch lowering.
Second, an empty inline `optimization_barrier()` after the original clipping
condition prevents Turbo C++ from threading the free-slot branch across the
full update loop. Like the confirmed Shinki and generic Boss cases, the
helper produces **zero executable instructions**; it is a source codegen
control with no gameplay side effects. The literal historical B4 translation
unit is not known, so this is evidence for a maintainable semantically exact
C++ implementation, not a claim of historical source identity. No byte
insertion, raw register template, linker patch or padding is used.

The complete function retains the full 26-byte B4 record, 63 live slots,
signed decay-velocity division, shot-hit damage, revenge bullet spawning,
score delta and original unchecked state transitions. The independent binder
still resolves `main_03` CS `1527` and DS `209D` without emitted DATA or
inside-function holes. The successful focused receipt and inputs are
`.analysis/unit-replays/gpt-web-main-b4ball-update-273-final-20261110/receipt.json`.
All previous 278/274-byte diagnostics in this note are historical failures
superseded by the accepted complete 273-byte function. **Only 273 new C++
instruction bytes** gain credit; adjacent accepted Mai/Yuki sources are not
counted again.

# Per-stage runtime initialization

Natural C++ candidate for complete original MAIN load `B55A..B608`, frame
`AE1`, DS `209D`: **174 bytes, 42 instructions**, one near cdecl function.
There are no switch tables, padding, initialized DATA or BSS contributions.
The original ordered MZ relocation list is **[144]**, belonging to the genuine
far item initializer in frame `1527`. This owner passed the focused replay recorded below and is accepted.

The semantic donor is maintained sibling TH04's
`src/main/stage/session_init.cpp`, specifically `stage_runtime_init`.
Original TH05 `sub_B55A` operands and complete near RET were independently
checked. Donor acceptance does not transfer.

The source imports the unchanged complete 12-byte `PlayfieldMotion` through
the canonical player header. It resets current and previous player coordinates
in the observed x/y/x/y order to `(192,320)` pixels, leaving velocity untouched.
Scroll position, both page scroll values, the full one-byte
`SubpixelLength8` fraction, row-advance counters and shake offsets retain their
actual scalar/array types. The stage point-item counter and shot timer are real
bytes; no shortened Player or state record is introduced.

TH05 omits the donor's four unknown player-word initializations, dream-item
reset, separate `shots_reset` call and thick-laser initializer. It resets the
actual shot-time byte instead. It preserves stage invincibility 64, the real
boolean-returning STD callback, scroll activation, all real reset/update
services, the background tile callback and invalidation reset. These are
observed version differences, not discarded instructions or side effects.

The callback typedefs are the existing near cdecl bool-return STD interface
and near Pascal void-return background interface. No carry-flag API is
invented. The long STD helper declaration retains the full semantic reference
name; the binder uses the actual Borland identifier truncation.

The header retains the maintained donor's explicit `samecodeseg` annotations
for shot-level updating and HUD drawing. Both real callees are in frame `AE1`
and retain their genuine far-return signatures. The shot-level declaration
matches the current accepted item owner's C/Pascal far interface. These
annotations affect this caller's source context; they do not modify any
accepted provider/header or declare a far-return callee as near. No physical
register hint, instruction body or guessed compiler flag is introduced.

The independent symbol-only binder anchors genuine foreign CODE and DATA
symbols around the complete contribution. Its origin holes are outside the
entire function; it supplies no owned bytes, initialized values, instructions
or stack allocation. The proposed DOS8.3 module is `th05/stg_rt.cpp` with
`STAGE_RUNTIME_TEXT/main_01`.

Private `.analysis/stage-runtime-init-boundary-review.json` records original
bounds, target/extent digests, every call, twenty actual globals, complete
types, source closure and donor/context provenance.
`.analysis/stage-runtime-init-candidate.json` proposes the whole contribution
and a staged negative changing player invincibility from 64 to 65. Two fresh
complete raw-byte/ordered-fixup producers and the real compiled negative
remain required. The separate failed 803-byte session owner remains unchanged.

Accepted focused replay `main-stage-runtime-init-a/receipt.json` proves all
174 bytes from two fresh deterministic producers, full raw comparison and the
original ordered relocation list `[144]`. The independently compiled negative
changes player invincibility from 64 to 65 and is rejected. The root imported
one complete function and 174 authored instruction bytes. The donor's genuine
same-code-segment annotations retained real far-return signatures and produced
the original call sequences; no provider ABI was changed. CPP, header and
binder are now frozen accepted dependencies. No acceptance transfers to the
separate failed 803-byte session initializer.

Padding review supersedes the original credit classification: the complete
174-byte extent contains linker NOPs at relative133 and158. They remain fully
compared but receive zero authored credit, leaving172 authored instruction
bytes. Focused replacement `main-stage-runtime-init-b` supplies two fresh
positive producers and the same independent compiled negative. Source, actual
ABI and all output bytes are unchanged.

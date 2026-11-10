# Stage-session initialization: exact source in original four-function context

The complete native stage initializer remains `[B237,B55A)`, 803 bytes.
Current root decoding checks all 257 instructions through the near RET,
every direct branch, and all fifteen destinations in the three post-return
tables. The 772-byte instruction extent includes linker-relaxation NOPs at
relative 213, 403 and 595, immediately before genuine PUSH-CS/near-CALL
transfers to far-returning HUD, tile-activation and shot-level services.
Those three NOPs get zero authored credit. The zero at 772 also gets none;
30 semantic compiler-table bytes remain mandatory. Potential credit is
therefore 799 bytes (769 instructions plus 30 tables), correcting the older
802-byte estimate. No authored counter changes from this review.

The true foreign interfaces and the entire initialization body are unchanged.
`stage_session_common_bindings.asm` is one conditional symbol-only source,
assembled on both sides of the actual C++ object. Its first view ends at
the complete source start. Its second view merges the real later far services
into the same public `STAGE_SESSION_TEXT` SEGDEF, at their actual addresses.
Both views have ordinary CRC-valid OMF, only reviewed metadata comments,
no LEDATA/LIDATA/fixups, no entry or stack and all ORGs below 64 KiB.
Original MAIN01/SHARED/MAIN03/DGROUP frames are modeled without retagging a
far API or supplying a helper body. The intended positive full end is B55A.

Before any new compiler invocation, a diagnostic relink reused the exact
earlier 802-byte `stg_sess.obj`. Its private
binder copy uses the actual old contribution end B559 solely to anchor
foreign symbols. The old object is unchanged; no output is patched. The
result restores all three native transfer forms and the original ordered
23-entry fixup stream. Its first 772 bytes differ only at table-base operands
261, 325 and 433, each one byte below the native table address. This is
routing evidence only: the zero is still missing and nothing is accepted.
Saved evidence: `.analysis/stage-session-common-routing-a/review.json`.

The actual new normal profile additionally enables ordinary `-a2` after all
canonical types and explicitly restores the CODE selector. It still emits
802 bytes. The first complete-contribution size gate rejects it before a
second producer or negative. The intended unchanged B55A tail cannot be
treated as a valid full positive layout for that shorter result.
The source and prepared common binder remain maintained, but the unit proposal
is parked privately outside the live manifest. No table cropping, inserted
zero, fixup sorting or ASM attribution follows from this failure.

The genuine native predecessors are entry110, gameplay-loop445 and
new-game-init468, totaling 1,023 bytes from AE38 through B237. A coherent
original-size prefix could supply the odd CODE phase naturally; this is a
future hypothesis, not proof of the historical TU or permission for a synthetic
prefix. The ordinary loop still has a real three-byte counter-lowering gap.
Its new meaningful modulo/compound/postincrement trials emit 442/442/444
bytes and remain complete-function failures; no second or negative is built.
The established baseline loop source is restored unchanged. See `main.md`.

Root native evidence: `.analysis/stage-session-current-native-review.json`.
Actual stage-binding/counter evidence:
`.analysis/runtime-stage-loop-resumed-review.json`, SHA-256
`e5f5d276eddd16da058657c648b5c48038feb8a6dfec4d0d518dc6be143ecc78`.
All 803 stage-init bytes and all 445 loop bytes remain unknown. Successful
installed execution probes and unrelated accepted objects were reused;
there is no global, packed-container or whole-program exactness claim.

A later first producer restores the donor-style normal `-a` after canonical
types, motivated by the successful item-family recovery. This standalone
initializer still emits 802 bytes, with the native 23-site order but no zero.
The source is restored to its prior baseline.
Normal alignment spelling alone does not establish the missing real context;
no second producer, negative or authored credit is added.

## 2026-11-10: complete 803-byte source recovery

`stage_session_init()` now passes strict native source replay at
`[B237,B55A)` with **803/803 original raw bytes**, including its authentic
30-byte compiler switch table and the otherwise missing alignment zero.
Both fresh Borland/TLINK producers reproduce the **23 original ordered
relocation sites**, actual near-Pascal start/end and all three relaxed
`NOP / PUSH CS / CALL` transfers to far services. A compiled change of the
original pellet-bottom column from 9 to 8 is rejected. The accepted scoped
unit is `main-stage-session-init-exact`; receipt:
`.analysis/unit-replays/gpt-web-main-stage-session-init-803-final-20261110/receipt.json`.

The complete original-order C++ translation unit
`src/main/runtime/stage_complete_context.cpp` contains four real adjacent
functions: `main()` (110), `gameplay_loop()` (445),
`gameplay_session_init()` (468), and `stage_session_init()` (803). A fresh
single-source diagnostic confirms their **whole 1826-byte `[AE38,B55A)`
contribution** and literal relocation stream match the native image. The
first three functions retain their **existing** accepted owners and receive
no new credit. This unit adds **799 authored bytes**: 769 instructions plus
30 compiler table bytes. Three real linker relaxation NOPs at stage-relative
213/403/595, and one zero at 772, are compared but not credited.

The decisive codegen constraints were **both** authentic source context and
original segment declaration order. Building the initializer alone emits
802 bytes and no switch-table zero. Building after only the real 445-byte
loop and 468-byte new-game initializer generates the zero, but its OMF record
partition places fixup +56 first, not last. Including the complete accepted
110-byte `main()` before those bodies naturally restores all 23 fixups in
their native order. For correct physical far-call frames, the compiler must
first declare the four genuine empty `main_01` segments, followed by the
ungrouped `SHARED` segment, followed by the three genuine empty `main_03`
segments. Otherwise `SHARED` gets absorbed by a neighboring group and
far-call CS operands change to AE1 or 14AB instead of their native value.
The maintained `stage_complete_context_bindings.asm` uses the existing
before/after symbol-only linkage supported by the local build tools: true
providers follow the **same** `DEMO_TEXT` segment after the compiler object,
allowing all three original same-CS far-return call relaxations. It emits
no foreign instructions or initialized DATA.

`stage_session_context.hpp` is the same original stage-session interface
with only a redundant sound enum declaration excluded because the preceding
real MAIN entry/gameplay header has already defined it. The linked function
bodies, packed record definitions, callbacks, flags and game behavior remain
unchanged; this is an original compiler-context recovery, not hand-emitted
ASM or target-byte patching. All previous standalone 802-byte findings above
are retained as historical diagnostics, not current ownership blockers.

# Stage-session common-segment investigation: no acceptance

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
archived 802-byte `stg_sess.obj` from `main-stage-session-init-a`. Its private
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
treated as a valid full positive layout for that shorter result. Its actual
source/argv/MAP/OMF and both binding views are retained under
`.analysis/unit-replays/main-stage-session-common-a/`.
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

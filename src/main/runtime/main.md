# MAIN entry and gameplay loop candidate

The new natural source owns the complete original consecutive functions
`main` at `[0xAE38,0xAEA6)` (110 bytes) and `gameplay_loop` at
`[0xAEA6,0xB063)` (445 bytes). These are offsets in the unrelocated MZ
program image of the locally attested TH05 MAIN executable, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Original instruction decoding covers both RET boundaries, and every local
branch lands on an instruction start. No following switch table belongs
to either function. The contribution uses `DEMO_TEXT`, group `main_01`,
frame `0AE1`; its native start was checked rather than transferred from
calibration or reference addresses.

The complete extent is 555 bytes: 553 instruction bytes and two original
linker-relaxation NOPs, at owner-relative offsets 103 and 534. Every byte
must compare; those NOPs receive no authored credit. The fifteen original
MZ fixups, in their existing order, are at relative offsets
`487,450,312,275,228,223,210,205,134,129,124,79,67,44,23`.

Semantic donors are the maintained TH04 reconstruction's
`src/main/core/main.cpp`, `gameplay_loop.cpp`, and `demo_prefix.cpp`.
Their source hashes are recorded privately. ReC98 `b6ba5b0a`'s
`th05_main.asm` supplies additional semantic and naming evidence. Neither
donor acceptance nor reference addresses establish TH05 exactness. The new
`main.cpp` includes the adjacent natural loop body to preserve a coherent
producer; the separate loop file remains readable on its own. No source
from an accepted owner is changed.

MAIN loads the real resident pointer, assigns 291200 bytes in DOS
paragraphs, initializes graphics/resources, seeds its process RNG from the
resident menu accumulator, preloads EMS state and selects the resident
sound modes. It runs stage sessions until the quit reason is not a stage
transition, then invokes the genuine far Pascal `GameExecl` API for OP.
The three filename objects are foreign bindings, at DS offsets `00B2`,
`00BE` and `00C3`. This packet supplies no initialized DATA or BSS.

The complete accepted `resident_t` is reused as 128 bytes; the entry reads
its RNG at offset40, BGM mode at18 and SE mode at21. No fictitious 256-byte
resident or partial Memory record is introduced. The entry does not
access a Memory aggregate. The complete three-value canonical quit enum
and canonical near-Pascal/far-Pascal callback typedefs are reproduced with
identical definitions, with compiler width assertions. Input/demo and
STD callbacks retain their real near C++ interfaces. The bombing renderer
uses the active `bg_render_bombing` callback at DS:3508. The separate stored
callback `bg_render_bombing_func` is DS:350A, as independently accepted bomb
controllers establish. The source spelling was corrected after the failed
producer; it remains unaccepted and was not replayed for this name-only fix.

The TH05 loop retains the actual update/render order, including lasers,
custom boss bullets, and the bombing-only player-character callback. The
STD callback performs midboss activation; TH04's additional direct call is
absent here. Bullet-caused slowdown participates in the 32-bit statistics.
The original Q-key debug stepping transitions use signed states0,-2,-1,1.
Frame counters and page flips use their actual word/byte widths. Performance
rank rises once per4096 stage frames rather than using TH04's remaining-life
formula. GRCG disable and access/display page selection use the genuine DOS
`outportb` intrinsic with ports `7C`, `A6`, and `A4`.

This remains a source candidate pending actual compiler evidence. The
natural frame increment and modulus chain deliberately contain no
pseudo-register transcription; the original unused DX copy may therefore
lower differently. Real far `GameExecl` and `playperf_raise` calls retain
the original API, while their five-byte linker-relaxation context is an
unresolved risk. No samecodeseg pragma, authored call instruction, filler,
NOP, flag manipulation, or inactive expression is added to force bytes.
An ordinary compiler/linker mismatch must remain unaccepted.

Private integration inputs are
`.analysis/main-runtime-prefix-unit-proposal.json`,
`.analysis/main-runtime-prefix-bindings.asm`, and
`.analysis/main-runtime-prefix-boundary-review.json`.
The outside-only binder supplies real foreign symbols and no helper
implementation or asset bytes. The proposed owner-level negative raises
the paragraph budget by one, changing actual allocation behavior. A
separate loop-only timer mutation is documented for a future independently
reviewed scope, if needed; it is not independent function acceptance.
Two fresh complete strict raw/ordered comparisons and the compiled negative
remain required before any authored credit. The subsequent stage-session
initializer beginning at `0xB237` is not recovered by this packet.

The later `main-entry-c` focused replay supersedes the entry-only blocker:
the canonical unchanged main body is now factored into `entry.cpp`, with
the independently verified same-CS far GameExecl context. Its complete110
bytes pass and109 instructions are accepted after excluding one checked NOP.
See `entry.md`. The combined555-byte candidate and complete gameplay loop
remain unaccepted; their earlier548-byte failed artifact is preserved.

## Bounded natural-expression result

One new standalone gameplay-loop producer is retained in
`.analysis/unit-replays/main-gameplay-loop-expressions-a/`. Two meaningful
conditional expressions recover the native debug-transition and periodic
rank-call control flow. The periodic-call expression follows the maintained
TH04 donor, and the same loop's existing palette expression corroborates the
compiler form. The real new frame value supplies modulo16 through ordinary
`++stage_frame`; no physical-register or unused-value expression is inserted.
The independently proved AE1 far `playperf_raise` interface is communicated
with its provider-specific samecodeseg annotation, retaining the far ABI.

The complete result is442 bytes versus native445. Both two-byte control-flow
branches are restored, and TLINK now emits the real relaxation NOP. The
remaining three-byte difference is the counter operation: actual memory
increment/load/byte-mask differs from native AX load/old-value DX copy/
increment/store/word-mask. The first complete-extent gate stops before a
second producer or negative. No bytes, record edits, arbitrary barriers,
flags or further expression variants are introduced. This source remains
unaccepted; its failed replay manifest is kept privately and omitted from
normal incremental plans.

Private `.analysis/gameplay-loop-expression-first-review.json`, SHA-256
`3bcad53f809161e6d0bd3b12bbc27873d55e10905678875b5036260a5689b50f`,
records the actual object, linked artifact, complete MAP scope, instruction
comparison and raw relocation lists. Unchanged older accepted entry inputs
are reused; no gameplay-loop bytes receive authored credit.

## Subsequent bounded counter-expression checks

The stage-session investigation required rechecking the genuine preceding
loop. Replacing the first mask with ordinary unsigned `%16` still emits442
bytes, with the same memory increment/load and byte mask. Consuming the
postincrement result as `(stage_frame++ + 1) %16` emits444, computing the byte
result before the memory increment; it still differs from native445.
The ordinary compound-result `(stage_frame += 1) %16` returns to442. All three
complete-function first-size gates reject the outputs before a second producer
or compiled negative. There is no physical-register alias, type change,
volatile annotation, inactive operation or compiler-flag matrix. The original
maintained baseline source is restored byte-for-byte.

An independent model executes the actual native and each of these three
compiled counter blocks for all65,536 input WORDs, including FFFF-to0 wrap.
All262,144 executions produce the mathematical next frame and modulo2/4/8/16
memory bytes, preserving adjacent canaries. Only these memory outputs are
checked: scratch-register differences, interrupts, callbacks, ports and the
whole loop are excluded. This proves bounded counter semantics, not exact
acceptance; all445 native bytes remain unknown.
Report `.analysis/gameplay-counter-memory-model.json`, SHA-256
`e2dbb6e2d9b22489d8ffb6365e96bd8f3d63eb9657aeafc0c6afdab89d1c83aa`.
Actual source/OMF/MAP/argv evidence is in
`.analysis/runtime-stage-loop-resumed-review.json`, SHA-256
`e5f5d276eddd16da058657c648b5c48038feb8a6dfec4d0d518dc6be143ecc78`.

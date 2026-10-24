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

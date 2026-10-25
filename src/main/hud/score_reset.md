# TH05 score preservation and reset candidate

The original complete `score_reset` occupies `[CFC6,D035)`,111 instruction
bytes in MAIN's unrelocated MZ program image. It is C++ near cdecl with no
arguments and a near RET. It contains no MZ fixups, NOPs, tables, DATA or BSS.

The TH04 maintained HUD donor supplies the ordinary descending digit loop and
initial `-G` producer option, but its simpler reset is not asserted equivalent.
TH05 first compares the current score with the resident high score using a
real three-state signed-word local: undecided1, copy-current2, keep-record0.
It processes digits7 down1, copying remaining current digits after deciding
the current score is higher, then clears each processed current digit. Digit0
is deliberately preserved. Finally it clears two genuine32-bit deltas and the
popup byte; it does not reset TH04-only unused/extend state.

The source includes the accepted complete128-byte resident and eight-byte
score union without modification. Real objects are current score DS3702,
delta3712, frame delta3716, resident far pointer41FC and popup byte1373.
The resident high-score field starts at offset68. No shortened resident view,
field alias, hand-picked machine register, emitted instruction or flag kernel
is introduced. The local comparison state is an ordinary integer and the
loop index keeps the maintained donor's logical `register int` declaration.

Native branches and the complete original return were checked independently
against locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The original behavior is corroborated by pinned ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05_main.asm`
`sub_10398`; those reference instruction statements are evidence, not an ASM
body imported into maintained source. Donor acceptance does not transfer.

This111-byte source is uncompiled and unaccepted. Its independent meaningful
negative changes the digit-loop condition from greater-than-zero to
greater-than-or-equal-to-zero, altering the real preserved score slot.
Two fresh whole-contribution raw/empty-ordered comparisons, OMF integrity and
the compiled negative remain required. The outside-only binder, target proof
and proposed entry are in `.analysis/hud-draw-reset/`.

## Accepted result

`main-hud-score-reset-a` passes both fresh deterministic whole111-byte raw
comparisons, the original empty ordered-fixup list and OMF checks. Its own
compiled digit-loop `>0`-to-`>=0` control was rejected. CPP, header and the
maintained binder are frozen accepted dependencies. This accepts the complete
reset function with its own control; no full-HUD or neighboring credit is
implied.

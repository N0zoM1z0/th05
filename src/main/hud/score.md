# Incremental score and record display

This semantic ASM candidate covers MAIN D4C0..D5C1, one complete 257-byte
contribution. HUD_SCORE_PUT begins at zero and the near score updater at 50.
There is one original EVEN NOP at 147, compared normally with zero credit.
The ordered MZ fixup is `[37]`, the true FAR GAIJI_PUTSA call. The following
00 byte at D5C1 is outside the contribution and remains unknown; accepted
laser code starts at D5C2. There is no CODE table or owned DATA/BSS.

Pinned ReC98 th05/scoreupd.asm includes the GAME5 branch of
th04/main/scoreupd.asm as a semantic donor. Independent native ASM-origin
review is required: modern source syntax alone is not origin evidence.
The reversed SI/DI restore in HUD drawing, shared unframed tally flow, AAA
decimal carry and explicit DF/IF-controlled record copy are native protocols,
not a failed compiler result promoted to ASM. Historical source, assembler
and exhaustive vendor ancestry remain unproved.

The complete eight-byte little-endian decimal score precedes the complete
eight-byte high score at DS:3702/370A. Their adjacency is part of the renderer
contract: it walks backward from high score into current score without resetting
SI. Digit zero is the continues-used slot. Rendering emits two eight-character
rows at (56,4) and (56,6), preserves the row terminator and deliberately returns
with caller SI/DI swapped. No register-preservation correction is introduced.

Pending/frame deltas are full DWORDs at DS:3712/3716. The updater retains the
native low-WORD writes to frame delta, the pending/32 step with minimum one,
the 6111 limit and preference for the larger prior frame delta. It converts
that frame delta using the already accepted five-WORD decimal factor table
at DS:1422. The nine-byte row at DS:142C is scratch decimal storage before
rendering. None of those foreign values or buffers are supplied or recounted.

AAA propagates carries through six score digits; the highest digit remains
unadjusted. The original overflow display quirk is preserved. Record comparison
and partial backward copy preserve the original equal-score and already-shown
paths, near popup callback at main_01:7459, and CLI/STD/REP MOVSB/CLD/STI sequence.
The source adds no input guard, score clipping, global clearing or IF restoration.
The zero-delta fast return does not touch drawing state. Foreign FAR renderer
and popup implementations remain outside this scope.

The symbol-only binder retains CS0AE1/DS209D and the real provider addresses.
It emits no instructions, state, divisor values, pixel data or stack. The near
popup is declared inside its genuine CODE context before reference. Existing
C++ source, resident types, accepted score reset and other HUD owners remain
unchanged. Source presence and exact acceptance remain separate.

Independent native/source/origin review:
`.analysis/hud-score-independent-origin-source-review.json`, SHA-256
`92190e9182375c1e03c07b4ae0754498577d72571a3a1cff83aea1f0df3e7f02`.
Candidate history e6294c2c explicitly identifies the TH04/TH05 micro-optimized
code and separate ASM translation unit; it corroborates the native inference
without proving historical source or transferring donor acceptance.

A native-only model passes 209 edge/generated cases against independent
integer/decimal arithmetic and glyph generation. It covers zero delta, prior
larger frame steps, pending DWORD extremes, ties with CX zero, already-shown
record copy, overflow/highest-byte wrap, exact popup assignment, two full rows,
stack cleanup and reversed SI/DI restoration. Record-copy writes are observed
with IF clear and DF set. The model tests frame inputs with high WORD zero;
it does not claim all DWORD frame states. The actual source still preserves
the full DWORD reads and native partial writes. The external renderer is
intercepted, not executed; its complete flag/register effects are not modeled.
Report: `.analysis/hud-score-native-semantic-check.json`, SHA-256
`e06d6862a21d683147b147bc94bebd22f6391c366f8115422b06d3ff63afa56b`.

Receipt `.analysis/asm-replays/main-hud-score-a/receipt.json`, SHA-256
`ccca871f11fa4cc1e5e334ee79a995e71ebb4b5f42f75aaff52954e599e87491`,
passes two fresh independent producers over all 257 bytes and ordered fixups
`[37]`. The own limit mutation from 6111 to 6110 retains the complete scope,
publics, frames and fixups and is rejected. Source inputs, actual assembler/
linker arguments and logs, OMF integrity, full LEDATA, MAP/group/public bounds
and MZ output are re-read by the unchanged ordinary ASM validator.
The original MAIN_01 GROUP/ASSUME context is set before the first producer;
no failed build, instruction/flag variant or first-producer rebuild occurs.
Existing installed execution proofs and unrelated accepted units are reused
after actual dependency checks.

The separate ownership decision in `config/reviewed_asm_families.json` adopts
only this complete family: 256 reviewed ASM instruction bytes and one compared,
uncredited EVEN byte. C/C++ counters, foreign DATA/providers, the trailing
unknown byte and whole-executable acceptance receive no credit.

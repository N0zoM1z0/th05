# TH05 MAINE: sound-board joystick probe and PSG input helper

The complete original MAINE `_TEXT` interval `[2E46,2E82)` consists of two
real near/far routines: `JS_START` (42 bytes including one alignment NOP)
and `SOUND_JOY` (18 bytes including one alignment NOP). `JS_START` scans the
PC-98 sound status port `0188h` 256 times at most. It enables the PSG mixer
for joystick use and records its result at DGROUP:022E; the near `SOUND_JOY`
selects PSG register 15 and reads joystick input via ports 0188h/018Ah.
These are the actual TH05-specific routines, not a reproduction of the
original Master SAJ-98 detection branch.

The maintained handwritten assembler has two full semantic function bodies,
with no target instruction dump. Only the original foreign `SOUND_I` and
`SOUND_O` routines are resolved from symbolic near-address labels at 2284
and 226E. The binder emits no foreign instructions or initialized data.
It preserves MAINE's real `_TEXT`/DGROUP layout, with DATA length 1D4Ah,
BSS length A800h, and original DGROUP linear base 10110h. These are original
uninitialized segment reservations, not invented global payloads or a fake
stack.

The focused source scope is 60 raw bytes: **58 instructions and two checked
alignment NOPs** at offsets 41 and 59. All original raw bytes and the empty
ordered MZ relocations must agree across two actual TASM/TLINK builds; a
native negative changes the 256-iteration poll count to 255. This is a
reviewed game-specific ASM owner, not compiler-generated C++ and not a claim
to the historically original source file.

## Accepted local replay

The source passed two independent pinned TASM 5.0/TLINK builds: **60/60
original bytes exact**, both original ordered MZ relocation lists empty, and
one compiled 256-to-255 poll-count mutation rejected. The exact receipt is
`.analysis/asm-replays/gpt-web-maine-joystick-start-a/receipt.json`.
Only this code contribution is accepted; the adjacent `JS_SENSE` and `SAJOUT`
functions remain separate unreviewed owners.

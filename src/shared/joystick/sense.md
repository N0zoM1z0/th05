# TH05 OP/MAINE: 21-byte joystick sense and legacy helper

The same 21 source-written bytes occur at OP `[2CBA,2CCF)` and MAINE
`[2E82,2E97)`. `JS_SENSE` (12 bytes, far) saves flags, disables interrupts,
selects the first joystick, calls the real near `SOUND_JOY` at the original
address, masks its six direction/button bits, restores flags, and returns
far. The subsequent `SAJOUT` (nine bytes, near) is a separate retained port
I/O helper, not part of the far function body. Both complete source functions
are present in the maintained semantic ASM, without source instruction dumps.

The original target has one **additional zero byte** after these functions:
OP `2CCF` and MAINE `2E97`. Neither belongs to either complete PROC and
neither is claimed. The two symbol-only binders reproduce the native code
address and true OP/MAINE DGROUP layout without foreign function bodies,
initialized DATA or artificial memory state. The historical authored source
may have used different macro spellings, so only the decoded original
machine code, ABI and source behavior are claimed exact here.

## Accepted local replays

Both OP and MAINE use the same shared semantic source file but separate
original-address symbol-only binders. Each of the two scoped 21-byte owners
passed independent two-producer TASM/TLINK comparison, with an empty original
MZ relocation stream and a rejected mutation of the six-bit joystick mask.
Receipts:
`.analysis/asm-replays/gpt-web-op-joystick-sense-verified-20261111/receipt.json`
and `.analysis/asm-replays/gpt-web-maine-joystick-sense-verified-20261111/receipt.json`.

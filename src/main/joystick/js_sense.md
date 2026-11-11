# MAIN far joystick state reader: 12 bytes

The original MAIN `[367A,3686)` `JS_SENSE` pushes flags, disables interrupts,
selects the first joystick, calls the already accepted foreign near
`SOUND_JOY` at `3668`, retains six direction/button bits, restores flags,
and returns far. Its original 12-byte body has **no trailing alignment byte**
and no MZ relocations. The byte at `3679` after `SOUND_JOY` remains unknown,
and the separate `SAJOUT` at `3686..368F` remains vendor owned; neither is
part of this new source contribution. The binder supplies symbols and
original MAIN segment extents only.

Focused receipt:
`.analysis/asm-replays/gpt-web-main-joystick-sense-verified-20261111/receipt.json`.
Two independent pinned TASM/TLINK producers match all original 12 bytes and
empty ordered relocations; compiling the six-bit input-mask negative is
correctly rejected.

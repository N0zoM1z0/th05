# MAIN joystick sound-board startup: 42 bytes

The maintained MAIN `JS_START` scans the PC-98 sound-board status port
`0188h` for at most 256 polls, then enables joystick input in PSG mixer
register 7 through the real external `SOUND_I`/`SOUND_O` functions. It writes
the resulting presence flag to original DGROUP:03D0 and returns far. The
complete native `[363E,3668)` contribution contains **41 instruction bytes
and one checked, uncredited EVEN NOP**.

This shares its original behavior with the independently accepted OP/MAINE
startup, but the MAIN near providers are genuinely at `247E` and `2494`
and the actual DATA frame is `209D0h`. The symbol-only binder reserves the
real MAIN CODE groups and the existing initialized DATA extent without
copying any foreign function, runtime state or initialized data. Source is
ordinary semantic ASM; the exact historical author source is not asserted.

Focused receipt:
`.analysis/asm-replays/gpt-web-main-joystick-start-verified-20261111/receipt.json`.
Two independent pinned TASM/TLINK producers match the original 42/42 bytes
and empty ordered relocations; compiling the 256-to-255 poll-count negative
is correctly rejected.

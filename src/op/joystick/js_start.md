# OP JS_START

`js_start.asm` is OP's sound-board joystick detection. It polls the PSG status
port `0188h` up to 256 times and returns AX = 0 if no board answers. Otherwise
it reads PSG register 7, keeps the low six bits, enables joystick input in the
upper bits, writes the mixer back, and stores the result in `js_bexist`.

This is a TH05-specific version of master.lib's joystick startup. Unlike
master.lib 0.23, it has no SAJ-98 detection path, so it is reconstructed on its
own rather than as an unchanged library procedure. `SOUND_I` and `SOUND_O` are
external near routines at `_TEXT` 20EA and 20D4.

The function ends in one word-alignment NOP after the RETF.

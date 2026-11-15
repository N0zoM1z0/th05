# MAINE sound-board joystick probe

`js_start.asm` is hand-written assembly for two TH05 routines that sit in
MAINE's `_TEXT` segment:

- `JS_START` polls the sound board status port `0188h` up to 256 times,
  enables the PSG mixer for joystick input, and stores the result at
  `DGROUP:022E`.
- `SOUND_JOY` selects PSG register 15 and reads the joystick state through
  ports `0188h`/`018Ah`.

Each routine ends with one alignment NOP (offsets 41 and 59). They call the
existing `SOUND_I`/`SOUND_O` helpers, which the symbol include resolves at
their original addresses `2284` and `226E`. The neighbouring `JS_SENSE` and
`SAJOUT` routines are not reconstructed yet.

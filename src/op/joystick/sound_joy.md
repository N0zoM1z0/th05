# OP SOUND_JOY

`sound_joy.asm` is the 18-byte near `SOUND_JOY` at `_TEXT` `[2CA8,2CBA)`. It
is a function of its own, not the tail of the preceding `draw_trapezoid`. It
selects PSG register 15 through `SOUND_O` (at 20D4) and reads the inverted
joystick bits from port 018Ah. The last byte is an `EVEN` alignment NOP.

`JS_SENSE` follows as a separate unit. The single zero byte at `2CCF` has no
known owner.

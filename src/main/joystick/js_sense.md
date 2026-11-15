# js_sense(): joystick state

MAIN `367A..3686`, 12 bytes of assembly. Saves the flags, disables
interrupts, selects the first joystick, calls `SOUND_JOY` (`3668`), keeps the
six direction and button bits, restores the flags and returns far. There is no
alignment byte after it; the byte at `3679` before it and master.lib's
`SAJOUT` after it belong to other code.

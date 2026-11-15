# Point popup digit conversion (`digits_register.asm`)

`pointnum_digits_set()` (ReC98 th05/main/pointnum/digits.asm) writes the five
decimal digits of a point value, least significant first, backwards from the
given pointer to the last digit, using the powers-of-ten table of the HUD
decimal code. It returns the popup width in AX: 8 pixels for every digit from
the highest nonzero one down, plus the units digit and the trailing zero that
the renderer always draws. 0 is 16 pixels wide, 65535 is 48.

It is kept as assembly because it reuses BP: after loading both parameters
through the frame, BP becomes the highest-nonzero-digit position, and each
power of ten needs a single DIV inside a `LOOP`. The plain C++ version
(`digits.cpp`) cannot express that; see `NOTES.md`. It preserves SI and BP,
pops 4 parameter bytes and ends with an `EVEN` alignment NOP.

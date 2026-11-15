# Point popup allocation (`add.asm`)

`pointnums_add_yellow` and `pointnums_add_white` are two entry points into one
procedure (ReC98 th05/main/pointnum/add.asm). Each advances its own byte ring
cursor (white: 200 slots, yellow: 80 slots placed after the white ones) and
writes the slot's flag and age before jumping into the shared body, which only
then sets up a BP frame. The white entry lies inside the yellow entry's
control flow. This shape is why it is kept as assembly rather than two C++
functions.

Both are near Pascal `(subpixel_t x, subpixel_t y, unsigned int points)` with
`RET 6`, and return the popup width in AX. The shared body sets flag 1 and
age 0, stores the current X/Y, converts the points with
`pointnum_digits_set()` into the record's digits and stores the returned width.
Previous Y, padding and the alive list are not touched. Cursors are not
validated. A final `EVEN` aligns the next function.

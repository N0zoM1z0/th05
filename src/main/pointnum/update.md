# Point popup update (`update.asm`, `update.cpp`)

`pointnums_update()` (ReC98 th04/main/pointnum/inv_upd.asm) treats every flag
other than free (0) and removal (2) as alive. Records marked for removal are
freed on the next call. For a live record it saves the previous Y, moves the
popup up by 0.5 pixels per frame once its age is 24 or more, marks it for
removal once Y reaches -4 pixels (the popup is off the top) or the
incremented byte age exceeds 36, and otherwise appends it to
`pointnums_alive`. The first survivor among the yellow slots (200-279) is
stored in `pointnum_first_yellow_alive`; the list always ends with 0.

`update.asm` is built: BX is the alive-list cursor, SI the record, DI the
remaining count, and the age is kept in CL.

`update.cpp` is the closest C++ version: 111 bytes, but the bytes differ.
What got it there from 126 bytes: assigning the new Y through the field
removes the stack local and frame, a signed countdown removes a redundant
zero test, the unsigned-byte flag comparison removes a sign extension, and
the unsigned yellow-range comparison restores the original branch. Remaining
differences: the compiler puts the list cursor in DI and the count in DX/CX,
subtracts 0.5 pixels as an ADD of a negative immediate with a reload of Y on
the false arm, and merges the two removal paths that the original keeps
separate. 18 register/ordering variants stayed at 111 bytes with the wrong
registers; 10 variants of the Y update and 12 compiler option combinations
gave 105-121 bytes without matching.

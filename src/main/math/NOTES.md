# Math helpers: notes

## Random ring

`randring` is a 256-byte table of master.lib `IRand()` results, followed
directly by the 16-bit cursor `randring_p`. `randring_fill()` fills it from
index 255 down to 0 and then clears the cursor.

- master.lib declares `IRand()` as `int pascal far`; storing the result into
  the byte array is what truncates it to AL. TH04's narrower byte-returning
  declaration does not produce TH05's code.
- The loop counter is a plain signed `register int`, which Borland puts in SI
  and which gives the original signed `>= 0` loop exit.

The readers (`randring_readers.asm`, see `randring_readers.md`) stay assembly.
`randring_next.cpp` records the closest plain C++ attempt.

## PlayfieldMotion::update_seg1/seg3

Both copies return the new point in AX:DX without going through memory. A
plain `return cur;` makes Borland build the 4-byte structure return in memory
(42 bytes instead of 32), so the built versions use pseudo-registers and omit
the return statement; see the comments in `motion_seg1_register.cpp`.

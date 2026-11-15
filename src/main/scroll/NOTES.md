# Scrolling: notes

## `scroll_driver()` (`driver.cpp`)

Straightforward C++ for the fraction accumulator compiles to 123 bytes instead
of 115: Borland reloads the fraction before computing the pixel advance,
copies the quotient between registers, and tests the result of
`scroll_line -= advance` with a separate memory read and comparison. The
original keeps the byte fraction in AL, clears AH to get the 0-15 pixel
advance in AX, and wraps on the sign flag of the subtraction itself; the
inline `SUB`/`JNS` pair reproduces that. The far `graph_scrollup()` call has
the function's only relocation.

## `scroll_tile_ring_update()` (`ring_update.cpp`)

The first plain C++ version compiled to 210 bytes instead of 204:

- `--tile_row_in_section < 0` became five instructions; the original is
  `DEC` + `JNS` on the variable, hence the inline assembly.
- Indexing `TILE_SECTION_OFFSETS[id]` scaled the ID by 2. TH05 STD files
  already store the IDs multiplied by 2, so the original uses the ID as a
  byte offset into the WORD table.

Its bindings file places only the preceding main_01 code before the compiled
object and everything else (rest of MAIN01, SHARED, MAIN03, DGROUP) after it.
A binder that put the MAIN03 range inside main_01 overflowed the 64 KiB group.

## `tile_ring_set_vo()` (`ring_set.cpp`)

Follows ReC98 th04/main/tile/set.cpp unchanged. Both divisions by 16 are
signed; an unsigned cast or a precomputed offset changes the code.

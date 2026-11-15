# Point popup invalidation (`invalidate.asm`, `invalidate.cpp`)

`pointnums_invalidate()` (ReC98 th04/main/pointnum/inv_upd.asm) sets the
invalidation box height to 8 once, then, for every record that is not free,
sets the box width to the popup width and calls
`tiles_invalidate_around(previous Y, current X)`. Popups move only vertically,
so that is where the popup was drawn last frame.

`invalidate.asm` is built. `invalidate.cpp` compiles to the same 44 bytes but
is not counted, since the assembly covers the function. Earlier C++ attempts:

| Source | Bytes | Result |
| --- | ---: | --- |
| Current X in an ordinary local (with or without `register`) | 52 | `ENTER`/`LEAVE` and a dead store to a stack slot |
| Both fields passed directly | 43 | Both arguments pushed from memory |
| Current X staged in `_AX` (current file) | 44 | Matches |

An unsigned loop counter adds a redundant zero test; the counter is signed.

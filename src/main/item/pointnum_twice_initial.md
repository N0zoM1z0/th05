# TH05 point-number doubling flag: original initialized game state

The original MAIN data at `[2227A,2227B)` (DGROUP `209D:18AA`) is the
mutable one-byte `pointnum_times_2`, initialized to zero. The pinned
ReC98 source `th04/main/pointnum/pointnum[data].asm` declares
`_pointnum_times_2 db 0` followed by `evendata`, and its companion
`pointnum.hpp` defines an ordinary one-byte boolean ABI. The accepted
TH05 `items_update` writes 1 while auto-pulling point items and resets
the byte to 0 afterward; the accepted Boss and Midboss score-bonus
routines write 0 to the same original DS offset before creating popups.

`pointnum_twice_initial.cpp` models this exact source object as an
ordinary mutable one-byte C++ flag. The focused native receipt
`.analysis/unit-replays/gpt-web-pointnum-doubling-initial-20261112-a/receipt.json`
contains two independent Turbo C++/TLINK producers matching the entire
one-byte initialized `_DATA` contribution and the empty original ordered
MZ relocation stream. The compiled false-to-true negative is rejected.

Only **one game-authored initialized DATA byte** is newly accepted.
The following `[2227B,2227C)` `EVEN` byte remains unknown, with no
padding or extra code credit.

# MAIN high-score display load: exact C++

`hiscore_load()` owns the complete 22-byte near C++ function at MAIN
`[C9A4,C9BA)` (CS `AE1`, DS `209D`). It first invokes the separately
reconstructed DOS score-section loader at `C882`, then copies eight digits
from the highest score record at DS `369F` into the current HUD high-score
buffer at DS `370A`. Each source digit has the `0xA0` gaiji offset removed.
The loop uses the original 16-bit `BX` array index and `CX`/`LOOP` hardware
interface. This routine contains no initialized DATA, padding, switch tables
or relocation sites. The NOP at `C9A3`, the preceding score-entry function,
and the player invalidator starting at `C9BA` are outside this claim.

Source `hiscore_load.cpp` reuses the existing full `scoredat_section_t` and
`score_lebcd_t` types. Its new declaration of `scoredat_load_for_cur()` in
the real `SCORE_IO_TEXT` segment deliberately avoids importing the unrelated
shared CODE segment into `main_01`. An earlier trial with `current.hpp`
attached the large foreign `SHARED` segment to `main_01`, exceeding 64 KiB;
that linker failure changed no accepted source. The final binder contains
only the actual score-state addresses and the outside-owner CODE placement.

Focused replay: `.analysis/unit-replays/gpt-web-main-hiscore-load-b/receipt.json`.
Two isolated Borland/TLINK producers agree on all 22 original bytes and the
empty original ordered fixup stream. The compiled negative changes the digit
count from eight to seven and is rejected. This is one new complete C++
function, not acceptance of the adjacent larger raw score insertion or player
movement code. Pinned ReC98 `th05/main/hiscore.cpp` supplies independent
high-level/legacy-register semantic context; literal historical source and
whole-executable identity remain unproved.

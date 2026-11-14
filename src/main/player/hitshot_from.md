# `hitshot_from()` — exact C++

`hitshot_from(Shot near *shot)` at MAIN `[13617,13683)` is a 108-byte
near-Pascal function with no relocations. It sits between the accepted C++
`shots_render()` and `shots_hittest()`. It marks the shot as removed and,
if the next ring slot of the 24 hit animations is free, starts one there:
pattern 28 for patnum base 20 (Reimu), otherwise 32. It copies the current and
previous positions and divides both velocity components by 6. The ring index
advances even when the slot is occupied.

`hitshot_from.cpp` is ordinary C++. TCC keeps the shot in DI and the slot in
SI, copies the two 4-byte points with 32-bit moves, and reuses BX=6 for both
divisions. The patnum test must compare an unsigned byte; a signed `char`
compare widens it with `CBW`. Two producers match all 108 bytes, and the
6→5 divisor negative is rejected. Receipt:
`.analysis/unit-replays/claude-hitshot-from-20261114f/receipt.json`.
This function replaces the earlier reviewed-ASM owner.

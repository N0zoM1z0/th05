# Original TH05 special bullet-group selector

The physical MAIN byte `[2228E,2228F)` (DS `209D:18BE`) is the mutable
one-byte `group_is_special`, explicitly declared in the original ReC98
`th05_main.asm` as `_group_is_special db 0` followed by `evendata`.
The following `[2228F,22290)` alignment byte remains unclaimed.

The complete accepted `spawn_groups.asm` writes the same original DS byte
as 1 before special-group dispatch and restores 0 afterward. Independently,
all three code paths in the accepted `spawn_raw.asm` consult the flag to
choose the ordinary versus special bullet initialization. This native
source/consumer evidence identifies its original semantics and width.

`group_special_initial.cpp` emits one ordinary mutable C++ byte in a
complete `_DATA` contribution. Its focused receipt
`.analysis/unit-replays/gpt-web-main-bullet-special-flag-20261112-a/receipt.json`
contains two independent Borland/TLINK producers with complete byte,
original MAP/OMF extent and empty ordered MZ relocation equality. The
compiled `group_is_special = 0` to `1` negative was rejected. This adds
**one game-authored initialized DATA byte**, without double-counting the
previously accepted ASM bullet operators.

# Mai and Yuki random flight

Natural C++ from pinned ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/boss/b4_both.cpp` and `th05/main/boss/impl.hpp`. It reuses the existing
complete 24-byte Boss state, subpixel geometry, byte direction enum and random
range helpers without changing accepted headers. The shared semantic macro
keeps the original random angle selection, directional reflection, deceleration,
clamps and final still frame. Both Bosses retain their separate direction state.

The original MAIN contribution is `[1785F,17957)`, 248 instruction bytes:
`flystep_random` is `[1785F,17937)` (216), and the two-Boss wrapper is
`[17937,17957)` (32). All observed branches target instruction starts. Both
functions are near Pascal in `main_03`, frame `1527`, cleaning six and two bytes.
There are no tables, padding or MZ fixups.

Original DS `209D` globals: Bosses at `5ABA` / `5AD2`, direction bytes at
`442C` / `442D`. Near callees are the three true random helpers at
`1529C` / `152AA` / `152C0` and vector helper at `152DA`. The scaffold binds
those foreign symbols and outside-owned holes only. Borland truncates the long
direction names to its actual 31-character external names; the binder uses
those actual EXTDEF identities, with no synthetic helper body or alias data.

`main-mai-yuki-flight-b` passes both independent cold producers and all raw
bytes. The compiled speed mutation from 6.25 to 6.0 changes actual flight
motion and is rejected. No foreign context or whole-game linkage is credited.

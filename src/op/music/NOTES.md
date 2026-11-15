# OP Music Room

`music.cpp` compiles all 15 Music Room functions (`BE79..C7D5`) and the Music
Room data as one translation unit, as the original was. An earlier split into a
prefix and a suffix unit matched the raw bytes, but the relocations of
`polygons_update_and_render()` and `musicroom_menu()` came out in the wrong
order. With one unit, the compiler emits the same 1020/1018/358-byte LEDATA
records as the original.

`nopoly_B_put()` (30 bytes at `BFF6`) is the one function that does not match
inside `music.cpp`. ReC98's `__memcpy__` version gives `33 FF` / `33 F6`
for `xor di,di` / `xor si,si`, where the original has `31 FF` / `31 F6`;
compiling through `tcc -S` and TASM gives the same result.
`nopoly_put_exact.cpp` writes the copy with register pseudo-variables and
explicit XORs, which matches when compiled directly with `tcc -c`.

Segment notes: TCC rejects `-zC`/`-zP` after the first token, so later segment
switches use `#pragma codeseg SEG op_01`. `music.hpp` declares
`musicroom_menu()` under `OP_MUSIC_TEXT` before it includes `menu.hpp`, so that
the first declaration gets the right segment.

The unit's data (DS `0FCE..2817`, 6217 bytes with 227 segment relocations)
includes `MUSIC_CHOICES[5][30]` and `MUSIC_FILES[5][30]`; the 81 unused slots
are implicit null pointers. `TRACK_COUNT` keeps internal (const) linkage. Its
BSS is DS `4D84..5060`, including the unused 104-byte array and the unused
`cmt_bg` planar pointers.

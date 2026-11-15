# OP High Score viewer

`view.cpp` holds the whole original translation unit (score recreation and
loading, digit/stage/place rendering, `regist_view_menu()` and the unlock-state
loader). It follows ReC98's TH04 sources with the TH05 branches selected.

`regist_view_menu()` lives in `regist_view_menu.inl` and is also compiled on
its own by `menu.cpp`. Compiled inside `view.cpp`, its raw bytes match, but
Borland splits the LEDATA record at offset 1023 of the unit, in the middle of
the menu, and the relocations come out in a different order. The standalone
`menu.cpp` produces the original order.

Because both translation units need the same filename strings, `files.cpp`
owns them as one `hiscore_filenames_t` object (DS `2818..284D`). The menu's own
four names start at an odd address inside that pool, so the menu unit cannot
own them by itself.

`scoredat_decode()` also decodes `hi2`, so the second score section must stay
even though TH05 never renders it. `hiscore_scoredat_load_for()` takes a signed
word (`playchar2`), not the byte-sized character enum.

`encode_exact.cpp` explains its own code-generation constraints.

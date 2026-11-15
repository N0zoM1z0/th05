# OP main menu

`menu.cpp` is one translation unit holding ReC98's `th05/op/start.cpp` and
`th04/op/m_main.cpp`. The `#pragma option -a2` in the middle is where ReC98's
second file starts; the launchers before it use byte-aligned data.

Build notes:

- `menu.cpp` and `strings.hpp` are UTF-8 and need the `cp932` source encoding
  in the unit manifest. All 26 descriptions match the original text, including
  the mix of fullwidth and ASCII spaces.
- `execl()` takes a four-byte `0UL` terminator in the large model.
- The unit owns its initialized data (flags, the 26 far `MENU_DESC` pointers and
  all strings) and the BSS at DS `[2DEC,2DF6)` (resident pointer, `in_option`,
  the menu callback and the two static input flags). A link scaffold must not
  add a STACK segment to DGROUP: doing so aligns and shifts this BSS by 84h.
- `menu_sel` and the `menu_sel_update_and_render()` parameters are `int8_t`,
  which mangles as `char`.

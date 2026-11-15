# ZUN Soft logo

The four functions follow ReC98's `th04/op/zunsoft.cpp` and `th04/zunsoft.asm`,
adjusted for TH05: input is reset and sensed with `input_reset_sense_held()` at
the start of each frame (TH04 resets before the loop and at the end of each
frame), and `pi_free()` is a far call.

`zunsoft_pyro_new()` receives four Pascal words: x, y, count and the sprite
byte (`RET 8`). Callers push x and y together as one dword, which is what
ReC98's `screen_point_t` parameter compiles to. Whether ZUN wrote one point or
two ints cannot be told from the binary.

`pyros`, `zunsoft_palette` and the six filename arrays belong to other units.
`filenames.cpp` (DS `0EEA..0F20`) is its own data unit; its link scaffold keeps
the rest of OP's data up to DS `2817` so that the test executable is valid.

master.lib's `MASTER_RET` expands to `far pascal` in the large model, so
`super_free()` and friends are Pascal even without `MASTER_CALL`.

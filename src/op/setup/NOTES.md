# OP first-launch setup

`setup.cpp` follows ReC98's `th04/op/m_setup.cpp`. ReC98's anonymous window
structure becomes `SetupWindow` here so that `setup.hpp` can declare `window`.

- `setup.cpp` and `strings.hpp` are UTF-8 and need the `cp932` source encoding.
- The unit starts at the odd OP address `B077` (group offset `0CE7`); nothing
  may be aligned in front of it.
- Its BSS is the 48-byte unused palette followed by `window` (DS `3F20..3F54`).
- The last SE help line is the same string as the last BGM help line and is
  pooled by the compiler.

# MAINE ending entry

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/end/entry.cpp`,
`th03/formats/cfg_impl.hpp` and the GAME=5 filename/ending interfaces.
This owner retains the full canonical `resident_t` and `cfg_t` declarations
without modifying accepted headers. Its local ten-byte CFG is read through
the real master.lib file API; the segment-only result becomes the real far
resident pointer. The original unchecked open/read behavior remains unchanged.

Canonical files are UTF-8. Use `source_encoding="cp932"` for the readable
`怪綺談1.dat` filename. The mutable ending-script filename remains a natural
static far pointer to `_ED00.TXT`; the ending and character fields select its
digits. There are no instruction emissions, target arrays, fake helpers,
optimization barriers or hand-coded stack operations. The large-model
`execl` terminator is the genuine four-byte `0UL`, not an artificial ABI shim.

The original decoded MAINE range is **`[A545,A695)`**, **336 bytes**:

| Function | Original half-open span | Bytes |
| --- | --- | ---: |
| `cfg_load_resident_ptr` | `A545..A576` | 49 |
| `game_exit_and_exec` | `A576..A5A4` | 46 |
| `end_animate` | `A5A4..A5FB` | 87 |
| `main` | `A5FB..A695` | 154 |

All 108 instructions decode contiguously through actual returns, including
the large-model `_main` far return. There are no CODE tables or padding. The
14 code segment fixups retain their original order. Private
`.analysis/maine-entry-boundary-review.json` records original calls, branches,
complete boundaries, 22 raw EXTDEF names and target identities.

Wrapper: `th05/maine_e.cpp`; segment `MAINE_E_TEXT`, group `group_01`, binary
context E. The group frame is **`0A54`**, load base **`A540`**; the unit begins
at group offset **5**. DGROUP is **`1011`**. Source-owned initialized DATA is
DGROUP **`[0090,00BB)`**, 43 bytes: the real four-byte script pointer and the
five filename literals `MIKO.CFG`, `_ED00.TXT`, `怪綺談1.dat`, `miko`, `op`.
Its sole pointer segment fixup is at DATA-relative 2 (DGROUP `0092`), with
original value `1011`. Source-owned BSS is the four-byte `_resident` far pointer
at DGROUP **`[1D6E,1D72)`**. These data scopes are not authored code credit.

`probes/units/maine_entry_bindings.asm` supplies only the genuine external
symbols. Its distinct origin holes surround whole compiler contributions;
it does not define `_resident` or any filename/pointer data and has no stack
allocation. Far helpers retain actual original **`E80`** frames and offsets,
which differ from calibration `E7F`. The true original staffroll destination
is **`E422`**, while calibration uses `E41D`; only the original operand is bound.
External data is `_random_seed` at DGROUP `0276` (4) and
`_mem_assign_paras` at `06CA` (2).

A natural negative control changes `frame_delay(100);` to `frame_delay(99);`,
altering the actual ending-entry pause. No build or source-current exact
acceptance is claimed by this preparation.

## Accepted focused replay

`maine-entry-a` passes both independent CP932-staged producers, all 336
instruction bytes / four functions, and 14 ordered CODE fixups. The actual
100-to-99 frame-delay negative changes output and is rejected. The owner DATA
and BSS observations add no extra progress credit.

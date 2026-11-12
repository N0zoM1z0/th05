# Initial score-registration page and name cursor

The original MAINE `[11631,11634)` has a complete three-byte initialized
state directly after the 51-byte selectable alphabet. Its actual consumers
identify `registration_page` at DS `1011:1521` as the byte flipped between
PC-98 display pages by `registration_frame()`. The following signed 16-bit
`entered_name_cursor` at DS `1011:1522` is used by the accepted registration
name, backspace, spawn and menu routines to index the eight glyph positions.
The canonical existing header declarations agree with those widths.

`initial_cursor_state.cpp` expresses the two original mutable zero initializers
in this physical order. The focused receipt
`.analysis/unit-replays/gpt-web-maine-registration-page-cursor-20261112-a/receipt.json`
contains two original Turbo C++/TLINK producers that match the complete
three-byte `_DATA` contribution and empty ordered MZ relocations. Changing
the cursor's initial value to one is rejected by the compiled negative.
The adjacent accepted score-file resources begin at `11634` and remain
separately owned. This adds three authored C++ initialized DATA bytes.

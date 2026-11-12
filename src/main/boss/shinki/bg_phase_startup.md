# Shinki B-type background initialization and shared B/C spin-line clock

Two physically separate and fully source-defined original MAIN near-DATA
objects now have natural Borland C initializers. Original
`_reference/ReC98/th05_main.asm` declares `_shinki_bg_type_b_initialized db 0`
at `[2235C,2235D)` and `_shinki_bg_spinline_frame dw 0` at
`[2235E,22360)`. The intervening single byte `[2235D,2235E)` belongs
to the original alignment, not either initializer, and remains UNKNOWN.
Both data owners use real global C public symbols and their independently
correct one-byte or two-byte types, not an artificial aggregate that
would count the padding.

The complete accepted `background.cpp` uses the B initialization flag to
build its original B-type linesets and adjust the existing particle pool
once before subsequent frames. The same B- and C-type update functions
increment the 16-bit `shinki_bg_spinline_frame` and use its modulo
period to alternate horizontal line motion. These are actual dynamic
state, not compiler switch tables, image assets, or unused zero-fill.

Both original native `_DATA` contributions were separately generated
from source, linked with only the original CODE frames and an outside
DGROUP prefix, and verified against the literal target bytes, full OMF
LEDATA/MAP boundaries, and empty original MZ fixups. Each has its own
compiled negative changing only the initial zero value to one:

- `.analysis/unit-replays/gpt-web-shinki-bg-b-initial-a/receipt.json`
- `.analysis/unit-replays/gpt-web-shinki-bg-spinline-clock-a/receipt.json`

The separately accepted two-byte particle-count sentinel and the
one-byte zoom-cycle counter remain distinct. The source-level C/C++
consumers will be selectively revalidated when their public declarations
are joined to these real data providers. These acceptances introduce
**three** new authored DATA bytes, without CODE double credit or a
whole-program cold replay.

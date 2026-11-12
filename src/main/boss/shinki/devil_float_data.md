# Stage-six Shinki Devil laser clock and floating direction C publics

Two separate native initialized-DATA objects originally declared by the
TH05 MAIN assembly have now been reconstructed from the genuine near C
types, not from a copied executable data dump.

The first, `shinki_devil_laser_grow_delay`, is an independently writable
**16-bit integer** at decoded original `[22428,2242A)` (DGROUP
`209D:1A58`). The complete native 802-byte `pattern_devil()` attack
reads and advances it before growing the real laser slots. Its original
`int` type and zero initializer produce an entire two-byte C DATA
contribution, not a synthetic local counter or a code instruction.

The second, `shinki_float_direction`, is the independent **one-byte**
zero-initialized floating-direction latch at `[2242A,2242B)` (DGROUP
`209D:1A5A`). The original `shinki_move_float()` leaf uses the byte to
switch between rising and falling motion when the signed vertical
velocity reaches its original bounds. Its width is one native C
unsigned byte, and the type does not require other state to be added.

The original source assembly has two distinct public symbols and a
following `evendata`. The following alignment byte and other original
zero state `[2242B,22434)` remain **unowned**. The previously accepted
Shinki two-by-two pattern callback table immediately precedes the new
objects at `[22420,22428)`; its original pointer words are not repeated.

Each DATA contribution was tested **separately** in the original MAIN
segment layout with two actual Borland C producers and its *own*
compiled negative mutating the initialized state from zero to one.
Both complete raw bytes, native OMF/MAP LEDATA extent, and empty original
ordered MZ fixup stream match exactly:

- `.analysis/unit-replays/gpt-web-shinki-devil-delay-data-a/receipt.json`
- `.analysis/unit-replays/gpt-web-shinki-float-direction-data-a/receipt.json`

These C DATA acceptances add **three** source-defined authored bytes,
not new CODE or padding. The independent large Boss/attack consumers
retain their original accepted code and will be selectively replayed
with the source-current C/C++ public declarations. No full cold replay
was executed.

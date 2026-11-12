# MAIN Boss random-flystep's actual default four-sided playfield clamp

The original decoded MAIN `[21E06,21E0E)` is one complete **eight-byte**
compiler-generated C++ initializer for the existing named object
`boss_flystep_random_clamp`. It is an `LRTB<Subpixel,Subpixel>` with
four real 16-bit Q12.4 gameplay coordinates, ordered **left, right,
top, bottom**:

| Source-level boundary | Pixel coordinate | Original subpixel word |
| --- | ---: | ---: |
| left | 32 | 0x0200 |
| right | 352 | 0x1600 |
| top | 24 | 0x0180 |
| bottom | 128 | 0x0800 |

The source constructs each member from a named pixel count shifted by
the canonical four-bit fixed-point scale. It uses the **full existing
C++ template type**, not an anonymous byte/word array or a synthetic
runtime initialization. `boss_flystep_random()` in the independently
accepted 398-byte movement family reads the four sides and clamps the
real moving Boss coordinates and next vertical direction. The complete
EX-Alice Boss controller later writes *different* arena boundaries to
the **same** global at the start of its fight; those dynamic updates
do not imply that the original default object was uninitialized.

The original address is DGROUP `209D:1436`. The symbol-only linker
scaffold contributes the authentic MAIN CODE group frames and only
the original outside `_DATA` prefix; the candidate's own eight bytes
are created by Turbo C++ from the initializer. The preceding ten
unknown zero bytes `[21DFC,21E06)` and the following independently
accepted `maine` filename at `[21E0E,21E14)` remain outside the
ownership claim, as do the original runtime movement instructions.

The focused native receipt
`.analysis/unit-replays/gpt-web-main-boss-default-clamp-a/receipt.json`
passes two independent pinned Borland C++ producers, full eight-byte
raw/OMF/LEDATA/MAP DATA equality, the original empty ordered MZ fixup
stream and a genuine compiled negative mutating the top edge from
24 to 25 pixels, which is rejected. No full cold replay or duplicate
CODE ownership follows from this single DATA contribution.

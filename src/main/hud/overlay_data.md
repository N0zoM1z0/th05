# Semantic overlay DATA bank

The accepted complete C DATA owner is original MAIN `[2237C,22420)`, 164
bytes, DS `209D:19AC..1A50`. Its 17 actual objects are modeled without filler:

| Relative offset | Complete field | Bytes |
| --- | --- | ---: |
| 0 | Fade union: input frame/output time | 1 |
| 1 | Boss-BGM frame | 1 |
| 2 | Popup frame | 1 |
| 4 | Text-effect buffer segment selector | 2 |
| 6 | Mutable `STAGE 1` selector string | 8 |
| 14 | Const `FINAL STAGE` selector string | 12 |
| 26 | Const `EXTRA STAGE` selector string | 12 |
| 38 | HiScore Entry fragment selectors | 9 |
| 47 | Extend fragment selectors | 6 |
| 53 | Bonus fragment selectors | 5 |
| 58 | Full PowerUp fragment selectors | 9 |
| 67 | DreamBonus Max fragment selectors | 11 |
| 78 | Five mutable far pointers to const popup strings | 20 |
| 98 | Dissolve-sprite index | 1 |
| 100 | Mutable far pointer to const blank-row text | 4 |
| 104 | Const `DEMO PLAY` selector string | 10 |
| 114 | Forty-eight ASCII spaces and NUL | 49 |

Natural word alignment leaves only offsets 3, 99 and 163. Original source
alignment directives and actual zeros independently confirm all three.
The C model has no padding members or byte-packing workaround: the compiler must
generate these bytes naturally. All 164 bytes participate in raw comparison,
while the three padding bytes receive no authored credit. The maximum proposed
semantic DATA credit is 161 bytes.

The source preserves the real one-byte fade union, byte frame/index state,
two-byte segment selector, one-byte gaiji enum, const/mutable arrays and six
true four-byte far pointers. Every field offset, total size and key type width
is asserted. `bb_txt_seg` is a segment selector, proved by original allocation
stores and direct `MOV DS,[19B0]` uses. It is not modeled as a false four-byte
pointer. The blank-row pointer retains the canonical unsigned Shift-JIS-byte
pointee, while popup pointers retain their const gaiji-byte pointees.

These gaiji arrays are encoded text, not font bitmap rows. The actual original
`GAIJI_PUTSA` at `1DBE..1E14` reads bytes until NUL and converts each selector
to TRAM character-code words. Independent original Master `GJPUTSA.ASM`
documents the same string API. Existing named bold-font definitions exactly
decode the four letter/digit captions. The five popup strings name consecutive
fragments of their respective messages; symbolic bases and fragment sequences
express those codepoints in source without copying font pixels or an opaque
hexadecimal payload.

The reference font's private 16-by-16 glyph grid visually corroborates the
popup fragment meanings. Its build command and converter define row-major
16-pixel cells. This is candidate semantic corroboration, not a claim of
independent original font-binary identity. The bitmap, preview and all font
pixels stay private and receive no acceptance or ownership exclusion here.

Original accepted HUD instructions independently write the stage digit at
DS `19B8`, index the far popup table at `19FA`, and use the far blank-row
pointer at `1A10`. The six exact original relative loader relocation sites
are `[102,96,92,88,84,80]`; all pointer values name actual fields in DS `209D`.
The static C initializer uses real self-field address constants, not numeric
addresses or linker-supplied pointer payload.

This is an explicit C reconstruction model grouping observed semantic objects,
not a claim about a historical struct. Its standalone API is
`hud_overlay_data.<field>`. It does not export old global-array aliases or
claim unchanged caller linkage. No accepted header/source has been modified;
any future caller integration needs its demonstrated affected closure.

The outside-only binder supplies true MAIN code frames and a DATA prefix
ending at `19AC`. It emits no instructions, text, pointer values, stack or
inside-owner holes. The C producer rejects accidental C++ mode and uses the
strict initialized semantic C DATA lane with zero functions. No constructor
or pixel initializer is involved. Its explicit word-aligned DATA model is
described below.

The first `main-hud-overlay-semantic-data-a` compiler attempt stopped before
its object was generated. Its one-byte selector check at frozen header line
54 passed; the first failure at line 59 was the complete struct-size check,
followed by all fourteen offsets beginning with the word at offset four.
An initial enum-width diagnosis was incorrect and is retracted. The temporary
byte-typedef variant b passed the selector check too and failed the identical
fifteen layout checks. Neither attempt ran a second producer or negative.
Both exact input sets and logs are retained privately. The first archive's
`failed-hud-overlay-c-enum` directory name records the superseded diagnosis;
its metadata now explicitly corrects it.

Variant c restored the original enum header and put `-a2` before all types.
Its actual diagnostic reduced to exactly three failures: the fade union was
rounded to two bytes, shifting the two following frame bytes to offsets two
and three. The enum-size check, complete bank size 164 and every remaining
field offset passed. No object, second producer or negative was produced.
Its exact three inputs and logs are preserved in the separate layout-c archive.

The approved variant d therefore preserves the original source options and
declares the original byte enum and fade union first. The header adds `-a2`
immediately before the bank struct, after the byte union. This expresses the
two independently proved type requirements: a one-byte fade union and a
word-aligned bank. Cached pinned TCC help documents `-aN` as alignment in N
bytes; active configuration contains only I/L paths and the producer arguments
contain no alignment option. No padding member, enum-size change, constness
change, other flag, field initializer or binder modification is used. This is
an explicit reconstruction DATA layout, not a historical-struct claim or a
CODE-parity experiment.

`main-hud-overlay-semantic-data-d` passes two fresh actual C producers,
complete gapless OMF DATA, the complete MAP scope, every raw byte, original
ordered relocations, all type assertions and input/tool/dependency identity.
Its own compiled mutation changes the first selector of `FINAL STAGE` from
F to E and is rejected. The164-byte extent contributes161 authored DATA
bytes; all three natural alignment zeros are compared and excluded. No font
bitmap, CODE, BSS or function credit is added.

Private native field/API evidence is
`.analysis/hud-overlay-data-boundary-review.json`; source/proposal evidence is
in `.analysis/hud-overlay-data-source-boundary-review.json` and the adjacent
unit proposal. Run `python3 .analysis/hud-overlay-data-review.py` and
`python3 .analysis/hud-overlay-data-source-review.py` for bounded native checks
without compiling or executing the game.

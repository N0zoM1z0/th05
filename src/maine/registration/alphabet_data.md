# Registration keyboard selector DATA

The complete accepted owner is the writable `uint8_t gALPHABET[3*17]` array
at original decoded MAINE `[115FE,11631)`, 51 bytes, DS `1011:14EE..1521`.
It includes three complete rows of 17 selectable glyphs. The source includes
the unchanged canonical glyph-ball header, preserving the existing global
name, byte storage, mutability, dimensions and all complete entity types.
No accepted input or caller is changed.

The original startup loads DX with `1011` and then DS with DX. This proves
the actual DATA frame; calibration's `1010:14EE` public is routing evidence
and must not shift the original target back sixteen bytes. Native accepted
cursor code at `BD09` indexes a byte at `[row*17+col+14EE]`, zero-extends it
and passes it to the real single-glyph `GAIJI_PUTCA` at `0000:121A`.
The original full display loop independently compares columns against 17
at `C3A1` and rows against three at `C3AA`.

The selected entries are:

- Row 0: A through Q.
- Row 1: R through Z, centered dot, full stop, musical notes, heart,
  exclamation, question mark, ellipsis and a duplicated Siddham HĀM glyph.
- Row 2: digits zero through nine; the point/dream/bullet kanji; left, right,
  space and End controls.

Named bold-font definitions establish normal GAME5 M/N ordering, letters and
digits. Existing gaiji definitions name the other symbols and navigation
controls. For three otherwise unnamed selectors, the private reference font
provides concrete semantic corroboration: the full stop is the named centered
dot shifted to the baseline; ellipsis is three such baseline dots; selector
`0F` is pixel-identical to the named Siddham HĀM glyph at `CC`. Source stores
only named selector constants, never those pixel rows or a font bitmap.
This does not claim independent original font-binary identity.

The control role is independently visible in original code at `C456..C463`,
which compares selected values against left `CE`, right `CF` and End `D5`.
The glyph-spawn consumer uses the same row-major byte table. This is a fixed
selection grid, not a NUL-terminated string: all 51 actual entries are nonzero.
The following zero belongs to the independent page byte at DS `1521`, read
and updated by the accepted frame helper. The preceding `EXED` object ends
at `14EE`. Both complete boundaries therefore have independent evidence.

The real start is even, so no preceding context, filler or alignment flag is
needed. There are no padding bytes or original relocation sites in the array.
The ordinary C++ definition retains mutable storage and expresses all 51
characters/commands by meaning, with no constructor or struct model.

The outside-only binder preserves original GROUP_01 and the real shared frame
`E80`, placing DATA at `1011` and reserving a prefix only through `14EE`.
It emits no alphabet bytes, internal holes, stack or instructions. The compiled
negative changes the first selectable A to B while retaining all 51 cells.

Two fresh producers in `maine-registration-alphabet-data-a` proved complete
51-byte gapless compiler DATA, the full MAP/PUBDEF scope, every raw byte,
the original empty ordered-fixup stream and deterministic normalized objects.
The compiled own character-selection mutation was rejected. Comparison uses
the pinned retained decoded view and its original relocation order; no decoder
was rerun and no packed-file equality is claimed.

Private review/proposals are
`.analysis/maine-registration-alphabet-data-boundary-review.json` and
`.analysis/maine-registration-alphabet-data-unit-proposal.json`. Run
`python3 .analysis/maine-registration-alphabet-data-review.py` for bounded
native checks without compiling or executing a decoder or game.

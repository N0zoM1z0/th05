# Staff text wipe

Current canonical bodies and producer choices are documented in
[full.md](full.md). Earlier standalone diagnostics and controls below remain
historical evidence; they are not relabelled as fresh compilation.

This accepted owner recovers the complete original MAINE helper at `DBE6..DD01`:
283 bytes, 112 instructions, near Pascal `RET 12`, and original ordered MZ
fixups **[261, 86, 53]**. It contains no NOP instructions, padding or CODE data
tables. `maine-staff-text-wipe-b` proves both fresh deterministic producers and the
compiled color1-to-2 control; see the focused result below.

The six actual signed word parameters are `left`, `top`, `width`, `height`,
`extent`, `direction`, pushed in Pascal order. Their callee BP offsets are
14, 12, 10, 8, 6 and 4. The return type stays the shared image-phase API's
`unsigned char`: AL zero means active, one means cleared, and two means covered.
Named status constants do not replace it with a bool or change the ABI.
Negative extent requests the real pending text clear at DS `1011:1746`.
Extent above `width / 16 + 7` fills the corresponding graphics rectangle and
returns covered. Intermediate states construct and draw a gaiji-selector row.

The original is ordinary bounded C++ logic with real graphics/text APIs and
one genuine hardware operation. `grcg_setcolor` is far Pascal at `0000:0F28`
with `RETF 4`; `grcg_byteboxfill_x` is at `0000:0C9E` with `RETF 8`;
`gaiji_putsa` is at `0000:125E` with `RETF 10`, including the genuine far
pointer to the local row. Borland's standard `outportb(0x7C, 0)` expresses the
original GRCG-off operation. No instruction templates or helper stand-ins are
used.

The local row contains text selector bytes, not a bitmap asset. `02h` selects
empty cells; `98h` is the first covered/fade selector, and subtracting extent
from `9Fh` selects the remaining intermediate cells. These are the actual
staff-font selector codes; they are not relabelled as the different common HUD
fade codes at `38h..3Fh`. The original gaiji string provider reads bytes until
NUL and writes two hardware text cells per code. Its primary API documents
80 halfwidth text columns. A 640-pixel row therefore holds 40 fullwidth,
16-pixel gaiji plus one terminator: the maintained buffer has 41 meaningful
bytes, not explicit filler. Two real word locals and the buffer need 45 bytes,
rounded to the observed even 46-byte stack frame. The physical original frame
could also hold a 42-byte array; this meaningful 41-byte model does not
authenticate the historical declaration. No padding member is added.

Native review matters here: `ReC98/th05_maine.asm` lines 4549–4704 are an older
candidate algorithm. They use an `ENTER 44` frame and one integer local, with
a horizontal clipping check inside the row-fill loop. The actual original
uses `ENTER 46`, two integer locals, top and width as live word values, a full
row terminator at `row[width]`, and the 80-column check in the final row-draw
loop. The maintained source follows those observed semantics. It fills the
row from either side according to signed direction, then draws it over the
inclusive converted height; it does not copy the stale reference's early break.

The independent header preserves the exact shared `staff_text_wipe()`
prototype and canonical pending-clear name agreed with both image-phase
owners. Their headers and all accepted inputs are unchanged. The binder has
only original external labels and holes outside the complete function; no
adjacent prefix, metadata or asset bytes receive credit. The compiled own
negative changes the actual covered-rectangle graphics color from one to two.
Private native review, hashes and the unit/control proposal are under
`.analysis/maine-staff-wipe/`. The focused result below records the actual fresh producers and full raw/ordered
acceptance.

## Focused result

`maine-staff-text-wipe-b` proves all283 bytes in two fresh deterministic
producers, the original ordered fixups and the rejected own graphics-color
1-to-2 mutation. The complete function has no NOPs, table or alignment credit.
The failed a receipt remains unchanged: only nine bytes within a twelve-byte
iteration-update sequence differed. Moving the three meaningful updates into
the `for` increment clause, `(i++, column += direction, extent--)`, restores
the original evaluation order without adding operations, type changes, register
hints or barriers. All other271 bytes already matched. The historical buffer
declaration remains unproved; the meaningful41-cell local receives ordinary
compiler stack alignment and needs no explicit padding field.

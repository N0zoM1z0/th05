# Sara and Mai/Yuki backdrop raster fillers

MAIN `[BEF4,BF60)` is a single 108-byte original-register source family
containing the complete near `sara_backdrop_colorfill()` at `BEF4..BF23`
and `mai_yuki_backdrop_colorfill()` at `BF24..BF5F`. The first function clears
four GRCG tile planes, uses the accepted `grcg_fill_playfield_rows` helper
at MAIN `10600`, then fills both playfield side columns while preserving DI.
The second uses two GRCG VRAM window segments (`A850` and `A968`) to draw
paired strips with twelve-DWORD batches in the upper band and four-DWORD
patterns below. It consumes the caller's EAX tile color, operates directly on
ES:DI and preserves DI as in the native procedure. No bitmap bank or new
state is defined.

The source reconstructs the explicit register and raster-geometry operations
from the pinned `ReC98/th05_main.asm` Sara/Mai-Yuki colorfill definitions and
its `GRCG_FILL_PLAYFIELD_ROWS` macro. The call into the separate row painter
and the two natural `EVEN` loop sites are kept symbolic, not copied as
machine-code arrays. The 108 compared bytes include NOPs at `BF23`, `BF2D`,
`BF49` and `BF5F`: four checked alignment bytes with zero ASM authorship
credit. The byte at `BEF3` and the following distinct renderer at `BF62`
are outside this family. All native MZ fixups are empty.

## Exact reviewed assembly acceptance

`.analysis/asm-replays/gpt-web-main-boss-backdrop-early-a/receipt.json`
records two independent native TASM32/TLINK producers. All 108 bytes,
the true empty relocation stream, complete CODE/OMF/MAP public boundaries
and the source negative altering the lower band by four bytes are verified.
The target-instruction/boundary record is
`.analysis/gpt-web-boss-backdrop-early-native-review.json`.

The explicitly reviewed ASM adoption contributes **104 instruction bytes**;
all four `EVEN` NOPs are checked with no credit. The accepted `10600` near
row painter is only referenced and is not double-counted.

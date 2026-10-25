# Point popup rendering and private mask writer

Two separate complete MAIN procedures reconstruct the point popup draw path:

| Scope | Complete bytes | Native NOP | Ordered MZ fixups |
| --- | ---: | ---: | --- |
| `@pointnum_put`, BE3A..BEA4 | 106 | 63 | empty |
| `POINTNUMS_RENDER`, E216..E28A | 116 | 115 | empty |

The worker's NOP comes from the row macro's EVEN; the driver's final NOP is
its own EVEN. All 222 bytes compare normally; two padding bytes receive zero
credit. The procedures are not adjacent in the original. The following
E28A circular-effects owner and BEA4 foreign C++ routine are excluded.

The real private interface takes AX=top, DX=left, CX=glyph and ES=VRAM.
The worker restores AX/SI/DI, preserves BP/DS/ES and returns DX advanced by
eight pixels, while BX/CX are scratch. The list driver keeps BP and DI live
across calls under that protocol. These interacting native register contracts,
conditional saves and hardware color sequence support inferred original
handwritten ASM. Modern ASM syntax or a failed compiler output is not the
basis. Literal historical source and original assembler remain unproved.

Pinned ReC98 th05/main/pointnum/render.asm, th04/main/pointnum/num_put.asm and
the shared sprite row macro supply candidate semantics only. A bounded
comparison with seven nearby primary Master sprite routines found different
multi-plane/dynamic-size/color-stream algorithms and no positive borrowed
body. That limited search does not rule out every historical adaptation.
Ordinary init/invalidate/update and digit conversion remain separate unknown
language/ownership questions; their proximity does not establish ASM origin.

## Full external types and behavior

The complete TH05 record is 16 bytes: flag0, age1, signed subpixel X2/Y4,
previous Y6, width8, five little-endian decimal digits10..14 and padding15.
There are 200 white plus 80 yellow records. The external list at DS:3FA6
has 281 complete WORD near pointers including its terminator; first-yellow
at DS:41D8 is one complete near pointer. Records start at DS:9F04. This source
does not create or initialize that pool, list, flag or width data.

The external raster bank at DS:084A is all 12 glyphs, eight horizontal shifts,
eight rows and two bytes per mask: 1536 bytes ending at DS:0E4A. The two
multiplier glyphs are retained in this full foreign geometry even though the
TH05 driver emits decimal digits and a trailing zero. No raster bytes are
supplied or granted authored/resource credit here.

The driver returns immediately for an empty pointer list without touching
hardware, ES or IF. A nonempty list sets ES=A800 and writes four white tile
bytes to port7E with interrupts disabled, then enables interrupts. At the
first-yellow pointer it writes FF/FF/00/FF under the same sequence. It assumes
the caller has already enabled the intended GRCG mode. Original IF is not
restored. Clear DF is required for the worker's LODSW; no CLD is added.

Valid widths are multiples of eight from16 to48, including the trailing zero.
Left is the signed pixel X plus32 minus half the width. Top uses the canonical
playfield top16 and half glyph height4, giving a12-pixel subpixel offset.
The true near Pascal scroll provider at DF28..DF50 consumes one WORD and
returns AX while preserving the live DX/SI/DI/BP/ES state. It remains a foreign
unknown owner, not an accepted contribution of either draw unit.

The worker chooses the glyph/shift rows and converts valid top/left to an
80-byte-row VRAM address. It skips zero words and writes a single byte when
the right mask byte is zero. At the bottom boundary it continues at row zero
without resetting the source cursor. No horizontal clipping, zero-width
guard, coordinate normalization or invalid-argument safety is introduced.

## Independent checks and preparation correction

Native/source-origin review:
`.analysis/pointnum-independent-native-origin-review.json`, SHA-256
`bf38de7d8ea882dc3791901d52b36aa3f9dda55201745cec3b75ca4ab08b198f`.
Initial prepared-source review:
`.analysis/pointnum-prepared-source-independent-review.json`, SHA-256
`2a82bdeebe02edb74eff331f8e9a1ec4605d0843119ed134736f08c778522c40`.

The initial draft incorrectly set PLAYFIELD_TOP to28. The first native-model
driver case failed before any assembler invocation. Canonical inherited
th02/main/playfld.hpp/.inc define16, so the shared new type include and
independent model were corrected from24 to12 pixels of top offset. The old
failed model and review are preserved; no original byte, source instruction
or flag is rewritten to hide the failure. Corrective independent addendum:
`.analysis/pointnum-prepared-source-geometry-correction-addendum.json`, SHA-256
`178db3959fbc2acbece73422b0fb6d484cbfaf81b42f6eadaff3f60d500f8fb0`.

The corrected native-only model passes530 cases, covering all12 glyphs and
eight shifts, zero-word/two-byte/single-byte mask writes, top/bottom ring cases, digit counts,
color transition, scroll states, stack and private register behavior. Its mask
bank is generated; it compares write addresses, widths, values and tile-port
events. It does not emulate colored GRCG framebuffer effects. It executes the
real foreign scroll provider without granting it ownership or acceptance.
Only valid widths and screen/ring coordinates are modeled. Report:
`.analysis/pointnum-native-semantic-check.json`, SHA-256
`dddeb25d28c37867a17592488237700d2fcdcb3ee51b939de9f7913600e72819`.

## Exact replay and explicit adoption

Both complete contributions pass the unchanged normal ASM gate: two fresh
independent producers, ordinary single CODE SEGDEF/LEDATA, empty DATA, original
CS/DGROUP/public boundaries, every raw byte and empty ordered MZ fixups.
Actual staged inputs, assembler/linker argv, successful logs, OMF checksums,
MAP and MZ outputs are re-read. Positives have deterministic normalized object
metadata and byte-identical MAP/whole MZ output; raw object hashes are retained.
Only dependency timestamps use existing metadata identity, never CODE or fixups.

Receipts:
`.analysis/asm-replays/main-pointnum-put-a/receipt.json`, SHA-256
`e7867e7b524e7e07aae8a5caeac52cff9f1621ad2cbfac072606ccdd3223c2f6`;
`.analysis/asm-replays/main-pointnum-render-a/receipt.json`, SHA-256
`55e0f7d34c104a1bf215e5d6984e1a279ef7fb5d245f04b058ec2b2ff039675b`.
The own worker mutation draws seven rows with the original eight-row asset
layout, changing only bytes42/47/59. The own driver mutation changes the
horizontal origin32 to31, changing only byte62. Both retain complete extents,
types, frames, publics, NOPs and relocation order and are rejected.

Independent actual-producer review:
`.analysis/pointnum-actual-replays-independent-review.json`, SHA-256
`1e1a833fc06a2bdee139aa76faf62c208663937ed20d702c9dd5e242284f179e`.
All six staged type includes have the corrected TOP16 identity. There is no
failed assembler producer, continuation, first rebuild or instruction/flag
matrix. The earlier geometry-model failure remains explicit. Installed tool
execution evidence and all unchanged accepted objects are reused after actual
dependency checks.

The separate decision in `config/reviewed_asm_families.json` adopts only the
two complete scopes: 220 reviewed ASM instruction bytes and two compared,
uncredited alignment bytes. It grants no C/C++, pool/list state, bitmap,
scroll-provider, neighboring-function or whole-executable credit. Model success,
exact replay and explicit ownership remain separate claims.

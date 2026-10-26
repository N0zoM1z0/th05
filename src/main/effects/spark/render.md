# Spark mask worker and batch C++ candidate

The complete private `@spark_render` at MAIN E020..E086 is 102 bytes:
101 instruction bytes and one final EVEN NOP at relative 101. The row-macro EVEN
emits zero bytes at relative 64. Every byte compares normally; padding receives
zero authored credit. Ordered MZ fixups are empty.

AX supplies pixel left, DX the VRAM ring top and CX the cel (masked to 7).
ES already selects the video plane. SI/DI are restored; BP/DS/ES and IF are
preserved. AX/DX/BX/CX are scratch. LODSW requires clear DF. The caller enables
GRCG mode and color. The worker skips zero words, writes one byte if the high
mask byte is zero, and otherwise writes a WORD, wrapping after row 399.
No invalid-coordinate handling or horizontal clipping is introduced.

The foreign bank at DS:14AA..18AA is 1024 bytes: eight horizontal shifts,
eight cels per shift, eight rows per cel, two bytes per row. This shift-major
layout differs from the point-popup glyph-major bank. No raster, pool or
other DATA/BSS storage is supplied or credited.

The private live-register protocol and shared semantic row macro support an
inference of original handwritten assembly for this worker. Pinned ReC98
th04/main/spark_render.asm and sprites/blit.inc supply candidate semantics.
A bounded review of seven nearby primary Master sprite routines and spark
identifiers found no positive borrowed body. Literal historical source,
original assembler and exhaustive vendor ancestry remain unproved.

The adjacent update E086..E0D2 and batch E0D2..E10E remain unknown. Accepted
lifecycle C++ E10E..E152 is unchanged. The full foreign batch pool consists of
64 records of 16 bytes at DS:5AEA: flag0, age1, current X2/Y4, previous X6/Y8,
velocity X10/Y12, angle14. Canonical playfield left 32/top 16 give half-glyph
coordinate offsets 28/12 pixels. Foreign scroll DF28..DF50 is near Pascal,
consumes one WORD and returns AX; raw color C204..C21E consumes AH and forces
IF enabled. Neither provider receives ownership or acceptance here.

## Natural batch C++ negative

render_candidate.cpp preserves the ordinary loop and uses register bridges
only for actual AH/ES/CL interfaces. The first invocation failed before an
object because the new header omitted screen_x_t; it now uses the existing
pixel_t alias and a two-byte assertion. One subsequent successful compilation
with the single inherited -k- profile generated 71 CODE bytes against 60 native
bytes. ENTER, temporary stack stores, a DX reload and LEAVE account for the
extent difference. Actual CL lifetime remains valid across the private call.

The first link also rejected the binding's uppercase raw-color spelling;
actual EXTDEF is @grcg_setcolor_direct_raw$qv. The binding is corrected to that
actual name without another compile/link: the 71-byte own SEGDEF already
proves the size failure. No second positive, control, receipt or acceptance
was produced. No instruction/flag search or ASM reclassification follows.

## Independent semantics and exact evidence

The native-only generated-bank model passes 464 cases: all shifts/cels,
high-cel aliases, zero/byte/WORD writes, bottom wrap, private stack/registers,
and foreign native batch color/scroll behavior. It checks port writes and
mask destinations, not colored GRCG framebuffer effects. Only valid screen
coordinates and clear DF are covered. Foreign execution grants zero credit.

Source origin review: `.analysis/spark-independent-native-origin-review.json`, SHA-256
`ac2b47e2761d03c5e5b208197de765d5f2536b95de1d643e41277ca5560a5d1a`.

Prepared source review: `.analysis/spark-prepared-worker-and-batch-source-review.json`, SHA-256
`760afa644759e7d30cca9b71f0b608a4e6d8641faeab9efc9130d37c256c1a44`.

Native model: `.analysis/spark-render-native-semantic-check.json`, SHA-256
`644360005afc5987d6a5a92c8f35f1214355beb9ddacb910c4161cd1298a2110`.

Batch cpp negative review: `.analysis/spark-batch-natural-first-independent-review.json`, SHA-256
`a115d9311c7786d32548e442013165084dc16d9ca5ecfd3918ee89d617cc9da8`.

## Complete replay and ownership

The unchanged normal ASM gate passes two fresh independent producers and the
own seven-row mutation. All 102 raw bytes, the complete ordinary CODE SEGDEF
and LEDATA, group/public placement and empty ordered relocations are checked.
The positives have identical normalized OMF, MAP and whole MZ output; raw OMF
hashes remain recorded. Existing normalization concerns dependency metadata
only, never instruction bytes or relocation order. DATA/BSS remain empty.
The negative keeps full extent, asset format, publics, frames and NOP 101;
its raw mismatch is rejected. Installed tool execution evidence is reused
after dependency identity checks. No worker producer failed or continued.

Receipt: `.analysis/asm-replays/main-spark-render-a/receipt.json`, SHA-256
`07396f7c5d98ebed0efee771542202fcf6b5cd9a02b6210cfc2e0c37e648080a`.

The separate decision in config/reviewed_asm_families.json adopts only this
complete worker: 101 reviewed ASM instruction bytes and one compared,
uncredited alignment byte. C/C++ counters, all 1024 raster bytes, the full
pool, batch/update, scroll/color providers and complete executable acceptance
receive no credit. Semantic model, exact replay and ownership remain distinct.

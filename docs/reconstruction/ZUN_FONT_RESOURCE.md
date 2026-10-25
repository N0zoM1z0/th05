# ZUN embedded font resource

Only the complete 8,192-byte bitmap at outer ZUN.COM file offsets
`2541..4541` is classified as `reviewed-embedded-font-bitmap`, with **zero
authored source credit**. This is neither compiler DATA acceptance nor original
ASM acceptance. The observation universe remains 319,268 bytes; its authored
denominator and percentage remain unreviewed.

The immutable target is the supplied candidate-local-attested 18,116-byte COM,
SHA-256 `5044ae03f7c0333f37d88ef34e244502f90d7314287f6f387c07569e4e0b120e`.
Independent pristine provenance remains unproved. Ranges below are original
outer file offsets, not the launcher's intermediate runtime addresses.

## Complete scope and native interpretation

The independently re-parsed directory places the complete `-G` child at
`2488..4541`, 8,377 bytes:

| Outer file range | Bytes | Observation / inventory policy |
| --- | ---: | --- |
| 2488..24D3 | 75 | Complete CG-RAM control code; stays unknown |
| 24D3..24D4 | 1 | Zero code/DATA alignment candidate; stays unknown |
| 24D4..2541 | 109 | Two DOS dollar-terminated messages; stay unknown |
| 2541..4541 | 8192 | Complete font bitmap; explicit resource classification |

The reader has no instruction NOP, relocation, embedded dispatcher or branch
destination inside the bitmap. It terminates with DOS AH=4Ch. Neither the
following zero nor the image is decoded as instructions.

Child COM offsets use `file - 2488 + 100`. SI starts at 1B9. DX begins at zero
and DL traverses all 256 values. Each glyph resets CX to 16 and BL to zero.
One LODSW reads two bytes per row: 256 glyphs times 16 rows times 2 bytes equals
8,192, ending exactly at child COM offset 21B9 without wrapping.

The glyph address is based on 5680, its low byte masked by 7F, and is sent
through ports A1/A3. Port A5 selects row-or-20 for the first column and the
unmodified row for the second; low/high font bytes go to port A9 respectively.
Mode 0B at port 68 precedes the loop and mode 0A follows it. These are bitmap
pixels programmed into character-generator RAM, not glyph selector text,
semantic tuning integers or compiler switch-table words.

LODSW requires DF clear; the child has no CLD of its own. The container parser
checks the dispatch entry's CLD and exact copy helper. The native gate also
decodes the complete dispatcher body and helper, rejects STD and unreviewed
dispatcher control flow, and checks the reader's loop/operand/port contracts.
This is static evidence under the recorded COM/DOS conventions, not observed
hardware execution or a new IF guarantee.

## Reference geometry and origin limits

The ignored reference BMP is uncompressed, bottom-up, one-bit 256 by 256 pixels.
Sixteen by sixteen tiles serialize in row-major glyph order, then top-to-bottom
16-pixel glyph rows. That complete transformation equals all native bitmap
bytes, SHA-256 `d78a4cc412d893f6f734c970145188e49b5b15319ba5a4ca2b5ef5dcf8e8d2d5`.
No inversion, normalization, missing row or padding substitution is used. No
image payload or target-byte initializer is added to maintained source.

The reference's generated bitmap include/build command corroborates geometry;
it does not authenticate historical font authorship, original source language
or a pristine distribution. The native consumer and complete physical scope
establish the resource role. No classification transfers to surrounding code,
messages, alignment, other children or vendor origins.

`-S` has positive Borland runtime/C++ evidence and cannot become original ASM.
`-O` matches a reference KAJA utility but still lacks the required independent
vendor provenance. The 311-byte `-M` assembly replay remains an origin inference.
All 9,924 other ZUN bytes stay unknown.

## Verification and explicit adoption

`config/font_resource.json` pins the target/view, complete child/reader/bitmap,
registered geometry, verifier/parser versions, private reference and independent
review. A separate `config/reviewed_font_resource.json` adopts only this bitmap.
Unsupported models, stale identities, partial bounds, duplicate/known overlaps
and any authored/instruction credit fail. Other classifications are unchanged.

Public CI checks metadata/adoption and the gapless inventory without private
files, explicitly reporting no native replay. The native command rehashes actual
inputs, re-parses the container, checks reader/DF semantics and compares every
BMP-derived byte:

```sh
python3 scripts/review_font_resource.py
python3 scripts/review_font_resource.py --native-check
python3 scripts/ownership.py --check
```

No compiler, assembler, Wine, Ghidra, download, decoder rerun or target execution
is required. Accepted source/producers and installed execution proofs are reused
unchanged. This is not two fresh source builds and cannot enter authored exact
ledgers or establish the global denominator.

Nine public tests cover synthetic BMP orientation/permutation, malformed formats,
metadata/decision mutations and overlap/credit rejection. Seven private negatives
reject changed glyph mask, column selector, row count, source pointer, output
width, dispatcher STD, and a changed reference pixel after repinning its identity.
Immediate controls use decoded operand locations. The preliminary report is
retained unmodified; two initially mislocated controls are superseded.

Private evidence:

- `.analysis/zun-layout-review/review.json`, SHA-256
  `18d20c98d2bf207e63da90c50d3fab4a3d1c6f704ccbe770e9eb1ce56de8b2eb`:
  independent complete container/native/resource review.
- `.analysis/font-resource/native-and-negative-review-b.json`, SHA-256
  `dd138c3a46d7274925bed800eecbc80a6ad74cc87f8f2c06e984cc0646300617`:
  root native check and seven final semantic negatives.
- `.analysis/zun-layout-review/gate-review-b.json`, SHA-256
  `ad273d2d0ed9f7c5fac6ca5b387103ba948c21059bfbbc182d44b56f3e382fce`:
  independent final gate review and negative readback.

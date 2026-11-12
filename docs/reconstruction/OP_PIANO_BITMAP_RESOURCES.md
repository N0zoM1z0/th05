# OP piano key masks and label font



The physical OP initialized-DATA region `[F9CE,FA32)` is now classified as
two complete, non-executable resources: 28 bytes at `0EFE:09EE` are four
identical seven-byte two-octave black-key row masks; the following 72 bytes
at `0EFE:0A0A` are nine 8×8 monochrome label glyphs (F, M, 1–5, S, G).
Their separate real MAP publics are `_PIANO_KEYS_BLACK` and
`_sPIANO_LABEL_FONT`. The already accepted key and label blitters address
those two exact DS offsets; no guessed identifier or zero-only match is
used.

The first resource is regenerated from the four seven-binary-byte `db`
rows in pinned ReC98 `th05/op/piano[data].asm`. The second is independently
read from the original 72×8/1bpp `th05/sprites/piano_l.bmp` using true
bottom-up BMP rows and 8-bit glyph tiles. That reconstruction equals the
retained `bmp2arr`-generated `.asp` source and the complete native OP bytes.
The original TASM `th05_op2.asm` ordinary `_DATA` LEDATA contains both
resources without FIXUPP; calibration MAP and original MZ match exactly,
including empty ordered relocations. This moves 100 bytes out of unknown,
classified as **28 sprite-bitmap plus 72 font-bitmap bytes**. It does not
award source-authored C/C++ credit or change the code-kernel receipts.

`python3 scripts/review_op_piano_resources.py --check` reruns the source,
BMP, object and original-image comparison. Separate proof and explicit
adoption live in `config/op_piano_resources.json` and
`config/reviewed_op_piano_resources.json`. The source asset provenance is
ReC98's candidate reconstruction, not a claim that its BMP was shipped
separately in the original game distribution.

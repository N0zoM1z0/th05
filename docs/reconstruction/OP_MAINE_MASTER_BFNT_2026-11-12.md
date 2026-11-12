# Master BFNT file signature: complete OP and MAINE initialized resources

OP `[F4BA,F4C0)` and MAINE `[102D4,102DA)` each contain the complete
six-byte `BFNT` file identifier (`42 46 4E 54 1A 00`). The archived Master
0.23 author source `BFNTID.ASM` explicitly declares the literal and NUL.
Both retained TASM `bfnt_id[data].asm` contributors reproduce its exact
source bytes in an ordinary `_DATA` LEDATA, and the real MAP publics anchor
both the `BFNT_ID` and `_BFNT_ID` aliases at `0EFE:04DA` and `1010:01C4`.

The original OP and MAINE MZ payloads and retained calibration products
match all six bytes at the exact source-backed positions, with empty ordered
loader fixups. A separate MAIN source owner already claims the independent
original six-byte BFNT marker at `[20D36,20D3C)` and is explicitly checked
but **not recredited** by this review.

`python3 scripts/review_op_maine_bfnt_id.py --check` proves the author
source, both native TASM objects, MAP exports, original MZ bytes and
the unchanged existing MAIN credit. Only **12 newly identified foreign
initialized DATA bytes** are adopted, with zero game-authored C++ credit.
The preceding nine unclassified OP bytes and the eight separate MAINE
pre-BFNT alignment bytes remain unknown.

# Original Master byte masks in OP and MAINE

Both decoded programs retain the complete eight-byte `BYTE_MASK` table from
Master 0.23's original `WORDMASK.ASM`, which MAIN has independently already
accepted. Each table is `FF 7F 3F 1F 0F 07 03 01`, a descending sequence
of low-bit masks used by the native Master graphics helpers.

| Program | Original load-module extent | DS offset | Retained TASM calibration |
| --- | --- | --- | --- |
| OP | `F800..F808` | `0EFE:0820` | `F800..F808` |
| MAINE | `1061A..10622` | `1011:050A` | `1060A..10612` |

The original eight bytes occur uniquely in each native decoded payload;
independently pinned MAP publics name `BYTE_MASK` at the two calibrated
DS offsets. A single complete ordinary `_DATA` LEDATA slice in each real
TASM object supplies all eight bytes. All compared original and calibrated
relocation streams are empty. The source is checked against the archived
Master author `WORDMASK.ASM` and retained native assembler copies.

Focused verification: `python3 scripts/review_master_byte_mask.py --check`.
The independent evidence and adoption files are
`config/master_byte_mask_op_maine_ownership.json` and
`config/reviewed_master_byte_mask_op_maine.json`.
Only these **16 bytes** are reclassified from unknown to Master third-party
initialized DATA, with **zero game-authored CODE/C++ credit**. No adjacent
hardware, screen, writable state or alignment range is claimed.

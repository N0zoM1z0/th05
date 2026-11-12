# Master BGM note/length tables: OP and MAINE

Both remaining original BGM note/duration tables have been identified from
Master 0.23's actual `B_DATA.ASM` source and retained native TASM objects.
MAIN's same 176-byte table was already accepted separately; this review
recovers exactly the two missing copies, **352 foreign DATA bytes** total.

| Program | Original load-module extent | Original DS offset | Calibration load-module extent |
| --- | --- | --- | --- |
| OP | `F844..F8F4` | `0EFE:0864` | `F844..F8F4` |
| MAINE | `10652..10702` | `1011:0542` | `10642..106F2` |

The table consists of 24 `note_dat` frequency/sentinel words followed by
64 `lcount` duration words, each exactly 16 bits. The `UNDF` source sentinel
is 100. Both native program images contain the complete source-generated
176 bytes exactly once. Their original ordered MZ relocation streams are
empty. Calibration MAP publics anchor `note_dat` and `lcount`; a single real
`_DATA` LEDATA from each TASM object covers the full table and matches both
linked calibration and native targets. Neither object requires inferred
padding, normalized bytes or fixup reordering.

`scripts/review_master_bgm_literal_data.py --check` independently replays the
archived Master source and both source-linked native comparisons. Its public
proof is `config/master_bgm_literal_op_maine_ownership.json`, with the narrow
adoption in `config/reviewed_master_bgm_literal_op_maine.json`. All 352 bytes
are classified as **third-party Master initialized DATA**, not game-authored
C++ and not CODE. The surrounding all-zero `glb SGLB <>` region has **no
corresponding ordinary OMF LEDATA writes** in the retained MAIN object and is
left unknown; its runtime storage cannot be relabeled as authored DATA just
because the linker materializes zeros. Remaining gaps before and after the
literal tables likewise stay unclassified.

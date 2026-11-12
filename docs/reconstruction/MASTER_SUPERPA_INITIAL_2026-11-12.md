# Master 0.23 sprite/superimpose initial state in MAIN, OP and MAINE

The archived author's original `SUPERPA.ASM` defines three *initialized*
16-bit variables: `super_buffer = 0`, `super_patnum = 0`, and
`super_charfree = 0`. These are Master library state for sprite pattern
allocation, count and release callback, not game-authored C++ data.

| Original program | Complete initialized words | Native calibration MAP |
| --- | --- | --- |
| MAIN | `210AC..210B2` | `209E:06EE..06F4` |
| OP | `F830..F836` | `0EFE:0850..0856` |
| MAINE | `1064A..10650` | `1010:053A..0540` |

Every source scope matches the author `SUPERPA.ASM`, retained TASM
`superpa[data].asm`, each actual `_DATA` LEDATA record, the original
calibration MAP publics and all bytes in each original MZ. The original
ordered relocation streams are empty.

The **preceding 32-byte pattern bank** is a separate `.DATA?`/uninitialized
allocation in the author's source (`super_patdata`, `super_patsize`) and is
**not claimed**. Nearby sound timer and palette ID states also have separate
owners or remain unknown. Focused verifier:
`python3 scripts/review_master_superpa_initial.py --check`. The evidence in
`config/reviewed_master_superpa_initial.json` adopts precisely **18 Master
initialized DATA bytes**, with zero new authored C/C++ credit.

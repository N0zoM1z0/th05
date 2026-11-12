# Master 0.23 memory allocator's initial DATA words

All three TH05 MZ programs contain the original four-word `MEM.ASM`
initializer: `mem_TopSeg=0`, `mem_MyOwn=0`, `mem_AllocID=0` and
`mem_Reserve=256` (4,096 reserved bytes). These are genuine, mutable
Master allocator state, not authored gameplay state.

| Program | Original eight-byte extent | Retained MAP `mem_TopSeg` public |
| --- | --- | --- |
| MAIN | `21084..2108C` | `209E:06C6` |
| OP | `F808..F810` | `0EFE:0828` |
| MAINE | `10622..1062A` | `1010:0512` |

The Master author's archived `MEM.ASM`, each native retained TASM source,
complete ordinary `_DATA` LEDATA, calibration and original decoded bytes all
match. The three original ordered relocation streams are empty.
`python3 scripts/review_master_mem_initial.py --check` checks those scopes.
Only these **24 bytes** moved out of unknown into third-party initialized DATA;
other adjacent memory/graphics/palette state remains unclaimed.

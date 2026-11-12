# Original Master 0.23 BGM global: three complete unwritten 108-byte structures

The 108-byte state following each source-verified 176-byte BGM
`note_dat`/`lcount` table is the actual `glb SGLB <>` Master 0.23 global.
The archived **original author** `B_DATA.ASM` exposes the label
`_bgm_glb`/`glb`, and its original `BGM.INC` specifies 23 SGLB members,
including 16-word track and tempo arrays and a four-byte timing word.
Every member is declared with `?` (uninitialized), and the assembled
structure is precisely 108 bytes. This is writable foreign runtime state,
not any kind of game-authored C++ initializer.

| Original program | Entire original reserved extent | Native MAP public |
| --- | --- | --- |
| MAIN | `21164..211D0` | `209E:07A6` |
| OP | `F8F4..F960` | `0EFE:0914` |
| MAINE | `10702..1076E` | `1010:05F2` |

For each program, the retained TASM object has a full ordinary `_DATA`
LEDATA ending exactly at the start of the global and another beginning
exactly 108 bytes later. **There is no source LEDATA initialization of any
of these 108 bytes**. Both the calibration and original MZ images
materialize the range as zeros, with no loader relocations. The original
Master author source and the retained source agree on the symbol and all
struct members. Previously accepted BGM note/duration arrays before these
scopes remain independently owned and receive no second byte credit.

`python3 scripts/review_master_bgm_global_reservations.py --check` validates
the original author source, native retained sources, complete structure
layout, true OMF unwritten gap, MAP publics and original MZ bytes.
The ownership inventory uses the narrowly validated
`reviewed-uninitialized-vendor-storage` category with zero source-authored
DATA/CODE, instruction and compiler credit. It classifies **324 previously
unknown source-backed storage bytes** without claiming original initialized
DATA or inventing BSS bytes beyond the observed decoded executable.

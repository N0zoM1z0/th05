# Original Master 0.23 machine, VRAM, joystick and palette DATA

The original author archive contains six complete initialized source
contributions between `file_sharingmode` and the PF buffer variables in
each of MAIN, OP and MAINE. The source/OMF/target chain verifies the following
fields in their original contiguous order:

| Source | Original author file | Source-written bytes | Meaning |
| --- | --- | ---: | --- |
| `GETMAC98` | `GETMAC98.ASM` | 10 | Nine Epson notebook IDs and explicit zero terminator |
| `GETMACAT` | `GETMACAT.ASM` | 22 | Two DOS/V device names and null far extension address |
| `GRP` | `GRP.ASM` | 11 | Five graphics VRAM words and byte mesh `55h` |
| *(excluded)* | native source alignment | 1 | Not declared as an initialized author value |
| `JS` | `JS.ASM` | 8 | Four zero joystick configuration words |
| `MACHINE` | `MACHINE.ASM` | 2 | Original zero machine-state word |
| `PAL` | `PAL.ASM` | 56 | Palette tone 100, exact 16 RGB triples, three zero state words |

Each program occupies a 110-byte contiguous physical interval: MAIN
`20D74..20DE2`, OP `F4F8..F566`, MAINE `10312..10380`. **109 bytes per
program** have source-backed DATA ownership. The separate zero at offset
`+43` remains *unknown* in all three, because the independent original
`GRP.ASM` writes the `55h` mesh but not the native `_DATA` alignment byte.

All six groups are reconstructed from numeric/string declarations in the
original archived Master source, then independently checked against the six
retained native TASM sources, complete ordinary OMF LEDATA, real MAP publics,
calibration and original MZ bytes. Every scoped ordered loader relocation
list is empty. The script `review_master_machine_graphics_palette.py --check`
repeats the source and toolchain comparison.

**Credit is deliberately deduplicated.** The complete **109-byte MAIN
copy was already accepted** under the prior `MAIN_MASTER_LITERAL_TABLES`
evidence, whose seven physical ranges are now cross-checked by the new
reviewer. Only OP and MAINE contribute **218 newly classified third-party
initialized DATA bytes**. No game-authored C++/instruction credit is awarded.
Evidence: `config/reviewed_master_machine_graphics_palette.json`.

# Master text-VRAM and VSYNC initialized DATA in three executables

Each of MAIN, OP and MAINE has a complete eight-byte Master 0.23 text-VRAM
initializer immediately followed by seven explicitly written VSYNC bytes.
The original author sources `TX.ASM` and `VS.ASM`, retained TASM sources,
object `_DATA` LEDATA, native MAP publics and original decoded MZ bytes agree.

| Program | TextVram (8 B) | vsync (7 B) | Unowned final byte |
| --- | --- | --- | --- |
| MAIN | `2106C..21074` | `21074..2107B` | `2107B` |
| OP | `F7F0..F7F8` | `F7F8..F7FF` | `F7FF` |
| MAINE | `1060A..10612` | `10612..10619` | `10619` |

The four text fields are the segment-relative text address zero, text VRAM
segment `A000h`, width 80 and visible flag 1. The VSYNC fields are one null
far callback, a zero delay word and a zero old-mask byte. All three original
MZ relocation streams are empty within these initialized words.

The final source-side byte emitted after `EVEN` is zero in each retained TASM
calibration, but **90h in the original game**. Its provenance is unresolved;
it remains unknown instead of being credited as initialized DATA or padding.

`python3 scripts/review_master_tx_vs.py --check` verifies the 45 bytes against
original Master author sources, all three complete native TASM LEDATA slices,
MAP anchors, calibration and original payloads. Evidence is stored in
`config/reviewed_master_tx_vs.json` with zero game-authored C++ credit.

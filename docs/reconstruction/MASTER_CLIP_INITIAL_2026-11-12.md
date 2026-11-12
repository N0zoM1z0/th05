# Master 0.23: original eight-word clipping state in three executables

MAIN, OP and MAINE each contain the complete original 16-byte clipping
initializer from the archived author's `CLIP.ASM`, separately retained as
`libs/master.lib/clip[data].asm`. The eight 16-bit words are `ClipXL=0`,
`ClipXW=639`, `ClipXR=639`, `ClipYT=0`, `ClipYH=399`, `ClipYB=399`,
`ClipYT_seg=A800h` and `ClipYB_adr=399*80`. The linked native programs
retain the original little-endian values and the Master clip/render functions
read these exact fields.

| Executable | Original load-module bytes | Calibration MAP public |
| --- | --- | --- |
| MAIN | `20D3C..20D4C` | `209E:037E` |
| OP | `F4C0..F4D0` | `0EFE:04E0` |
| MAINE | `102DA..102EA` | `1010:01CA` |

Each native calibration TASM object contains one complete, ordinary
16-byte `_DATA` LEDATA for this table, matching the original archive's
source definitions and the exact program payload. All three original
ordered MZ relocation streams are empty. The source-derived sequence occurs
uniquely at each original offset.

Focused verification:
`python3 scripts/review_master_clip_data.py --check`. The evidence and
narrow adoption reside in `config/reviewed_master_clip_data.json`.
Exactly **48 previously unknown bytes** now have third-party Master
initialized DATA ownership, without new game-authored C/C++ credit.

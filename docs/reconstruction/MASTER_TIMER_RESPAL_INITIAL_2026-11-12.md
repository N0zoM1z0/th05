# Source-backed BGM timer divider and OP palette resource ID

The original Master 0.23 author's `B_TMHOOK.ASM` contains the independent
`intdiv dw 1` default. The retained actual TASM module
`bgm_timerhook[data].asm` preserves it. Its two-byte `_DATA` contribution
matches the original MAP, OMF LEDATA and native MZ images of all three
executables, with no original loader relocation.

| Program | Source-written `intdiv` extent | Native calibration MAP |
| --- | --- | --- |
| MAIN | `210B2..210B4` | `209E:06F4` |
| OP | `F842..F844` | `0EFE:0862` |
| MAINE | `10650..10652` | `1010:0540` |

OP also includes a ten-byte `ResPalID = 'pal98 grb', 0` at `F836..F840`,
explicitly defined in retained `respal_exist[data].asm` and identified by
its separate MAP public `0EFE:0856`. Its entire ordinary TASM `_DATA`
LEDATA and original MZ payload match, with empty fixups. Unlike `intdiv`,
this palette-ID owner is proven from retained ReC98 native source and
actual toolchain outputs, **not** an independently pinned Master author
archive. The intervening two OP bytes `FF FF` at `F840..F842` remain
**unknown**; they are not included in either source-owned span.

The focused verifier
`python3 scripts/review_master_timer_and_respal.py --check` checks exact
source constants, MAP/OMF positions, native and calibrated bytes, no
relocations and original target identity. Only **16 foreign initialized
DATA bytes** are newly classified, with zero game-authored C/C++ credit.

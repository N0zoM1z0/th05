# Master file handle and sharing defaults in three EXEs

All three executable DATA segments contain the same consecutive mutable file
initializers: `file_BufferSize = 0`, `file_Handle = -1` and
`file_sharingmode = 0`. The **first four bytes** are explicitly sourced to
the original archived Master 0.23 author `FIL.ASM`. The **last two** are
source-verified from retained ReC98 `dos_ropen[data].asm` (not independently
present in the frozen original author archive). Both sources have real native
TASM `_DATA` LEDATA and linked MAP publics, complete original/calibration
byte identity and empty ordered MZ fixups.

| Executable | FIL 4 bytes | DOS_ROPEN sharing 2 bytes |
| --- | --- | --- |
| MAIN | `20D6E..20D72` | `20D72..20D74` |
| OP | `F4F2..F4F6` | `F4F6..F4F8` |
| MAINE | `1030C..10310` | `10310..10312` |

Focused verifier:
`python3 scripts/review_master_file_initial.py --check`. The narrow proof
is in `config/reviewed_master_file_initial.json`. These **18 foreign DATA
bytes** are no longer unknown. No game-authored C++ byte is awarded; adjacent
machine-detection and library DATA remain separately classified or unknown.

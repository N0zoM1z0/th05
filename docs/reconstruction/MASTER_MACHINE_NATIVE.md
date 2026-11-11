# Source-exact Master machine detection and buffered I/O

Seven complete original Master 0.23 procedures in MAIN are now source-linked:
**780 previously unknown CODE bytes**.

| Procedure | MAIN extent | Bytes |
| --- | --- | ---: |
| `PALETTE_BLACK_IN` / `PALETTE_BLACK_OUT` | `0600..0644`, `0644..0682` | 68 + 62 |
| `BOPENR` / `BREAD` | `0682..06D6`, `06D6..0706` | 84 + 48 |
| `GET_MACHINE_98` | `1B4A..1BC8` | 126 |
| `GET_MACHINE_AT` | `1BC8..1D1E` | 342 |
| `GET_MACHINE_DOSBOX` | `1D1E..1D50` | 50 |

The [bounded source reviewer](../../scripts/review_master_machine.py) compares
each entire procedure against the independent original Master ASM archive and
the pinned actual TASM input. The differences are explicit 16-bit assembler
spellings: `NOPCALL`, typed `PUSH`/byte fields, and three branch-range
trampolines in the AT detector. The two maintained raw `E9` near jumps
in the machine detectors are checked to land at the genuine, separately
bounded `GET_MACHINE_DOSBOX` entry (`1D1E`), not accepted as arbitrary bytes.

The actual original TASM OMF LEDATA and ordered FIXUPP records reconstruct
all seven full native scopes without exceptions; calibration/original byte
ranges and ordered MZ relocations match. The [proof](../../config/master_machine_ownership.json)
and [adoption](../../config/reviewed_master_machine.json) contain the
source and complete CODE hashes.

```sh
python3 scripts/review_master_machine.py --check
python3 scripts/ownership.py --check
```

This restores third-party Master ASM only, not authored C++ or adjacent
padding. The whole-game replay was not run.

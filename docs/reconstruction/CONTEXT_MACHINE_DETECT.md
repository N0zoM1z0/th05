# OP/MAINE: original Master machine-detection source, 868 bytes

The complete original machine-detection chain in both decoded executables is
now source-linked to the authentic Master 0.23 assembler archive. Four whole
procedures per executable occupy **434 bytes each**:

| Function | OP CODE | MAINE CODE | Bytes per executable |
| --- | --- | --- | ---: |
| `GET_MACHINE_AT` | `1016..116C` | `1068..11BE` | 342 |
| `GET_MACHINE_DOSBOX` | `116C..119E` | `11BE..11F0` | 50 |
| `CHECK_MACHINE_FMR` | `119E..11AC` | `11F0..11FE` | 14 |
| `GET_MACHINE` | `11AC..11C8` | `11FE..121A` | 28 |

The unchanged `GETMACDB.ASM` and `GETMACFM.ASM` authored procedure bodies
match the actual native TASM sources directly. The two larger adapted
functions have a small, explicit source transformation:

- `GET_MACHINE_AT` changes the FM-R constant name, expands three out-of-range
  conditional branches to inverted conditions followed by a direct jump,
  and spells the final near jump into the adjacent DOSBOX routine as native
  `DB E9,01,00`. That byte directive is present in the retained compiler
  input; it is a linker-context compatibility workaround, **not** recovered
  game-authored C++ or an instruction copied into a new source file.
- `GET_MACHINE` changes the FM-R constant name and uses an inverted condition,
  two native NOPs and a direct jump for the original `JE GET_MACHINE_98`.
  These are the exact original TH05 compiler inputs rather than source
  assertions about how the unmodified upstream assembler would lower them.

Apart from these listed transformations, every normalized authored source
statement is identical to the retained native source. All eight complete
contributions are uniquely anchored by their real original exported publics.
The pinned OP/MAINE TASM objects provide full LEDATA and **14 ordered OMF
fixup actions** across both contexts. Rebinding them to their original
segments reproduces every original CODE byte and the empty ordered MZ
relocation streams; the independent calibration images match as well.

The source-linked evidence is
[`config/context_machine_detect.json`](../../config/context_machine_detect.json),
with explicit ownership in
[`config/reviewed_context_machine_detect.json`](../../config/reviewed_context_machine_detect.json).
Recheck this bounded region with
`python3 scripts/review_context_machine_detect.py --check`. The public CI
checks structural source/decision identity without invoking the original
binary or Wine. All **868 bytes are Master-derived foreign CODE**, not
newly credited game-authored bytes.

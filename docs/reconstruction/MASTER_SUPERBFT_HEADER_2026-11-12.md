# Master SUPERBFT: 32-byte BFNT header reserve in all three EXEs

The unexplained 32-byte zero-filled interval between the initialized Master
MEM and SUPERPA state is a single native BFNT header, not compiler padding
or written-zero initialized DATA. The original archived Master `SUPERBFT.ASM`
contains `header bfnt_header <>`. Its archived `SUPER.INC` defines the
32-byte BFNT header with 12 fields: every field is an assembler `?`,
including the two variable-length byte arrays and the far timestamp word.
The retained ReC98 native module uses the same declaration.

| Original executable | Exact original unwritten header | Calibrated local `_DATA` gap |
| --- | --- | --- |
| MAIN | `2108C..210AC` | `063E..065E` |
| OP | `F810..F830` | `035E..037E` |
| MAINE | `1062A..1064A` | `045E..047E` |

Each genuine TASM object has complete `_DATA` LEDATA records ending and
starting at these boundaries, with **no initialized bytes** within the
32-byte header. All three original target views materialize the entire
header as zeros, with no original relocation sites; the retained calibration
MZs match. The source header's 32-byte structure size comes from the archived
Master author, not from a guessed binary array length.

`python3 scripts/review_master_superbfnt_header.py --check` verifies the
original source, retained header and TASM, complete OMF gap and target identity.
The precise proof in `config/reviewed_master_superbfnt_header.json` classifies
**96 previously unknown bytes** as zero-credit uninitialized foreign storage.
It does not award game-authored C/C++ initialized DATA or infer authorship for
any adjacent alignment byte.

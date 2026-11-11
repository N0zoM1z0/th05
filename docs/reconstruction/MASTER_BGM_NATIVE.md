# Original Master BGM source recovery in TH05 MAIN

Nine complete sound and music driver procedures from the original Master
0.23 library now have source-linked native ownership of **1,614 CODE
bytes** in TH05 MAIN. Each original function is reconstructed from the
real TASM object and its original symbol fixups, not instruction bytes
copied from the original game.

| Complete function | Original MAIN range | CODE bytes | Original OMF FIXUPP |
| --- | --- | ---: | ---: |
| `_BGM_MGET` | `36E8..3812` | 298 | 15 |
| `_BGM_TIMER_INIT` | `3952..3996` | 68 | 9 |
| `_BGM_PINIT` | `39C0..39FE` | 62 | 2 |
| `_BGM_TIMERHOOK` | `39FE..3AAE` | 176 | 19 |
| `_BGM_PLAY` | `3B16..3C44` | 302 | 30 |
| `BGM_SOUND` | `3C44..3C8E` | 74 | 5 |
| `_BGM_EFFECT_SOUND` | `3C8E..3D06` | 120 | 7 |
| `BGM_INIT` | `3D4E..3EF2` | 420 | 30 |
| `BGM_FINISH` | `3EF2..3F50` | 94 | 6 |

The [native verifier](../../scripts/review_master_bgm.py) checks the
original author's Master 0.23 ASM archive, its active TASM function
boundaries, and the actual source-built OMF module. All complete
instruction/operand streams must match after only explicit adaptations
to the original assembly notation: `@@` label scoping, `b_init_` /
`b_e_snd_` local label namespaces, spelling a typed `spart` structure
member, one unused `pcat:` label, and an explicit `word ptr`
annotation on the original 16-bit `push`.

The maintained port sometimes spells an original Master `CALL` as
`NOP; CALL` to retain the original linker footprint. This is a
documented source adaptation, **not** an exemption from the raw-byte
oracle. The linked original opcode, NOP, target and complete original
function boundary are still compared byte for byte. No game C++
authorship is claimed from that adaptation.

## Genuine original relocation model

All original near OMF FIXUPP sites are reconstructed from the actual
`_TEXT`/`_DATA`/`_BSS` symbols. The native C0 startup independently
establishes the original initialized DATA and BSS offsets as 18 bytes
lower than in the genuine saved TASM calibration. Three original
segment-word FIXUPP records include the original DGROUP frame
`209Dh` versus calibration `209Eh`, or the unchanged `_TEXT` segment.
These exact original MZ relocation sites and their **original order**
are checked, not sorted or inferred from the target bytes.

The verifier reconstructs original and calibrated CODE independently
from the same source OMF. It checks complete raw bytes, unique
whole-function occurrences, and ordered original relocations. Its
[evidence](../../config/master_bgm_ownership.json) and
[explicit decision](../../config/reviewed_master_bgm.json) grant only
the nine complete member extents. Unaccepted neighboring functions,
including the larger `BGM_READ_SDATA` loader, remain unknown until
their own source/macro-context review.

```sh
python3 scripts/review_master_bgm.py --check
python3 scripts/review_master_bgm.py --structural-check
python3 scripts/ownership.py --check
```

These are **third-party native ASM CODE** bytes, not the number of
decoded instructions, and contribute **zero game-authored C++ bytes**.
No full cold replay, invented source state, or new denominator is
involved.

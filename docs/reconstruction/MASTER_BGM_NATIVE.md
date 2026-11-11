# Original Master BGM source recovery in TH05 MAIN

Seventeen complete sound and music driver procedures from the original Master
0.23 library now have source-linked native ownership of **2,266 CODE
bytes** in TH05 MAIN. Each original function is reconstructed from the
real TASM object and its original symbol fixups, not instruction bytes
copied from the original game.

| Complete function | Original MAIN range | CODE bytes | Original OMF FIXUPP |
| --- | --- | ---: | ---: |
| `_BGM_BELL_ORG` | `3690..36C0` | 48 | 1 |
| `_BGM_BELL_ORG` | `3690..36C0` | 48 | 1 |
| `BGM_GETNUMBER` (private) | `36C0..36E8` | 40 | 0 |
| `_BGM_MGET` | `36E8..3812` | 298 | 15 |
| `BGM_READ_SDATA` | `3812..3952` | 320 | 17 |
| `BGM_READ_SDATA` | `3812..3952` | 320 | 17 |
| `_BGM_TIMER_INIT` | `3952..3996` | 68 | 9 |
| `_BGM_TIMER_FINISH` | `3996..39C0` | 42 | 4 |
| `_BGM_TIMER_FINISH` | `3996..39C0` | 42 | 4 |
| `_BGM_PINIT` | `39C0..39FE` | 62 | 2 |
| `_BGM_TIMERHOOK` | `39FE..3AAE` | 176 | 19 |
| `BGM_BELL` (private) | `3AAE..3B16` | 104 | 2 |
| `_BGM_PLAY` | `3B16..3C44` | 302 | 30 |
| `BGM_SOUND` | `3C44..3C8E` | 74 | 5 |
| `_BGM_EFFECT_SOUND` | `3C8E..3D06` | 120 | 7 |
| `BGM_STOP_PLAY` | `3D06..3D20` | 26 | 2 |
| `BGM_SET_TEMPO` | `3D20..3D4E` | 46 | 4 |
| `BGM_STOP_PLAY` | `3D06..3D20` | 26 | 2 |
| `BGM_SET_TEMPO` | `3D20..3D4E` | 46 | 4 |
| `BGM_INIT` | `3D4E..3EF2` | 420 | 30 |
| `BGM_FINISH` | `3EF2..3F50` | 94 | 6 |
| `BGM_STOP_SOUND` | `3F50..3F6A` | 26 | 2 |
| `BGM_STOP_SOUND` | `3F50..3F6A` | 26 | 2 |

The [native verifier](../../scripts/review_master_bgm.py) checks the
original author's Master 0.23 ASM archive, its active TASM function
boundaries, and the actual source-built OMF module. All complete
instruction/operand streams must match after only explicit adaptations
to the original assembly notation: `@@` label scoping, `b_init_` /
`b_e_snd_` / `b_b_org_` local label namespaces, spelling a typed `spart` structure
member, two unused source-only machine labels, and explicit `word ptr`
annotations on 16-bit `push` instructions. The 320-byte `BGM_READ_SDATA`
loader also expresses the original active large-model `_push` macro as an
explicit `if LDATA` plus a typed push of the far-pointer segment. The 320-byte
`BGM_READ_SDATA` loader is also reproduced in full: its original
`_push` macro has the same active large-data stack result as the
port's explicitly guarded `IF LDATA` / `push word ptr` form.
The original unused `pc98:` fallthrough label in `_BGM_BELL_ORG`
has no branch references and is source-verified separately.

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
the seventeen complete member extents. Unaccepted neighboring functions
and gaps remain unknown until their own source/macro-context review.

```sh
python3 scripts/review_master_bgm.py --check
python3 scripts/review_master_bgm.py --structural-check
python3 scripts/ownership.py --check
```

These are **third-party native ASM CODE** bytes, not the number of
decoded instructions, and contribute **zero game-authored C++ bytes**.
No full cold replay, invented source state, or new denominator is
involved.

## Private Master bell calculation and original alignment

The 104-byte `[3AAE,3B16)` scope belongs to `BGM_BELL`, the private near
helper immediately before `_BGM_PLAY`. The genuine Master 0.23 `B_PLAY.ASM`
contains this complete body, which chooses PC-98 or PC/AT speaker output,
scales pitch from the music part's note and octave, and writes the timer
period. The source changes only namespace-local labels, typed `SGLB.pmask`
access and an unused PCAT label; all 52 normalized source lines match. The
original TASM OMF supplies 104/104 exact native bytes with **two original
ordered offset fixups**, no MZ segment relocations and a final original
`EVEN` NOP at `3B15`, after its `RET`. That alignment byte is not new
game-authored instruction credit. The true extent is bounded by the end of
`_BGM_TIMERHOOK` and the public `_BGM_PLAY` entry, not an inferred public for
the private helper.

## Complete private decimal note-length reader

The original Master `B_MGET.ASM` begins with a non-exported `GETNUMBER:`
helper before the public `_BGM_MGET`. Its original source and the retained
TH05 TASM source have **23 identical normalized source lines**. The whole
`36C0..36E8` scope accumulates decimal note-duration digits into CX by
multiplying by ten, advances the music part's far text pointer and returns
near. The actual native OMF writes **40/40 original bytes**, including its
original EVEN alignment NOPs, with no FIXUPP or MZ relocations. The original
near helper is bounded by the preceding `_BGM_BELL_ORG` and following
`_BGM_MGET`, not an invented exported symbol.

These 40 CODE bytes are third-party Master source, with no new game-authored
C++/ASM credit. The existing verifier now covers 17 sound routines and
**2,266 source-backed CODE bytes** in MAIN without a whole-program rebuild.

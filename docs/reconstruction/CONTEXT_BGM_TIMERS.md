# Exact source-linked Master BGM timer/PSG functions in OP and MAINE

The native OP/MAINE CODE attribution now includes **14 complete original
Master 0.23 procedures totaling 1,224 previously unknown bytes** (612 bytes
per decoded executable). These are substantive functions, not an opcode match
restricted to a prefix; the largest is the **280-byte `BGM_TIMERHOOK` interrupt
controller** in *each* executable.

| Complete original Master function | OP | MAINE | Bytes each |
| --- | --- | --- | ---: |
| `_BGM_BELL_ORG` | `2CD0..2D28` | `2E98..2EF0` | 88 |
| `_BGM_TIMER_INIT` | `2F92..2FD6` | `315A..319E` | 68 |
| `_BGM_TIMER_FINISH` | `2FD6..3000` | `319E..31C8` | 42 |
| `_BGM_PINIT` | `3000..303E` | `31C8..3206` | 62 |
| `_BGM_TIMERHOOK` | `303E..3156` | `3206..331E` | 280 |
| `BGM_STOP_PLAY` | `3346..3360` | `350E..3528` | 26 |
| `BGM_SET_TEMPO` | `3360..338E` | `3528..3556` | 46 |

The original author ASM comes from `B_B_ORG.ASM`, `B_TIMER.ASM`,
`B_PINIT.ASM`, `B_TMHOOK.ASM`, `B_SP_PLY.ASM` and `B_S_TEMP.ASM` in the
separately pinned Master archive. The actual retained TASM source is the
corresponding `libs/master.lib/` family from the native OP/MAINE build. Each
**whole procedure** is source-equivalent under only explicitly verified
near-call `NOPCALL` spellings, the typed `spart` PSG record qualifier, and
private bell/clock label spellings. No function body, field offset or gameplay
operation is hidden by normalization. No TASM-generated instruction bytes
are copied into maintained authored C++ source.

Both real OMFs provide all CODE LEDATA bytes without holes and exactly
**63 ordered FIXUPP actions per artifact**. The independently recovered
original `_TEXT` start (`0000:0272`) and the original OP/MAINE DGROUP layout
are used to link source into the native decoded payload and calibration MZ.
Every byte in all 14 bounded contributions matches. Original ordered MZ
relocations are **not empty or assumed sorted**:

- `_BGM_TIMER_INIT`: a real segment16 relocation at function offset `+19`
  targeting `_TEXT` (segment `0000`). It is separately verified against the
  authentic OMF method, location and the actual ordered original MZ entry;
  this is **not** the DGROUP relocation convention used by most other helpers.
- `_BGM_TIMERHOOK`: a real DGROUP segment16 relocation at `+3` in each
  original context, in addition to the ordinary CODE/data offset16 fixups.

The original and calibration relocations, full procedure extents and unique
original target locations agree. Other BGM functions already accepted as
vendor source remain separately owned; these 1,224 bytes do not overlap them.
The untouched third-party code earns **zero game-authored C++/ASM byte credit**
and cannot establish whole-executable or packed-file exactness.

Source/code evidence:
[`context_bgm_timers.json`](../../config/context_bgm_timers.json).
Separate explicit ownership decision:
[`reviewed_context_bgm_timers.json`](../../config/reviewed_context_bgm_timers.json).
Run `python3 scripts/review_context_bgm_timers.py --check` for the focused
original source/OMF/native check. The public CI lane uses
`--structural-check` and the updated gapless ownership ledger; unrelated
accepted units and the whole-program cold replay were not rebuilt.

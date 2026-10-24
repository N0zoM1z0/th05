# Enemy rendering reconstruction

The algorithm is reused as natural C++ from the maintained TH04 owner
`src/main/enemy/enemies_render.cpp`, SHA-256
`738af3eb931e3b355b527f556f670f1086555779da3a4d1172d534f872d95a0b`.
TH04 acceptance does not transfer. The complete TH05 enemy layout is separately
corroborated by nmlgc/ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/enemy/enemy.hpp`. No reference assembly or target instruction stream
is transcribed into this source.

Pinned MAIN SHA-256:
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The complete original function is MZ load-module range **`[DF50,E01F)`**,
**207 bytes**, SHA-256
`527c9dc3b95b741ede2f3922851ce064e60de3224d5baf0f2cb650f3ae6c4017`.
Its 75 instructions decode through the terminal RET at `E01E`; all 15 local
branch targets are instruction starts. There is no CODE-data or padding.
Two ordered MZ fixups refer to the zero-valued far-call segment words.
Add the 4032-byte MZ header to convert these addresses to file offsets.

The target loop independently shows 32 entries and a 64-byte entity stride.
`enemy.hpp` preserves every real TH05 field: motion, signed HP/score words,
near script pointer and instruction position, byte speed and animation state,
signed item enum, all collision/autofire flags, complete 14-byte BulletTemplate,
subtype and unused members. Its five-byte unused tail comes from the complete
original structure declaration and record stride; it is not fabricated to fit
one selected field. Those state bytes receive no authored code credit.
Every member offset, complete 64-byte size and two-byte near script pointer is
asserted. Canonical item, template and geometry declarations are reused through
the existing bullet update header; no same-named alternative types are added.

Wrapper `th05/enemy_r.cpp` may include
`src/main/enemy/enemies_render.cpp`. Use established MAIN flags and the owner's
`MAIN__TEXT`, group `main_01`; original main_01 frame is **`0AE1`**, load base
**`AE10`**, with this function at group offset **`3140`**. DGROUP frame is
**`209D`**. The function is near Pascal and returns with RET.

| External binding | Original position | ABI |
| --- | --- | --- |
| `_enemies` | DGROUP:`93FA`, 2048 bytes | 32 real 64-byte enemy records |
| `SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1` | load `DF28`, main_01:`3118` | C near Pascal, signed word in/out |
| `SUPER_ROLL_PUT` | `0000:2FE0` | C far Pascal, three signed words |
| `SUPER_ROLL_PUT_1PLANE` | `0000:2E1A` | C far Pascal, four signed words and unsigned plane mask |

The normal blit retains `_AX` as the actual scroll helper result, as in the
maintained TH04 source; the damaged branch retains the saved `top` and clears
the real damage byte afterward. Genuine compiler registers come from
`<dos.h>`. Source branch order, animation division and sprite-byte arithmetic
are preserved. No ASM, emit, fake linker symbols or code-generation barriers
are present.

Private `.analysis/enemies-render-boundary-review.json` records the original
identity, complete extent, call sites and ordered fixups. A natural negative
control changes the unique local `ENEMY_W = 32` to 30, changing actual sprite
centering. Two fresh producers in `.analysis/unit-replays/enemies-render-b` reproduce
all 207 raw bytes and both ordered zero-valued frame fixups. Normalized OMF
and actual dependencies agree; the compiled width mutation is rejected.
Acceptance independently rechecks the saved producers and canonical source
without rebuilding unchanged units. Whole-program linkage remains open.

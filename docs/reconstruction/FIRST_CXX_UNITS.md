# Bounded MAIN C++ units

`player_angle_from` calculates a player-facing angle from Q12.4 coordinates
and adds an unsigned angle bias. The five tuning functions adjust stack count
from performance rank and dispatch the selected difficulty helper.
The next two Boss functions implement random, clamped flight and gradual
movement towards a point. The CFG reader loads the resident segment from
MIKO.CFG using three real DOS interrupt intrinsics.

Target `th05-main`, SHA-256 `c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`:

| Maintained unit | Load-module extent | Complete bytes | Instruction credit |
| --- | --- | ---: | ---: |
| `src/main/player/angle.cpp` | `0x171CC..0x171EA` | 30 | 29 |
| `src/main/bullet/tune.cpp` | `0x17676..0x176B8` | 66 | 62 |
| `src/main/boss/movement.cpp` | `0x15914..0x15AA2` | 398 | 398 |
| `src/main/formats/cfg_resident.cpp` | `0xE61E..0xE644` | 38 | 37 |
| `src/main/boss/explosion.cpp` | `0x1060E..0x107D2` | 452 | 452 |
| `src/main/hud/overlay.cpp` | `0x11D50..0x1245E` | 1806 | 1806 |
| `src/main/player/reimu.cpp` | `0xE6FB..0xEB92` | 1175 | 1175 |

Ranges are half-open and relative to the original MZ load module. Its header
is 4032 bytes; do not confuse these with packed-file offsets or physical memory.
The original raw function boundaries include final returns and five observed
NOP alignment bytes in the first two units, plus one CFG NOP. Explicit
codestring directives reproduce/check those NOPs;
they are excluded from authored instruction credit. Their original insertion
mechanism is not independently established. ReC98 module contributions suggested the sizes;
the original instructions and complete cold comparison confirm these extents.

The source begins as candidate ReC98 C++, with local owning declarations.
Borland compilation checks the full Motion and BulletTemplate field layouts,
enum widths and 16-bit integer/pointer assumptions. Declaration layout outside
used accesses remains a corroborated ABI hypothesis, not whole-object runtime
acceptance.

The unit oracle uses a **symbol-only linker context**, not a full game build.
`probes/units/main_bindings.asm` supplies no instructions or target payloads.
Its unused ORG holes place external symbols and contribute zero authored credit.
The target's observed references bind `iatan2` at `0000:1F3A`, `player_pos` at
DGROUP:`36D2`, `playperf` at `5770`, and `bullet_template` at `577E`.
The original startup loads DS from relative segment `209D`. Difficulty helpers
are at load offsets `1758E`, `175D2`, `1762A`; near-call differences are preserved.
Names and type roles are inferred from C++ semantics and corroborated source;
numeric references and branch destinations are target observations.

Boss context binds the 24-byte `boss` at DS:`5ABA`, sprites left/right/stay
at `371A/371C/371E`, eight-byte clamp at `1436`, and one-byte next-y direction
at `3720`. Near helpers are `randring2_next16` at load `1529C`, AND at `152AA`,
MOD at `152C0`, and `vector2_near` at `152DA`. The CFG context binds the filename
at DS:`18D2`, ten-byte CFG at `41F2`, and the four-byte resident pointer at `41FC`.
Raw accesses confirm these numeric bindings; complete unused state layouts
remain source-corroborated hypotheses. The CFG's three `geninterrupt(0x21)`
calls are compiler intrinsics, not transcribed instruction bodies. Unchecked
open/read errors and original movement rounding/AND behavior are preserved.

Two isolated, fresh builds compile the maintained C++ and link those bindings.
Every byte of each complete CODE contribution matches its pinned original
extent without masking, patching, substitution or normalization. The ordered
relative MZ relocation sites also agree. OMF structure and producer identity
pass; dependency-timestamp-normalized objects agree between cold rounds.
The sole angle relocation is a far-call segment word; tuning has none.

A third build changes performance threshold 38 to 39. The resulting executable
still links, but the raw comparison rejects it. Public tests additionally reject
same bytes with different fixups, truncated extents, split relocation words and
ambiguous MAP contributions.

Replay:

```sh
bash scripts/run_heavy.sh python3 scripts/replay_units.py --output .analysis/unit-replays/NEW
python3 scripts/progress.py --accept .analysis/unit-replays/NEW/receipt.json --write
python3 scripts/ci.py
```

The first replay accepted 6 functions and 91 instruction bytes. The next replay
cold-builds all four contributions and accepts 9 functions, 532 complete bytes
and 526 instruction bytes after excluding six observed NOPs. It does not prove
whole-program placement or standalone linkage. The next focused replay compiles
only the 452-byte Boss explosion contribution, reusing unchanged tool probes and
the four prior accepted contributions. This brings the current total to
11 functions, 984 complete bytes and 978 instruction bytes. It does not prove
whole-program acceptance. Two subsequent focused replays add nine HUD overlay
functions (1806 bytes, including 24 ordered far-call fixups and a near callback)
and eight Reimu shot functions (1175 bytes, zero MZ fixups). These reuse previous
accepted sources and unchanged tool probes. Current total: 28 functions,
3965 complete bytes and 3959 code bytes. It does not prove
whole-program placement, global layout, standalone linkage, data ownership,
packed-file exactness, runtime gameplay or the global authored-byte percentage.
The first whole-reference MAIN calibration differs from the original and is
retained as a failed counterexample, not an accepted executable.

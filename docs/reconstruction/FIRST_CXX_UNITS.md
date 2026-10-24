# First bounded MAIN C++ units

`player_angle_from` calculates a player-facing angle from Q12.4 coordinates
and adds an unsigned angle bias. The five tuning functions adjust stack count
from performance rank and dispatch the selected difficulty helper.

Target `th05-main`, SHA-256 `c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`:

| Maintained unit | Load-module extent | Complete bytes | Instruction credit |
| --- | --- | ---: | ---: |
| `src/main/player/angle.cpp` | `0x171CC..0x171EA` | 30 | 29 |
| `src/main/bullet/tune.cpp` | `0x17676..0x176B8` | 66 | 62 |

Ranges are half-open and relative to the original MZ load module. Its header
is 4032 bytes; do not confuse these with packed-file offsets or physical memory.
The original raw function boundaries include final returns and five observed
NOP alignment bytes. Explicit codestring directives reproduce/check those NOPs;
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

This acceptance covers 6 functions and 91 instruction bytes. It does not prove
whole-program placement, global layout, standalone linkage, data ownership,
packed-file exactness, runtime gameplay or the global authored-byte percentage.
The first whole-reference MAIN calibration differs from the original and is
retained as a failed counterexample, not an accepted executable.

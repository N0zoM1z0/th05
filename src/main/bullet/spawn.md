# Bullet spawning (assembly)

`spawn_groups.asm` and `spawn_raw.asm` hold TH05's bullet spawning code. It
is kept as assembly, as in ReC98's `th05/main/bullet/add_1.asm` and
`th05/bullet.asm`. `spawn_types.inc` declares the records they use (bullet
template, `bullet_t`, motion, gather template).

| File | MAIN range | Contents |
| --- | --- | --- |
| `spawn_groups.asm` | `171EA..173DE` | playperf speed tuning, the four spawn wrappers, group velocity/angle calculation and its 16-entry handler table |
| `spawn_raw.asm` | `1743C..17676` | raw bullet allocation, its far regular-spawn trampoline, and the Easy/Hard/Lunatic template tuning |

The C++ `bullet_template_clip()` (`clip.cpp`) sits between the two, and the
C++ tuning wrappers (`tune.cpp`) follow the second.

## Why this stays assembly

The code passes state in registers across its helpers: AL holds the speed
being tuned, BL/BH the spread/stack state, CL/CH speed and group iteration,
and SI/DI the angle and completion state. Raw allocation patches two byte
immediates in the code segment before spawning. Easy and Lunatic tuning jump
into Hard's dispatcher and handlers instead of being separate functions.

## Behavior to preserve

- Byte arithmetic wraps; the stack completion test is signed.
- Random rings advance their pointer by its low byte only.
- Invalid group IDs fall back to the default handler.
- ZUN bug: Easy's stack decision tests a stale AH, which holds the last
  spread angle delta rather than the stack count.

## Padding

Alignment bytes, an inert jump to the next instruction (`spawn_raw.asm`
`[178,180)`) and the two runtime-patched immediates (value 123) are compared
like all other bytes but count as padding, not authored code.

## Replay

```sh
python3 scripts/replay_asm_family.py --plan
bash scripts/run_heavy.sh python3 scripts/replay_asm_family.py \
  --unit main-bullet-spawn-groups \
  --native-review .analysis/bullet-spawn-native/groups-boundary-review.json \
  --output .analysis/bullet-spawn-native/NEW_FRESH_DIRECTORY
```

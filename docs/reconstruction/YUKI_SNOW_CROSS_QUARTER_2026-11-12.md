# Yuki solo snow cross: four real quarter-turn launches

In the complete original 670-byte four-function Yuki late-attack compiler
unit, the snow-cross attack fires four actual B4 projectiles in four
successive quarter-turn directions. The maintained
`YUKI_SNOW_CROSS_QUARTER()` source protocol calls the real `b4balls_add()`
**before** each `+0x40` angle step; it is expanded at all four original
call sites. Only after all four launches does the snow-direction oscillation
increment the angle. All actual bullet callback, sound, timeout and RNG
behavior is unchanged.

This existing dirty source edit was **not discarded**: the complete
`main-yuki-solo-later-patterns` contribution was freshly replayed through
both genuine original Borland/TLINK producers, reproducing all 670 bytes
and the original ordered relocation stream. The compiled original semantic
negative was rejected. Receipt:
`.analysis/unit-replays/gpt-web-yuki-four-snow-cross-quarters-20261112-a/receipt.json`.
This improves an already exact natural source and grants no duplicate CODE
credit; no full cold replay or other unrelated units were run.

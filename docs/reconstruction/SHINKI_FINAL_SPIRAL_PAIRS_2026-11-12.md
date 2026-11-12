# Shinki's original final spiral: paired offsets and distinct ring updates

The Shinki final-circle callback is compiled immediately before the
full **959-byte** `shinki_update()` controller in the real MAIN03 original-
order producer. Both opposite B6 balls use the same real centered offset
placement and `b6balls_add()` after the shot angle is selected, while the
red cloud ring and pellet cloud ring use the same spawn-mode/group/speed/
spread preparation but retain different sprites, angles and post-spawn
angular steps. The natural C++ now expresses those two genuine protocols
as `SHINKI_SPIRAL_FIRE_OFFSET_B6BALL()` and
`SHINKI_SPIRAL_FIRE_RING(direction, sprite)`.

No branch cadence, randomness, origin offset, sound event, projectile state
or relative execution order changes. The focused original-compiler replay
`main-shinki-update-context` rebuilt the **complete 959-byte accepted owner**
with real final-circle compiler context: both independent TCC/TLINK
producers match all original raw bytes and original ordered MZ relocations,
and the compiled semantic negative is rejected. Receipt:
`.analysis/unit-replays/gpt-web-shinki-final-spiral-pairs-20261112-a/receipt.json`.
The source is a refinement to already accepted Boss CODE with no duplicate
credit, not a new synthetic code producer or full cold replay.

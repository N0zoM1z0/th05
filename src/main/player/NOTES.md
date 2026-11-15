# Player: notes

- **Death radius.** An unsigned 16-bit value: it subtracts 112 with wrap and
  halves unsigned at the fifth of eight points. TH04's signed division gives
  different wrapped values.
- **Rounding.** Reimu's bomb-star slow pixel conversion is signed division
  by 16; a shift rounds negatives differently. The renderer's half-radius
  accumulator must stay signed int for the same reason.
- **Bomb timing.** Yuuka restores the hardware scroll on bomb frame 161,
  Reimu on frame 130. Yuuka's signed `% 4` tests play the sound and select
  tone 150 on remainder 0 and tone 100 on remainder 2.
- **Miss.** During the miss animation, dream values above 2 decay by 2 on
  Boss HP-fill or odd stage frames, and values at or below 2 become 1. The
  last four frames flash the palette.
- **Player update.** A pending hit opens the 40-frame deathbomb window,
  192 invincibility frames and 72 frames of respawn movement. Movement
  retries conflicting input once and optionally halves the signed velocity.
- **Shots.** Homing expires at age 16 but still applies that frame's step.
  Collision uses inclusive unsigned relative-distance boxes. The laser
  collision variant reflects regular bullets except on three of every four
  Easy frames. The shot clock is an 18-frame cycle.
- **Shot velocity table.** 256 points of two signed Q12.4 words at 12 px/frame.
  `scripts/generate_shot_velocity_table.py` regenerates it with an 80-digit
  sine series and explicit nearest rounding.
- **Power thresholds.** The power byte at DS:36F0 is compared against nine
  unsigned words at `[BX+18AC]`.
- **Codegen.** `hitshot_from()` must compare an unsigned byte; a signed
  `char` widens with `CBW`. In `shots_render()`, declaring the loop counter
  before the `Shot*` pointer gives the native `BP-2`/`BP-4` layout. Reimu's
  option iterator initialises only its counter; the angle is set by the
  branches. The `shot_update()` angle stays a plain `char` field, written
  through an `unsigned char` reference for `+=`/`-=`.

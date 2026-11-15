# EX-Alice (Extra stage): notes

- **Phase ladder.** 18 phase values, with HP endpoints 26,500 → 23,800 →
  21,000 → 18,100 → 15,100 → 12,600 → 9,600 → 6,800 → 3,400 → 0. Each of the
  four regular waves runs 32 patterns.
- **Pattern selection quirk.** After each random flystep the controller
  increments `patterns_seen` and looks up
  `exalice_patterns_by_phase[wave][patterns_seen & 1]` *before* testing
  `patterns_seen >= 32`. At 32 the selected callback never runs: the jump to
  `regular_complete` skips both the callback and the hit/score-bonus path.
  Each wave starts with a preinstalled callback: `random_fan`,
  `gravity_stacks`, `fixed_laser_fan` (not in wave 3's two-entry bank) and
  `cross_cheetos`.
- **Charge timeout.** The test is strictly `phase_frame > 4000`, so frame
  4000 still hit-tests and frame 4001 jumps straight to charge completion.
- **Bomb gate.** Bombing reloads the immunity byte to 39 every frame. The
  controller decrements it at the start of each update, so the last bombing
  update leaves 39. Shots are hit-tested only when the byte is zero.
- **Phase transition.** Increments the phase, resets frame/mode/pattern count
  to `0/REPOSITION/0`, copies the previous `phase_end_hp` into HP and installs
  the next threshold. An untimed completion can explode and enable the
  item-dropping bullet zap.
- **Final fan.** Charges at frame 64 and fires two bullets on every even frame
  from 128 to 5000 (2,437 volleys). The leaf runs before the inclusive
  `phase_frame <= 5000` hit gate, so frame 5000 fires and hit-tests; frame
  5001 skips the hit test and leaves `defeat_bonus` false. Bullet speed goes
  from 2.5 to 6.5 px/frame and the orbit radius from 0 to 64 pixels as HP
  drops, using unsigned 32-bit multiply/divide. The orbit position uses the
  previous frame's radius, so it lags HP by one update.
- **Byte 15.** The Ready transition seeds it to zero. In wave 1 `random_fan`
  ignores it, and `turning_rings` toggles it at frame 64 and uses it as its
  rotation direction.
- **Laser patterns.** The fixed-laser fan uses the first 16 slots of the
  32-slot laser array and a signed 16-bit cyclic slot counter at DS:1998,
  reset at frame 208. Bouncing rings grow by one bullet every 128 frames up to
  a strict limit of 14.
- **Firewave renderer.** Player coordinates use signed `/ 16`; the vertical
  band test is an unsigned 16-bit difference, and the left/right horizontal
  comparisons are asymmetric.
- **Hexagrams.** The one-byte `hexagrams_flag` cycles through
  uninitialised/clockwise/counterclockwise. The radius grows by 5 pixels per
  update and resets at 320, flipping the rotation. Coordinates are converted
  to pixels by signed `>> 4` before drawing.

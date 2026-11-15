# Alice (stage 3): notes

- **Phase ladder.** The 15-phase controller walks the HP thresholds
  7,400 → 5,200 → 3,000 → 800. Regular waves of 24 patterns alternate with
  puppet-beam phases. The setup, ready and puppet-entrance clocks are 128, 64
  and 128 frames; the final spread ends strictly at frame 1,000.
- **Puppet beam.** Charging circles start on the beam's frame 16 (radius 64)
  and contract as `(64 - beam_frame) * 2` during frames 32..63. Each beam
  phase lasts 600 Boss frames and opens with a 160-frame burst window that
  grows unchecked. Shot collision uses a 56×8 pixel radius centred 64 pixels
  right of puppet 0. The player rectangle is a different 128×8 box with a
  4-pixel lead, compared as unsigned 16-bit values (inclusive left, exclusive
  right, wrapping).
- **Puppet motion.** Each axis moves by half the 16-subpixel unit, then by a
  quarter of the residual, and snaps to the previous position once both
  truncated increments are zero. X updates before Y.
- **Charge patterns.** Gather starts at frame 40, fire at 64, finish at 96.
  The gather call pushes `(frame - 40, 9, 8)`. The laser fan spawns three
  aimed lasers spaced ±16 (colour 6, width 8, age 40, speed 5).
- **Scratch bytes.** `AliceScratch` is a view of `boss_statebyte[16]`: byte 7
  is the attack wave (0–3), byte 8 the beam sprite base, byte 9 the beam
  phase and byte 15 the charge angle. Each charge pattern reseeds byte 15 to
  8 or 0, so it carries nothing across phases.
- **Codegen.** The foreground's animation expression has to be written as
  three plain branches over the existing frame-modulo variables. A joined
  byte-frame local (with or without `register`) emits 146 bytes with an extra
  store/reload, and an inline quarter-frame helper emits 148.

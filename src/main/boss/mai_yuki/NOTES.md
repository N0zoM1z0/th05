# Mai and Yuki (stage 4): notes

- **Shared fight.** 9,000 shared HP with gates at 5,500 and 2,250. The first,
  laser and final pattern banks run 10, 5 and 21 completed callbacks. The
  forced HP-gated repositions (pattern 9 or 14) use a 64-frame lead-in and
  trigger their clear/explosion effects at frame 16; normal repositions use
  16 frames. All five near-pattern array selections index with `& 3`.
- **Defeat.** The first small explosion is at frame 16 and the big circle and
  survivor sprite choice at frame 32, followed by ±4 shake for 12 frames and
  an 8-frame sprite progression. At frame 64 the survivor's dialog and BGM
  title load with palette tone 60. If Mai lost, Yuki's position is copied into
  the shared primary Boss object.
- **Initial patterns.** Mai's completed callback resets the shared timer and
  mode; Yuki's deliberately does not. Yuki's persistent patterns return
  false and fire at 16/8/2-frame cadences.
- **Survivor solos.** Yuki's attack counters are per wave: the first wave
  ends at 12 attacks, `boss_phase_next()` resets `patterns_seen`, and the
  second wave runs a further 24. The final bank cycles with
  `patterns_seen % 5`. Mai's laser cycle and revenge snow reuse scratch
  byte 10 for two successive roles (pattern counter, then snow angle).
- **B4 balls.** Destruction quarters both signed velocity components
  (division toward zero), adds 550 score and, with revenge enabled and
  Y <= 240 pixels, fires one regular bullet. Decay advances one sprite every
  four ticks and frees the ball after four cels.
- **Codegen.** Mai's standalone update needs `#pragma option -a2` after every
  object type is complete, to word-align its switch table. In the foreground,
  declaring the four uninitialised coordinates in the order Mai-left, Mai-top,
  Yuki-left, Yuki-top keeps Mai's in SI/DI and Yuki's on the stack. Including
  the broad HUD overlay header redeclares `to_sp(float)`; a `bool`
  declaration before Turbo C++'s canonical typedef fails to compile.
- **Disassembly trap.** The near Boss predicate at `1527:A860` is load
  `1FAD0`. Disassembling with a global linear address wraps the relative
  operand and prints `FAD0`.
- **Relocation order.** A direct TCC object for the late-pattern prefix emits
  a cyclic rotation of the target MZ relocation order; only the full
  surrounding context reproduces it.

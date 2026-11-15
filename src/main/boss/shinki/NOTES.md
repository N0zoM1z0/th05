# Shinki (stage 6): notes

- **Devil pattern.** Spread bullets start after a 192-frame delay and fire
  every 4 frames. The outer angle climbs from `0x00` by `0x04` to `0x40` at
  frame 256, then swings between `0x40` and `0x30` every 64 frames. Lasers
  arm at HP <= 5,600 or frame 1,800. The four fixed lasers are assigned in
  A/B/C/D order as `(outer, inner, 0x80-inner, 0x80-outer)`. They turn on
  phase frames divisible by 8, and the turn state repeats after 18 turns
  (144 frames).
- **Devil fast cadence.** The B6 interval switch is gated by HP <= 3,800 or
  frame >= 2,500, but is only checked on laser-turn frames: when time
  triggers it, frame 2,504 is the first eligible one. The spawn check runs
  before the switch, so the new rank interval (52/20/16/12) applies from the
  next callback. `shinki_devil_laser_grow_delay` is a 16-bit int; the
  comparison against 65 is a one-shot gate that cannot wrap and retrigger.
- **Devil cleanup order.** The phase controller, not `pattern_devil()`, stops
  lasers A–D after its HP/timeout decision. `laser_stop()` shrinks an active
  laser but frees a waiting or growing one, so an active beam still renders at
  full width on the exit tick. Moving the stops into the pattern would change
  that frame's hit/render order.
- **Devil codegen.** The ReC98 "turn into a loop" suggestion is unsafe: a
  four-slot `for` loop emits 800 bytes instead of 802. Keep the four
  explicit calls.
- **Final phase timing.** Phase 11's 16-frame defeat transition does not
  clear `phase_frame`: it advances to phase 12 at frame 17, so phase 12 first
  sees frame 18. The 3,000-frame timeout is measured from phase-11 entry. The
  leaf runs before the strict `phase_frame < 3000` hit gate, so frame 3,000
  still fires and then skips the hit test, leaving `defeat_bonus` false. Over
  the phase: 360 opposed B6-ball pairs (frames 128..3,000 every 8), 176 red
  rings, 152 pellet rings and 2,281 flystep calls from frame 720.
- **Final B6 speed carry.** The final two-ball spiral never sets
  `b6ball_template.speed`. It inherits whichever earlier phase wrote last:
  phase 8's purple transition (sixteen random 2.0–6.0 values at frame 192),
  phase 9's first rank-timed aimed ball (4.0 at frames 192/160/140/144 for
  Easy..Lunatic) or the Devil's first aimed ball (3.75 at frames
  256/280/256/280). The HP gates can end phase 9 or the Devil before those
  writes, so the final phase may still use the last purple random speed.
  `b6balls_add()` copies and tunes the template speed into a local.
- **Wing phases.** Wing rain waits until frame 128, then drops blue B6 balls
  every 8 frames at 3.0–5.0 px/frame, with a five-bullet aimed spread every 24
  frames (angle deltas 16/12/10/8 by difficulty). The purple transformation
  shakes for frames 160..191, spawns 16 purple balls at frame 192 (angles
  `[0x20,0x60)`, speeds 2–6) and returns true at frame 200. Wing preparation
  alternates tone 100/150 over eight frames and stops all six lasers before
  returning.
- **Yumeko handoff.** Yumeko's laser-sword pattern writes the laser template
  width (6) and Stage 6 never resets it; Shinki's six manual spawns copy that
  inherited width into `grow_to_width`.
- **Enum width.** The 3,000-frame wing threshold must stay in the 16-bit local
  enum. Moving it to a byte-sized enum changes Borland's DX vs DL parity
  masking.
- **B6 balls.** `b6ball_t::age` is never reset by the original update; the
  word is effectively unused. Decay halves both signed velocities and
  advances one cel every four frames through sprites 204–207.
- **Background state.** `[22360,22363)` holds three one-byte flags: type C
  initialised, type D initialised, and EX-Alice's `hexagrams_flag`.
  `_shinki_bg_type_a_particles_alive` starts at 255 (`-1 & 0xFF`) as an
  "uninitialised" sentinel compared against a signed word.
- **Particle renderer codegen.** Turbo C++ lowers `top > 0` to two-byte
  `OR AX,AX` where the original has `CMP AX,0`. ReC98's `keep_0()` helper
  (the address of an external `address_0`) forces the three-byte compare
  while keeping the signed condition.

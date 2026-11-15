# Midbosses: notes

- **Defeat ring.** 16 sprites revolving at radius `phase_frame << 4`
  subpixels, capped at 48 pixels.
- **Stage 1.** The orbit radius is a signed 16-bit HP subtraction followed by
  an unsigned 32-bit multiply.
- **Stage 2.** The entrance lasts 256 invulnerable frames. Byte 14 (the orbit
  drift) is stored unsigned but read as `signed char` before each
  increment/decrement; widening or clamping it breaks the wraparound. The
  final attack ends at frame 800.
- **Stage 3.** Each update publishes the midboss position to the bullet and
  gather templates. After a 32-frame wait it picks pattern
  `(patterns_done % 3) + 1`. Patterns charge until frame 32, fire at 32/48/64
  and reposition at 96. The vanish helper snaps X to the player, clamped to
  64..320.
- **Stage 4.** 1,100 HP, a 192-frame entrance and sixteen patterns. Patterns
  telegraph at frame 16, fire during frames 48..80 and return at 96. The
  disappearance leaf disables vulnerability at frame 16, picks a new centre
  in `[64,320) × [64,96)` at frame 48 and returns at 80; the caller resets
  `phase_frame`, the leaf does not clamp it.
- **Stage 5.** The entrance ends at frame 192. Charge circles appear at frame
  16 (colours 3 and 2) and each callback starts at frame 32. Pattern bodies
  return 0/1 in AX and the caller reads AL.
- **Extra.** Byte 12 picks the early or late pattern set once HP drops
  strictly below 1,000; byte 13 is a wrapping signed ring step, byte 14 the
  dash count and byte 15 the dash animation. The swing animation keeps
  `frame *= 2` and a bitwise OR of its two conditions.
- **Codegen: mask width.** `midbossx_patterns_done & 7` must use an `int`
  mask. The original promotes before masking (`MOV AL; MOV AH,0; AND AX,7`);
  an `unsigned char` mask emits `AND AL,7; MOV AH,0` and is one byte short.
- **Disassembly trap.** In 16-bit CS coordinates the stage-2 damage target is
  `1527:A820` (load `1FA90`); a linear disassembler shows `FA90`.
- **Open.** The default midboss's final 65-byte function calls the far
  `midboss_reset()` with four bytes (`PUSH CS` / near call) at `1C663`. A
  typed far call produces five; natural relaxation to the original form is
  unproven.

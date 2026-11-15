# Louise (stage 2): notes

ReC98 has no C++ for Louise yet. Its `th05_main.asm` calls her movement
function `sub_18BB8`. The names here are our own.

- Louise's fight has eight phases with HP thresholds 4400, 3000, 1900, 500
  and 0. Phases 3 and 6 are 64-frame pauses before she switches to her firing
  sprite. The first three attack phases end after 20 patterns, the last one
  after 10.
- `boss_statebyte` (`scratch.hpp`): byte 10 is the charge speed (0x18 at
  first, 0x14 for the turning rings), byte 14 selects between sweeping lasers
  and turning rings, and byte 15 is the direction of the blue spreads and red
  stacks, later picked at random by the sweeping lasers.
- The mirrored fans slow down each bullet group by adding the byte `0xFB`.
  A compound assignment made the unit 6 bytes shorter, and a plain
  `speed.v = speed.v - ...` had the right size but generated SUB instead of
  ADD. `louise_speed(-0.3125f)` doesn't
  work either, since that helper converts the float straight to an unsigned
  byte. Negating the converted positive value gives ZUN's code.
- `louise_update()` needs `#pragma option -a2` to word-align its phase switch
  table.

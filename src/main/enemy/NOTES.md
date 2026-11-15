# Enemy notes

Enemy code is mostly C++ following TH04's enemy and STD code, with TH05's own
64-byte `enemy_t` (`enemy.hpp`). The enemy script interpreter is original
assembly (`script.asm`, see `script.md`).

Layout in MAIN: `enemies_add()` and `std_run()` (`ENEMY_SPAWN_TEXT`), then
`enemy_bullet_template_push()`, then `enemies_update()`, all in `main_03`.
`enemies_render()` and `enemies_invalidate()` are in `main_01`.
`enemies_add()` is built twice: on its own by `spawn.cpp`, and together with
the rest by `lifecycle.cpp`, which both include `spawn.inl`.

## TH05 differences from TH04

The STD spawn record is 8 bytes: script index, unaligned x/y words, item,
subtype and an unused byte. Enemies start with autofire on Lunatic, kills give
7 sparks, the score is widened as unsigned, items are only dropped if not
`IT_NONE`, homing has no player-height cap, and on-screen enemies recharge the
dream gauge (the byte at DS:36F6, not the one at 36F5). `enemies_gone` and
`enemies_killed` are separate words.

## Code generation details

- `std_run()` and `enemies_update()` call far functions in their own code
  segment (`midboss_activate_if_stage_frame_is_midboss_start_frame()` and
  `sparks_add_random()`). `#pragma samecodeseg` tells the compiler, so TLINK
  shortens those calls to `NOP / PUSH CS / CALL near` as in the original.
- `enemy_bullet_template_push()` is a 7-word `REP MOVSW`. A structure
  assignment calls `F_SCOPY@` instead, and `__memcpy__` sets SI, DI and CX in
  a different order; setting the pseudo-registers in source order matches.
  Its parameter is a reference to the template, not to the whole enemy.
- `enemies_invalidate()` passes the 4-byte `SPPoint` through a function
  pointer cast, which gives the original single 32-bit push to
  `tiles_invalidate_around()` (declared as two words, y then x).
- `enemies_render()` passes `_AX` instead of `top` to `super_roll_put()`;
  the original reuses the scroll helper's return value.
- The script interpreter's movement helper returns its result in CF
  (CLC/STC) and its caller branches on it directly, so it cannot be a normal
  C++ `bool` function.

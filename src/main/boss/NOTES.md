# Boss code: notes

Code shared by all bosses lives in this directory. Each boss has its own
subdirectory. Most of the C++ here is adapted from ReC98 (`th04/main/boss/`
and `th05/main/boss/`). The ASM files (`backdrop_fill*.asm`,
`sparks_add_*.asm`) are hand-written register-level code. Their `.md` files are
part of the ASM unit configuration.

## Things that are needed to reproduce the original code

- **`boss_hittest_player()`** (`collision_body.inl`) has to compute the
  distances in the `_AX`/`_DX` pseudo-registers, as in ReC98. With ordinary
  local variables, Turbo C++ puts X into BX and the function grows from 43 to
  46 bytes. Seventeen variants were tried (declaration order, subtraction
  order, `register` hints, direct comparisons). The closest one was 45 bytes.
  A full `SPPoint` local spills to the stack and gives 59 bytes.
- **`midboss_hittest_shots_damage()`** must keep its four separate hitbox
  stores. The inline `shots_hittest(center, radius_x, radius_y)` helper
  generates 4 fewer bytes.
- **`boss_defeat_update()`** needs ReC98's empty `optimization_barrier()`
  call. Without it, the compiler merges the two `stage_allclear_bonus()`
  calls. Unlike ReC98's version, this build does not call
  `score_delta_commit()` before saving the stage score.
- **Sara's foreground renderer** needs its locals declared as `left, top,
  patnum`. Declaring them as `top, patnum, left` puts `left` on the stack
  instead of DI, which adds 2 bytes and moves Louise's renderer after it.
- **`shinki_bg_particles_render()`** compares the top coordinate with
  `keep_0(0)`, which returns the address of a symbol at DGROUP:0000. This
  produces ZUN's `CMP AX, 0` instead of `OR AX, AX`.
- **`background.cpp`** puts its last two functions into a second segment
  (`BOSS_BG_LATE_TEXT`). Compiled as one segment, the code bytes are
  identical, but the third 1024-byte LEDATA record ends in the middle of the
  last function, and one far-call relocation ends up out of order.
- The random-range helpers in `background.hpp` must keep their layering
  (float to subpixel, then signed range). Writing them with local min/max
  temporaries stops the compiler from folding branches and adds 46 bytes to
  one function.
- **`player_sparks_circle()`** pushes radius and count with a single 32-bit
  immediate (`00C00018`). Swapping the arguments keeps the size but changes the
  immediate.

## Data

- `explosion_big_frame` (`explosion_frame.c`) is at DGROUP:18E4. Those two zero
  bytes were first attributed to the Stage Clear Miss/Bomb counters, which are
  actually at DGROUP:1A62 (see `src/main/stage/NOTES.md`).
  Zero-initialized data alone doesn't identify its variable.
- `late_game_state_publics.h` declares three unrelated C globals between
  Shinki's float-direction latch and those Stage Clear counters:
  `bullet_zap_drop_point_items` (DGROUP:1A5C), `hud_hp_bar_value_prev` (1A5E)
  and `midboss_defeat_angle` (1A60). Their definitions are in `src/main/bullet/`,
  `src/main/hud/` and `src/main/midboss/`. The zero bytes between them are
  alignment, which nobody owns yet.
- `boss_flystep_random_clamp` (`movement_default_clamp.cpp`, DGROUP:1436)
  defaults to X [32,352] and Y [24,128]. EX-Alice overwrites it with her own
  arena.

## Linking

Mai and Yuki's direction latches have names longer than 31 characters. Turbo
C++ truncates external names to 31 characters, so the symbol bindings must use
the truncated names.

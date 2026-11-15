# MAIN HUD notes

The HUD code is C++ except for three hand-written ASM routines: the
eight-cell bar (`bar.asm`), the score display and update (`score.asm`) and the
decimal number renderers (`numbers.asm`). Their notes are `bar.md`, `score.md`
and `numbers.md`. The remaining files hold the HUD's initialized data.

## Code generation

- `combined.cpp` exists because `hud_put()` only compiles to the original
  bytes behind the eight HUD functions that precede it. On its own it would
  start at an even address, which changes the alignment byte before its switch
  jump table and the grouping of its relocations. The eight functions are
  copies of `score_reset.cpp`, `lives_bombs.cpp`, `indicators.cpp` and
  `hp_draw.cpp`; keep them in sync. `combined.hpp` cannot include those files'
  headers, because each one places its functions in its own code segment.
- In `hud_put()`, the rank label must be passed as
  `(const char near *)&glEASY[rank * 8]` and converted to far implicitly. An
  explicit far cast computes the offset before pushing DS, while the original
  pushes DS first (12 bytes differ).
- `hud_bar_put()` takes an `int` value although the ASM routine only reads its
  low byte. Declaring it with a byte parameter lets the compiler push the
  global's memory word directly, saving two bytes in both the dream and power
  callers.
- `hud_bombs_put()` compares `bombs` as an unsigned byte, although the variable
  is signed everywhere else.
- `overlay_data.h` needs `-a2` for the word-aligned variables, but only after
  the one-byte fade union; with `-a2` in effect, the union is padded to two
  bytes and shifts the next two fields.
- `colors_and_hp.c`: the two identical "x" strings for lives and bombs must be
  non-const, or the compiler merges them. The leading zero byte of unknown
  purpose is needed to put the following data at its original even address.
- `overlay.cpp` assigns its own functions to the near callback pointers
  `overlay1`/`overlay2`, so its link layout must keep the original
  `main_01`-relative function addresses (`overlay_titles_update_and_render`
  is at `711D`).

## Game behavior

- `score_reset()` copies a beaten high score digit by digit into the resident
  structure before clearing the score. Digit 0 counts the continues used and is
  neither compared nor cleared. TH04's version only clears the score.
- The dream bar reaching its maximum (128) shows the "DreamBonus Max" popup and
  clears bullets for at least 20 frames.
- The HUD number renderers in all three ASM files share one nine-byte glyph row
  (`decimal_scratch.c`) and the powers-of-ten tables in `decimal_tables.cpp`.

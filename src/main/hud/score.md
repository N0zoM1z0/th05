# hud_score_put() and score_update_and_render() (score.asm)

`hud_score_put()` draws the high score at (56, 4) and the current score at
(56, 6). Scores are eight little-endian decimal digits; digit 0 counts the
continues used.

- The current score directly precedes the high score in memory. The loop
  starts at the high score's top digit and simply keeps walking backward into
  the current score, so the two variables must stay adjacent.
- ZUN bug: SI and DI are popped in the wrong order, so the function returns
  with the caller's SI and DI swapped.

`score_update_and_render()` adds part of the pending `score_delta` to the score
each frame:

- The per-frame step is `score_delta / 32`, at least 1 and at most 6111. A
  larger step from the previous frame is kept, as long as it does not exceed
  the pending delta. Only the low word of `score_delta_frame` is written.
- The step is split into decimal digits with the five-digit power-of-ten table,
  using the shared glyph row as scratch space, and added with `AAA` carries.
- ZUN quirk: the highest digit is added without carry adjustment, so a score
  overflow produces glyphs beyond 9.
- If the new score beats the high score, it is copied over with interrupts
  disabled and the direction flag set (`CLI`, `STD`, `REP MOVSB`, `CLD`,
  `STI`), and the first time this happens, the "HiScore Entry" popup is shown.
  After that popup, every update copies the score without comparing.

ReC98's `th04/main/scoreupd.asm` (GAME == 5 branch) documents the same code.

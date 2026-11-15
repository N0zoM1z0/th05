# MAINE high score registration

ReC98 only has the glyph ball types for this module (`th05/regist.cpp`); the
functions were decompiled from the original binary, following the structure
of TH04's registration code.

## Build contexts

`full_context.cpp` compiles the whole original module (decoded MAINE
`B4D6..C5E7`, 17 functions) in order. The function bodies live in the `.inl`
files and in `src/maine/score/end_body.inl`, and are shared with the smaller
wrappers (`alphabet.cpp`, `commit.cpp`, `frame.cpp`, `values.cpp`,
`display.cpp`, `places.cpp`, `motion.cpp`), which were matched first.
`spawn.cpp`, `update.cpp` and `menu.cpp` are not used by any unit.

Several functions only match together with their original neighbours:

- `regist_menu()`'s bytes match on their own, but its 31 relocations only
  come out in the original order in `full_context.cpp`. Borland writes code
  in 1024-byte LEDATA records and orders fixups by record; the two score
  codecs in front move that boundary to the right place. Compiling through
  `TCC -S` and TASM gives ascending fixups and doesn't help either.
- `glyphball_spawn()` is one byte short alone (the zero before its switch
  table is missing), and `glyphballs_update()` matches alone except for its
  relocation order. `motion.cpp` compiles both together and matches.
- `registration_score_put()` and `registration_place_put()` come out one byte
  off alone; `values.cpp` and `display.cpp` group them with their neighbours.
  `display.hpp` must declare both display functions in one segment context.

## Small things that change the generated code

- `glyphballs_commit_and_wait()`: the second loop initializes `i` before
  `ball`, the first one the other way round.
- `glyphball_spawn()`: `place_r` must be a register variable captured before
  the `ball` pointer.
- `registration_stage_put()`: `y` must be declared before `color`.
- Phase changes use `ball->phase++`/`--`. Arithmetic with enum casts compiles
  to longer code.
- `motion.hpp` must leave the SHARED segment ungrouped, or the far calls into
  it are encoded with the wrong frame.
- The codecs' byte rotation is an inline `ROR` with the key in `AL`
  (see `full_context.cpp`).

## Data

`alphabet_data.cpp` holds the 3x17 keyboard, `initial_cursor_state.cpp` the
flipped VRAM page and the name cursor. Of the 9 glyph balls, only 8 are ever
used.

# Stage code notes

## Stage setup (`setup.cpp`)

The ten functions from `boss_reset()` to `stagex_setup()` follow ReC98's
`th05/main014.cpp`. ReC98 also places `score_delta_commit()` there, but in
the original MAIN the next function after `stagex_setup()` belongs to a
rendering module, so it is not part of this file. The file is compiled with
`-d-` (no duplicate-string merging); the repeated `"st03.bb"` literal must
stay a separate string. `select_for_rank()` is a far function in the same
segment, so TLINK turns its two calls into NOP / PUSH CS / near CALL.

## Stage 2 background

- `PlayfieldMotion::update_seg1()` returns the new X in AX and Y in DX.
  `stage2_update()` has to compare those registers directly; storing the
  returned point in a local first produces 11 extra bytes.
- In `stage2_particle_init()`, `frame <<= 3` compiles to a shorter in-place
  shift (476 bytes instead of 492), and a named X temporary gets spilled to
  the stack (498 bytes). Assigning `frame = frame * 8` and storing directly
  into the particle reproduces the original.
- `stage2_palette_falling` is a separate byte (DS:4A84) and is not part of
  `stage2_transition_counters.c`. The four zero bytes after those counters
  are still unidentified.
- `background2.cpp` combines the initializer and the update into one
  translation unit, as laid out in the original. It is not built; each
  function has its own unit.

## Clear bonuses

- `stage_point_items_collected` is a byte. Declaring it as a word, as in
  ReC98's reference listing, makes each bonus function three bytes shorter.
- Every `hud_points_put()`/`hud_5_digit_put()` call is a far call within
  the same segment, which TLINK turns into NOP / PUSH CS / near CALL (seven
  NOPs in `stage_clear_bonus()`, nine in `stage_allclear_bonus()`).
- `stage_allclear_bonus()` only gets the original relocation order when it
  is compiled after the two multiplier helpers and `stage_clear_bonus()`:
  Borland emits relocation records per 1 KiB of code, and the function's
  relocations straddle such a boundary. `bonus_full.cpp` therefore includes
  `bonus_helpers.cpp`.
- TH05 stores the multiplier descriptions as near pointers; TH04 uses far
  pointers. The rank `switch` in `stage_bonus_apply_modifiers()` compiles to
  an 8-byte jump table at the end of the function.
- The captions in `bonus_glyph_text.cpp` are strings of gaiji codes, printed
  with `gaiji_putsa()`; both are centered on the playfield at X = 224.

## All-zero data is ambiguous

The previous-stage miss/bomb counters (`bonus_previous_resources.c`) were
first placed at DS:18E4, where two zero bytes also matched the original.
The bonus functions actually read DS:1A62/1A63; DS:18E4 is the Boss
explosion frame counter. Matching zero bytes do not identify a variable;
always check the address used by the code that reads it.

## Unidentified bytes

The zero byte after `ST00.STD` (`std_filename.c`) is not part of the
filename array.

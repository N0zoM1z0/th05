# MAINE All Cast ending

`allcast.cpp` follows ReC98's `th05/end/allcast.cpp`. `lines.cpp`
(`screen_line_next_animate()`) is only forward-declared in ReC98 and was
decompiled from the original binary. The other files hold the ending's data:
the credit strings (`credits_data.cpp`), their display order and per-screen
line counts (`line_table.cpp`), the background file names and quarters
(`background_filenames.c`, `background_index.cpp`), the BGM name (`EXED`) and
two small counters and a page byte.

- `graph_putsa_fx_func--` in `lines.cpp` has to be a plain enum decrement.
  Assigning through a cast compiles to a load/decrement/store sequence that
  is three bytes longer than the original `DEC word ptr`.
- `allcast_lines_per_screen` holds the seven real counts and is indexed with
  `loaded_screen_id - 1`. ReC98's disassembly labels it one word earlier,
  overlapping the last `LINES` pointer; no dummy element exists.
- The compiler truncates identifiers to 31 characters, so the map shows
  `wait_flip_and_check_measure_targ` and `screen_fadeout_animate_and_advan`.
- Duplicate strings (the background names, repeated cast lines) are separate
  arrays in the original. Keep them as separate definitions.

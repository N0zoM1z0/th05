# Staff roll notes

The staff roll code is 20 functions at MAINE `D31F..E801`: the 17 scene
functions in `body/`, the two verdict bitmap transfers, and
`staffroll_animate()`. `staff_complete_context.cpp` compiles all of them in
their original order. `full.cpp` compiles only the 17 scene functions, and
the remaining `.cpp` files are standalone wrappers around the same bodies.
`staff.cpp`, `bitmap.cpp` and `bitmap_snap_segmented.cpp` are not part of the
build.

The small initialized variables live in the `staff_*.c` files, declared in
`state_publics.h`. The original has single alignment bytes between some of
them, so each group is a separate C file. `state_publics.h` must be included
before the C++ headers that redeclare these variables, so that they keep
their C linkage.

## What the original code generation requires

- **Compiling everything in one segment and translation unit.** Code goes out
  in LEDATA records of roughly 1 KiB, and relocations are emitted per record.
  Standalone builds of `staff_image_update_b()` and `staffroll_animate()`
  match every byte, but emit their relocations in a different order. In the combined file, the record splits fall where they
  did in the original.
- **The empty `if` branch** in the trail loops of `staff_particles_update()`
  and `staff_scene_render()`. Writing the sentinel check as
  `if(x == STAFF_CENTER_NONE) {} else { ... }` makes Borland reload the trail
  pointer after the comparison, as the original does. In
  `staff_particles_update()`, `i` must also be declared before `trail_center`
  to get the original stack slots, and `staff_scene_render()` must zero `i`
  before setting `trail_color`. Neither `-Z-`, `-O-`, class helpers, nor
  explicit expressions recovered the reload.
- **Increments inside conditions and `for` clauses**: `++staff_rain_cursor`
  inside the `if` of `staff_rain_spawn()`, and `(i++, column += direction,
  extent--)` in `staff_text_wipe()`.
- **Top before image pointer** in both image functions: copying `center_y`
  into `top` before taking `&cdg_slots[slot]` matches the original's
  initialization order.
- **Bitmap transfers as inline assembly** in `bitmap_hardware_context.inl`.
  The plain C++ versions (`bitmap.cpp`: 69 + 142 bytes,
  `bitmap_snap_segmented.cpp`: 58 bytes) are much larger than the original
  43 + 83 bytes. `bitmap_transfers.asm` reproduces the logic in TASM, but
  TASM32 encodes three XORs with the opposite opcode direction (`33` instead
  of `31`) and orders the two relocations differently; Turbo C++'s built-in
  assembler produces the original bytes. The compiler saves SI/DI itself, so
  the asm blocks must not push them again.
- The binder for the combined build has to subtract two from the SHARED
  offsets of the earlier functions, because SHARED word-aligns to `E802`
  after the controller ends at `E801`.

## Game behavior

- `staff_back_page` alternates between 0 and 1 every frame, and doubles as a
  0/1 term for motion that should only happen every second frame.
- The two image slots draw their picture on both VRAM pages, cover it with
  reverse black text cells, reveal it with a gaiji wipe on the text layer,
  and later hide it again with a wipe followed by black boxes on both pages.
  `STAFF_IMAGE_HOLD_MEASURE` (3996) keeps the last picture on screen.
- `staff_text_wipe()` uses gaiji 0x98 (opaque) to 0x9F (most transparent).
  The row buffer holds 40 gaiji of 16 pixels plus a terminator. The original
  differs from ReC98's older reading in `th05_maine.asm`: it uses a 46-byte
  frame with two locals, terminates at `row[width]`, and checks the 80-column
  limit while drawing.
- ZUN quirk: The image cover loops and the wipe's row loop are inclusive and
  cover one more row/column than necessary.
- ZUN quirk: `staff_rain_spawn()` never spawns particle 63.
- Without BGM, the music measure is approximated as `staff_frame / 22`.

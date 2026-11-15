# Dialog notes

MAIN's dialog code is one contiguous segment, `[139F5,140C4)`, in this order:
the two STD-to-boss callbacks, `dialog_box_put()`, `playfield_copy_front_to_back()`,
`dialog_face_unput_8()`, `dialog_box_wipe()`, `dialog_box_fade_in_animate()`,
`dialog_op()`, `dialog_run()`, then the tail (`dialog_animate()`, the face
loader, `dialog_exit()` and the Ex-Alice sprite override). The .TX2 loader
(`file.cpp`) sits right before it. ReC98 covers the same code in
`th04/main/dialog/shared.cpp`, `th05/main/dialog/dialog.cpp` and
`th05/formats/dialog.cpp`.

Most bodies live in `.inl` files and are built by several `.cpp` files,
because some functions only compile to their original bytes in a particular
translation-unit context.

## Translation-unit context matters

- **`dialog_op()` switch-table alignment.** The original has one zero byte
  between the function's `RET 2` and its 30-byte jump table. Turbo C++ only
  emits it when everything from `std_update_done()` up to `dialog_op()` is in
  the same translation unit, which is what `opcode_full_context.cpp` does.
  Compiled alone (`opcode.cpp`), with only the box functions before it
  (`runtime.cpp`), or with only the graphics functions before it, it comes out
  one byte short. Things that did not help: `-a`/`-a1` before or after the
  header, a separate segment for the callbacks, explicit reserved cases, `-G`
  (468 bytes). `-a4` and `-a8` are rejected by Turbo C++ 4.02, and `-a2`
  before `runtime.hpp` breaks the packed 5-byte `tx2_op_06_params`.
  `TCC -S` followed by TASM gets the bytes right but writes the fixups in
  ascending instead of the original order.
- **`dialog_run()`** compiles to the right bytes in the full-context build
  too, but its fixup records come out in a different order there, so it is
  matched by `run.cpp` on its own.
- **`dialog_exit()`** gets its switch-table alignment byte only when compiled
  alone (`exit.cpp`). In the combined `tail.cpp` it is one byte short, which
  also shifts the following Ex-Alice function by one byte (its own bytes are
  still correct).
- **`dialog_animate()`** calls `GameExecl()` far. The original linker turned
  that call into `NOP / PUSH CS / CALL near` because both are in the same
  code segment; `#pragma samecodeseg GameExecl` in `animate.cpp` tells the
  compiler so. In `tail.cpp` it stays a 5-byte far call. The callback in
  `boss_transition_body.inl` gets the same relaxation for its call to
  `dialog_animate()`.
- The callbacks' first declaration in `boss_transition.hpp` fixes their code
  segment; `TH05_DIALOG_OPCODE_FULL_CONTEXT` selects `DIALOG_RUN_TEXT` for the
  full-context build.

## Code generation details

- `dialog_op()` must read file names through `const unsigned char far *`.
  With plain `char`, the `'$'` comparison gets a sign extension.
- The three EGC/GRCG functions are pseudo-register code. The inline
  instructions are there because Turbo C++ picks a different encoding for the
  pseudo-register version: `mov bx, ax` (89 C3, not 8B D8), the two
  `add ax, dx` and the `mov di, ax` in `dialog_box_put()`, its
  `dec dx / jne` row loop (the compiler copies DX to AX to test it), and
  `test bx, 7`, which the compiler would shorten to `test bl, 7`.

## Data

`dialog_fn` (DS:1ECC) points at `"_DM00.TX2"` inside the resource bank, so it
is a C pointer initializer with a relocation, in its own file
(`resource_pointer.c`). `BOX_TILES` (DS:1ED0, 24 bytes) follows, then the
133-byte bank `dialog_resources` (DS:1EE8). `resources.c` and `box_tiles.c`
must be compiled as C.

## Open question: `dialog_sequence_id`

The dialog code reads `dialog_sequence_id` at DS:1EE8, the bank's first field
(that is also where ReC98's `th05_main.asm` places `_dialog_sequence_id`).
`sequence_initial.cpp` instead defines a variable of that name for the zero
byte at DS:1F6D, right after the 133-byte bank, which is most likely the
bank's word-alignment padding. Both match their bytes in isolation, but a
whole-program link would resolve `dialog_sequence_id` to DS:1F6D.

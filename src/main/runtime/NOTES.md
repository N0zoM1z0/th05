# MAIN runtime: notes

Things learned while matching this directory's code to MAIN.EXE that the
source comments only summarize.

## The startup module (`stage_complete_context.cpp`)

`main()`, `gameplay_loop()`, `gameplay_session_init()` and
`stage_session_init()` are adjacent in MAIN and form one original module.
`stage_session_init()` only compiles to the original bytes inside that
complete translation unit:

- Built alone, it is one byte short: the zero byte before its word-aligned
  switch tables is missing, because the function then starts at an even
  offset. After the three preceding functions it starts at an odd offset.
- Built after only `gameplay_loop()` and `gameplay_session_init()`, the byte
  is there, but the fixup at +56 is emitted first instead of last. With
  `main()` included as well, all 23 fixups come out in the original order.
- The empty `#pragma codeseg` lines at the top have to declare the four
  main_01 segments, then `SHARED`, then the three main_03 segments.
  Otherwise `SHARED` is absorbed into a neighboring group, and the CS
  operands of far calls change.

`stage_session_context.hpp` is `stage_session_init.hpp` minus the
`snd_load_func_t` enum, which `main.hpp` already defines in that unit.
`stage_session_init.hpp` is also a hashed semantic input of an ASM family
in `config/asm_families.toml`, which is why it wasn't changed to make the
enum optional instead.

## Same-segment far calls

Several far functions (`GameExecl()`, `hud_put()`, `tiles_activate()`,
`shot_level_update()`, `hud_lives_put()`, `hud_bombs_put()`,
`playperf_raise()`) are in the same physical code segment as their callers.
TLINK then rewrites the five-byte far call into `NOP / PUSH CS / CALL near`,
which is what the original contains. Borland's `#pragma samecodeseg` after
the prototype, together with linking caller and callee into the same
segment, reproduces this. Being in the same group alone is not enough
(`demo/demo.hpp`). Never declare these functions near instead.

## Frame counter in `gameplay_loop()`

The original updates `stage_frame` and the four modulo bytes with
`mov ax, stage_frame / mov dx, ax / inc ax / mov stage_frame, ax /
and ax, 0Fh`. The DX copy is never used, and the mask is word-sized. Plain
C attempts all failed: `++stage_frame & 15` and `% 16` (442 bytes instead of
445, byte-sized mask), `(stage_frame++ + 1) % 16` (444), and a named
`previous_frame = stage_frame++` (451). The pseudo-register version in the
source matches; assigning DX before AX swaps the first two instructions.

## Smaller findings

- `stage_state_init()`: `hitshot_next_free_id = shots_alive_count = 0`
  has to be one chained assignment. Two separate zero stores are 4 bytes
  longer.
- `gameover_gaiji_bank.c`: with `const` text arrays, Borland emits the
  non-const erase string first and the order no longer matches. All six
  arrays are therefore non-const.
- `frame_counter_data.cpp` includes no header. Including `handoff.hpp`
  pulled in code segment declarations that made TLINK fail with
  "Group MAIN_01 exceeds 64K".
- `continues_used` is the lowest byte of the BCD `score`; the original
  accesses the same address under both names.
- The three `maine` filenames (`end_binary_names.c`,
  `score_handoff_names.c`) and the two erase strings are separate copies in
  the original. They must not be merged.

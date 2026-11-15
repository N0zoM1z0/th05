# MAIN score file notes

These files handle MAIN's access to GENSOU.SCR: loading and saving the
section of the current character and rank (`current_*.inl`), loading the top
score for the HUD (`hiscore_load.cpp`) and entering a score on continue
(`continue_enter.cpp`, `continue_raw.cpp`). ZUN wrote them with Turbo C++
pseudo-registers and raw INT 21h calls; ReC98's `th05/main/hiscore.cpp`
documents the same functions. The section codec is hand-written ASM, see
`scoredat_code.md`.

## Code generation

- `scoredat_load_for_cur()` only compiles to the original 55 bytes with `-O-`
  (`current_load.cpp`). With optimization, the compiler turns the early
  `JNC / RET` after a failed open into a jump to the final RET, one byte
  shorter. Both an early return and an if/else produce that. `current.cpp`,
  which compiles load and save together without `-O-`, therefore does not
  match for the load function.
- `hiscore_load.cpp` declares `scoredat_load_for_cur()` itself. Including
  `current.hpp` would put the large SHARED code segment into `main_01`, which
  then exceeds 64 KiB.
- `continue_raw.cpp` uses the 386 `MOVSD` instruction, which Turbo C++'s
  built-in assembler rejects (also when written as `movs dword ptr`). The unit
  uses the `tcc-s-tasm32` pipeline: TCC writes assembly with `-S` and TASM32
  assembles it unchanged.
- The two strings in `resource_names.c` are kept in one struct so that they
  stay in their original order.

## Game behavior

- In TH05, `hiscore_continue_enter()` only enters the score in turbo mode, and
  it does not reload the score file first as TH04 does.
- The continue entry stores the stage as a gaiji digit starting at 1; the
  Extra Stage is stored like stage 1.
- ZUN landmine: `scoredat_save_cur()` does not check whether opening the file
  succeeded.

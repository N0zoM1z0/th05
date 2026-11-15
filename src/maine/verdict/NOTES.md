# Verdict notes

The verdict code is ten functions at MAINE `C5E7..D31F`: the four number
formatters, the bonus, both comment selectors, `verdict_main()`,
`verdict_animate()` and the stage score tally used by the staff roll.
`full.cpp` compiles all of them in their original order and is the build
that matches. The other `.cpp` files are standalone wrappers around the same
`body/*.inl` files.

## What the original code generation requires

- **One translation unit.** `verdict_animate()` and `verdict_main()` have
  relocations in a non-monotonic order. Borland splits a segment's code into
  LEDATA records of roughly 1 KiB, and the fixup order follows those splits.
  Compiled alone, the bytes match but the relocation order does not.
- **`register` on both coordinate locals** of
  `skill_apply_and_graph_percentage_put()`, as in TH04. Without them, the
  function grows by six bytes because `top` gets copied into a stack local.
- **`int` bonus constants.** `verdict_apply_bonus()` came out one byte short
  when its bonus values were written as `2500L` etc. Only the miss/bomb factor
  `200L` is a long.
- **`char verdict_rank_glyphs[5][8]`**, mutable and with the default data
  distance. A `const near` declaration produces the same values with the
  `PUSH DS` in a different place.
- **Separate string objects.** The original has duplicate strings as distinct
  objects ("最終得点" twice, "％" twice, "点" twice, "．" twice, "回" twice).
  Identical const strings in one translation unit may be merged, so the
  duplicates are spread across `metric_ui_data.cpp`, `score_ui_data.cpp` and
  the two C struct banks in `punctuation_data.c` / `counter_units_data.c`.
- **`state_data.hpp`** repeats the state declarations without the function
  declarations of the other headers. Their `#pragma codeseg` lines add an
  empty SHARED segment to the object, which then gets grouped into GROUP_01.
  It also includes `resident.hpp` for the `bool` typedef, which TC4 lacks.

## Game behavior

- Skill is the sum of five percentages (stage completion, enemies, items,
  point items, bonus) minus the slowdown percentage, divided by 12, plus a
  quarter of the stage completion rate. It then gets high score, difficulty,
  starting lives/bombs, game speed, miss and bomb adjustments, and a 7/8
  penalty for game overs, before being clamped to a per-difficulty maximum.
- Reaching any ending counts as 100% stage completion.
- The skill value is only shown if fewer than half of all frames were slowed
  down. Otherwise, the screen shows "？？？？？？点" and a warning.
- `_ude.txt` consists of 30-byte records. Records 0-25 rate the skill value,
  and records 26 and up hold the second comment line chosen by
  `verdict_comment_id()`. Values of 1,500,000 and above skip the seek and get
  record 0 from the freshly opened file.
- `verdict_comment_id()` compares `resident->unknown` (offset 12, purpose
  unknown) as an unsigned byte.
- ZUN quirk: `skill` is unsigned, but all of its divisions are signed.
- The rank glyphs use TH05's bold gaiji alphabet starting at `0xAA`, where M
  and N are in alphabetical order (TH02's font swaps them).

# MAINE high-score file

`end.cpp` holds MAINE's copy of the TH04/TH05 score-file lifecycle
(`scoredat_recreate()`, `hiscore_scoredat_load_for()` and
`hiscore_scoredat_save()`, ReC98 `th04/hiscore/end.cpp`). The score record
layout is shared with OP and comes from `src/op/hiscore/view.hpp`.

- `hiscore_scoredat_load_for()` takes a word-sized `int` player character
  (ReC98's `playchar2`), even though the global `playchar` is one byte. The
  original pushes a full word.
- Every file call uses its own copy of `"GENSOU.SCR"`: MAINE has four separate
  writable arrays (`SCOREDAT_FN`, `SCOREDAT_FN_0`..`_2`, defined in
  `resource_strings.c`), not OP's single pooled literal. The `#undef
  SCOREDAT_FN` / local `extern` dance in `end_body.inl` selects the right one.
- The two codecs, `scoredat_decode()` and `scoredat_encode()`, live in the
  registration module (`src/maine/registration/full_context.cpp`) because they
  sit there in the original link order. Their byte rotation is one inline
  `ROR` on a value kept in `AL`. Turbo C++ 4.0J's `_crotr()` compiles to a far
  library call, and a shift/or expression compiles to `MOV/SAR/SHL/OR`, so
  neither reproduces the original.
- `resource_strings.c` is compiled as C. Its two identical slow-mode warnings
  are separate arrays in the original as well.

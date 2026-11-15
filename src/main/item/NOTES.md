# Item code notes

The item code follows ReC98's TH04 item sources (`th04/main/item/`), with
TH05's 40-item pool, 32-dot splashes and changed scoring.

## Translation units

- `family.cpp` compiles `items_init()`, `items_add()`, `items_miss_add()`,
  `item_extend_check()`, `item_collect()` and `item_miss_penalty()` as one
  unit, with `#pragma option -a` as in TH04. Compiled on its own,
  `item_collect()` is one byte short (619 instead of 620: the zero byte
  before its switch jump table is missing) and its relocations come out in a
  different order. At its original offset after the preceding functions,
  both match.
- `splash_init.cpp` and `dot_render.cpp` are plain C alternatives that are
  not built. The intrinsic `memset()` produces 24 bytes (PUSH DS / POP ES and
  a different register order) instead of the original 26, also with `-G`.
  The C dot renderer produces 42 bytes instead of 28; the game uses
  `splash_dot_exact.asm` (see `splash_dot_exact.md`).

## Code generation details

- `items_add()`: the drop-cycle parity test is `item_drop_cycle & 1`. A
  signed `% 2` compiles to IDIV and makes the function 8 bytes longer.
- `items_update()`: `PlayfieldMotion::update_seg3()` returns X in AX and Y in
  DX. Storing the result in a local gives 248 bytes instead of 241. Reading
  AX/DX directly but computing the pickup distance in ordinary C gives 235
  bytes, and the compiler loads the player's X into AX, overwriting the
  item's X. The current version computes the distances in BX, with the two
  subtractions as inline asm to get the original `29 C3` / `29 D3`
  encodings.
- `item_splashes_init()` uses inline `xor ax, ax`, since the compiler's own
  zeroing is encoded as `33 C0` instead of `31 C0`.
- `stage_point_items_collected` is a byte that is incremented without
  saturation. ReC98's reference listing has a saturating word.

## Open questions

- `DREAM_SCORE_PER_ITEMS` is declared unsigned, as in TH04; all its values
  are non-negative, so the binary doesn't tell.
- Unidentified bytes: the byte after `item_drop_cycle`, the alignment byte
  after `pointnum_times_2`, and the byte after `items_pull_to_player`.

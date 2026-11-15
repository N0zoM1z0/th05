# Play performance and rank/character selectors

MAIN `CF7A..CFC6` is one 76-byte assembly module with four entry points,
following ReC98's `th04/main/playperf.asm`, `th04/main/select_for_rank.asm`
and `th05/main/select_for_playchar.asm`:

| Function | Start | Notes |
| --- | --- | --- |
| `PLAYPERF_RAISE` | `CF7A` | adds, clamped to `playperf_max` |
| `PLAYPERF_LOWER` | `CF94` | subtracts, clamped to `playperf_min` (signed `JGE`) |
| `select_for_playchar(int, int, int, int)` | `CFAC` | C++ linkage; picks one of four words by `playchar` |
| `SELECT_FOR_RANK` | `CFB2` | picks one of four words by `rank` |

All four are far. The performance functions are Pascal and read their byte
argument from `SS:[SP+4]` through BX. The two selectors share their tail from `CFB5` on,
which is why they can't be written as two separate C functions. `EVEN`
produces the original alignment NOPs at `CF93` and `CFB1`.

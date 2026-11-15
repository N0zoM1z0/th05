# EMS cache (MAIN)

`ems.cpp` holds the four EMS functions at MAIN `[B826,BAD2)`, ported from
ReC98's `th05/ems.cpp` (and `th04/main/ems.cpp`):

| Function | Start | Bytes |
| --- | --- | ---: |
| `ems_allocate_and_preload_eyecatch()` | `B826` | 155 |
| `bomb_bg_load__ems_preload_playchar_cdgs()` | `B8C1` | 267 |
| `ems_preload_boss_faceset()` | `B9CC` | 154 |
| `eyecatch_animate()` | `BA66` | 108 |

## Behavior

- The faceset preloads copy CDG slots into EMS from slot 2 (offset 100000) or
  slot 8 (offset 200000) until they reach a slot without an alpha plane, and
  free each slot after copying. ZUN landmine: the walk is not limited to the
  faceset's slots or EMS region, and every slot is assumed to have the first
  slot's bitplane size.
- The four-plane size is multiplied in 16 bits before it is converted to the
  `long` that `ems_write()` takes, as in the original.
- The EMS handle name is `KAIKIEMS` in this executable, although ReC98's TH05
  macro says `GENSOEMS`. `EMS_NAME` stays an external symbol.

## Code generation

- **Switch table alignment.** `bomb_bg_load__ems_preload_playchar_cdgs()` has
  a word-aligned, 8-byte jump table at `B9C4`, preceded by a zero padding byte
  at `B9C3`. Without `#pragma option -a2` the unit is one byte short. The
  pragma comes after all struct definitions so that their layout is
  unaffected.
- **Fixup order of `ems_preload_boss_faceset()`.** Compiled from `ems.cpp`
  alone, the boss function matches all 154 bytes, but its four fixups come out
  as `[133,114,71,24]` instead of the original `[71,24,133,114]`. Turbo C++
  splits its LEDATA/FIXUPP records depending on how much code precedes the
  function in the segment, and only the full 3,226 bytes from `main()`
  onwards give the original split. `ems_boss_full_context.cpp` therefore
  compiles copies of all those functions in one translation unit; the other
  three EMS functions are verified from `ems.cpp`.

  Shorter prefixes all failed: the 1,400 bytes from `stage_runtime_init()`
  keep the right start and bytes but give `[133,114,71,24]`; 1,226 bytes give
  `[24,133,114,71]`; 1,178 bytes (without `stage_session_free()`) give the
  right order, but start at an odd address, so the table's padding byte is
  lost and the function starts one byte early. `-y`, `-a1`/`-a16`, extra
  `codeseg` pragmas at function boundaries, and `tcc -S` + TASM32 (which
  sorts all fixups in ascending order) did not help either.
- **SHARED segment in the combined unit.** The compiler emitted an empty
  `SHARED` segment definition grouped into MAIN01. Putting the external
  SHARED functions into that same segment inserted 14 bytes of alignment and
  moved every far call and data address; the link scaffold therefore defines
  them in a separate `EMS_SHARED_PROVIDER` segment.

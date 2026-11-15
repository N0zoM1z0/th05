# Yumeko

Yumeko's update function, attacks and swords (MAIN, segment `B5_UPDATE_TEXT`
in group `main_03`; the sword renderer is in `main_01`).

## Translation units and code generation

- `attacks_context.cpp` compiles the sword renderer, `swords_add()`,
  `swords_update()` and the seven attacks from `patterns.cpp` to
  `laser_swords.cpp` as a single translation unit, in their original order.
  The aimed-sword and laser/sword attacks are only exact in this context:
  compiled on their own, their bytes match but their relocations come out in
  a different order (`[329,309,203,71]` instead of `[71,329,309,203]`, and
  `[402,382,232,72]` instead of `[232,72,402,382]`). The preceding code
  determines where Turbo C++ splits the OMF `LEDATA`/`FIXUPP` records, which
  in turn decides the fixup order. Each file still compiles on its own;
  `TH05_YUMEKO_COMBINED_CONTEXT` only suppresses the per-file `-zC`/`-zP`
  options.
- `swords_update()` reads the `Point` returned by `update_seg3()` directly
  from DX:AX. The two empty `optimization_barrier()` calls emit no code but
  keep the clip and collision `continue`s from being merged into one jump.
- `angle_call.hpp` calls `player_angle_from()` through a function pointer
  that takes plain words. With the `Subpixel` signature, the
  `x.v + to_sp(64)` argument of the aimed-sword attack gets stored in a
  temporary first, which makes the function 3 bytes too long (357 instead of
  354).
- `update.cpp` needs `#pragma option -a2` for the word-aligned phase switch
  table (one alignment byte at `1FA3A`, then 11 table words). The pragma must
  come after the shared headers.
- `gather_add_only_3stack()` takes `(frame, 7, 6)`, and `select_for_rank()`
  takes its values in Easy/Normal/Hard/Lunatic order. Both are easy to get
  backwards when reading the pushed DWORDs in the disassembly.
- Borland truncates external names to 31 characters, so the EXTDEF for
  `yumeko_pattern_counterrotating_spreads` is truncated. Keep any new macro
  name in these files unique within its first 31 characters as well.

## Boss scratch bytes

`final_ring_scratch.hpp` describes the 16 `boss_statebyte` bytes:

- `stage5_setup()` sets byte 0 (aimed-sword spawn interval, 20/10/6/6 by rank)
  and byte 1 (laser spawn interval, 48/32/24/24) before the fight starts.
- Bytes 12-15 are reused by every attack: volley length, speed-up flag or
  sweep round, and the two aim/rotation angles or the sweep and final-ring
  state.

## Gameplay

- Each mobile wave consists of 20 attacks. The first one is selected when
  entering the phase; the following 19 alternate between the first two
  entries of the wave's bank in `schedule_data.cpp`. The 20th reposition ends
  the wave without a hit test. The phase-5 bank has 12 slots, of which only
  the first two are used.
- The final ring fires 74 rings, on frames 32, 48, ..., 1200. On a timeout at
  frame 1200, `defeat_bonus` stays false: it shares its byte with
  `patterns_seen`, which the final approach clears.
- The sword sweep doesn't reset side, bullet speed or aim between cycles. The
  first cycle fires 4 bursts of 12 bullets (speeds 16-104); later cycles
  fire 5, the first of them silently and at the previous angle.
- ZUN quirk: the laser/sword attack's Lunatic volley window (48 frames) is
  shorter than Hard's (52).

# Sara (stage 1): notes

`sara.cpp` follows ReC98's `th05/main/boss/b1.cpp` closely. `foreground.inl`
and `pattern_tables.cpp` hold her foreground renderer and the phase 2/3
pattern table.

- **Byte-sized angle updates must use literal steps.** With an enum constant
  instead of a literal, Turbo C++ adds directly to memory instead of going
  through AL like ZUN's code. This affects the spiral angles (`+0x06`/`-0x06`),
  the two laser angles (`+= 0x01`, `-= 0x01`) and the corridor spread angle
  (`+= 0x0E`). Using names for these steps made the unit 18 bytes shorter.
- `#pragma option -a2` before `sara_update()` word-aligns its 5-entry phase
  switch table, as in ZUN's code. The byte before the table is alignment.
- `boss_statebyte[10]` is the previous pattern in both phase 2 and phase 3.
  The entrance sets it to `0xFF`. Phase 2's timeout does not reset it, so
  phase 3's first pattern can't repeat phase 2's last one.
- The phase 2 flight delay goes 64, 52, ... 16, 4; the phase 3 pattern length
  goes 80, 104, ... 176, 200. Both conditions only check the current value,
  so neither stops exactly at 12 or 180.
- In the final laser corridor, the left laser stops turning at angle `0x4A`
  on frame 210, long before the 1300-frame timeout. The turn interval grows
  at frames 64, 128, 150 and 180.

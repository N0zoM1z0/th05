# Bullet generation clipping

`clip.cpp` adapts the semantic C++ in nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/bullet/clip.cpp`. The function prevents spawning a bullet that would
not complete its 16-frame decay before an active clear ends, rejects centers
outside the expanded playfield, detects a player collision, and tunes speed
unless fixed-speed mode is active. The original behavior still spawns a bullet
on player collision; it sets the hit flag without returning early.

The complete original function occupies load offsets `[173DE,1743C)`: 94 bytes,
32 contiguous instructions, no padding, CODE data or MZ fixups. SHA-256:
`a8742468f00e45cf56fd0e1902feb0f758bc880540bd72e9af82904604b71e52`.
Every local branch lands on an instruction boundary, including the shared early
true return. The final false return ends the extent. The source retains signed
Q12.4 coordinates, unsigned collision tests and genuine register intrinsics.

The original main_03 frame is `1527`; the group offset is `216E`. The real
fastcall helper `@playperf_speedtune` receives/returns byte speed in AL at load
`171EA`. Globals use original DGROUP offsets: `player_pos=36D2`,
`player_is_hit=36F3`, `bullet_clear_time=3F97`, `group_fixedspeed=41E0`, and
`bullet_template=577E`. Existing full 12-byte motion and 14-byte template types
are reused without modifying any accepted shared header.

The symbol-only binding context emits no external implementation. Two isolated
producers in `.analysis/unit-replays/bullet-clip-d` pass complete raw/fixup
comparison and normalized OMF determinism. A compiled change from the decay
threshold 17 to 18 is rejected. This reuses the unchanged tool identity receipt
and does not rebuild previous units. Public acceptance independently rechecks
the saved artifacts. Whole-program linkage remains outside this scope.

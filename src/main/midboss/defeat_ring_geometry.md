# Stage midboss defeat: exact 16-sprite revolving ring

The original independently accepted **170-byte** near-C++
`midboss_defeat_render()` now uses `defeat_ring_geometry.hpp` to
name its full native motion and clip behavior. The ring radius is
`midboss.phase_frame << 4` subpixels, capped at **48 pixels**. Once
it reaches that cap, the physical one-byte C public
`midboss_defeat_angle` increments by one unit each update. Each draw
renders **16 actual 16-pixel-spaced angle positions**, incrementing
the original shared angle by `0x10` after each sprite, with its
original polar X/Y vector and direct PC-98 drawing APIs. Clipping
uses 16-pixel margins around the genuine 384×368 playfield, then
converts Q12.4 X to pixels with the real 16-pixel display offset.

The original one-byte initialized DATA is at MAIN `209D:1A60`,
source-owned by `defeat_rotation_angle.c` and imported through the
same C-linked header as the original 1619-byte bullet and 88-byte
HUD consumers. No second rotating-angle object exists. The actual
170-byte original function and its compiled 0x10→0x11 turn-step
negative pass the source-current native six-scope replay:
`.analysis/unit-replays/gpt-web-bullet-hp-midboss-exalice-native-publics-b/receipt.json`.
The separate original initialized byte and its compiled 0→1 negative
pass the current producer
`.analysis/unit-replays/gpt-web-defeat-angle-native-C-public-after-ABI-a/receipt.json`.
The original physical opcode stream, sprite resource and ordered
relocations were not rewritten or counted twice. No full-game cold
replay was run.

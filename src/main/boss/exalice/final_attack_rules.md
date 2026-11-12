# EX-Alice terminal Cheeto, spiral-gather and final fan attack protocol

The complete original terminal attack cohort has four separately accepted
natural C++ functions: cross Cheetos (143 bytes), turning Cheetos (109),
spiral gather (334), and the final expanding fan (223). The readable
`final_attack_rules.hpp` now names genuine source-level clocks, origin
offsets, sprite patterns, angular reflection, bullet stack/spread sizes,
HP scaling and player-aimed Cheeto behavior. It introduces no storage,
copy of rendered pixels, inert optimizer barrier or target instruction
sequence; all original state stays in `boss`, `cheeto_template`,
`bullet_template`, `gather_template`, `exalice_sweep_x` and the original
three scratch bytes.

The **cross attack** fires an aimed nine-bullet spread every sixteen
frames at 3.5 pixels/frame. Every 64 frames it also fires a color-11
Cheeto at speed three, alternating the player-angle offset between
+0x20 and -0x20 on a 128-frame period. It completes at frame 256.
The separate **turning Cheeto** fires every eight frames at speed four,
alternates the signed ±0x40 player-angle offset every sixteen frames,
updates the original 32-frame random flystep and completes at frame 128.

The **spiral gather** begins at frame 64 with offset 104 pixels,
three-bullet spread with eight angular steps, and real initial Cheeto
and bullet angles. Until frame 128 the original gather uses a 256-pixel
radius, alternating ±2 angle steps every sixteen frames. Its next
phase shrinks the radius to 128 and emits mirrored paired fixed-speed
shots every two frames. Every 32 frames it changes the original
bounded angle ramp in scratch bytes 13–15, returning true only when
that countdown has finished and `exalice_sweep_x` has captured the
actual player X coordinate. Its live 334-byte source body is shared
by the full four-function context and the independent standalone
`-S` compiler-assembly producer, not replicated or replaced.

The **final fan** charges at frame 64 (sprite 181), then after frame
128 fires two paired spreads on even frames while rotating the source
angle. Bullet speed and the Boss's horizontal oscillation radius both
scale with the live remaining wave-4 HP relative to the original
3,400-HP boundary. The literal 16-subpixel/pixel conversion, modular
signed arithmetic, `SinTable8` lookup and byte-rotation writebacks are
unaltered by the source names. Its true paired shots and original
sound are still emitted in the same order.

The native DATA, public addresses and near/far callback references
remain external; all four owners have no unreviewed interior holes.
The three ordinary C++ callbacks were compiled in two independent
native Borland rounds, including their original CODE bytes, function
boundaries and ordered fixups, with a rejected change to Cheeto speed:
`.analysis/unit-replays/gpt-web-exalice-final-weapon-cxx-a/receipt.json`.
The 334-byte spiral callback was separately compiled in its required
`TCC -S → TASM32` lane, with the genuine original `[86,256]` relocation
order and a rejected radius 256→257 mutation:
`.analysis/unit-replays/gpt-web-exalice-final-weapon-spiral-a/receipt.json`.
These functions were already accepted; this pass adds source meaning
without duplicate CODE credit or a whole-program cold replay.

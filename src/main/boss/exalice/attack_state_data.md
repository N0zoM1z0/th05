# EX-Alice laser and spiral state: complete near initialized DATA

The original MAIN load-module `[22368,2236C)` has two adjacent native 16-bit
objects in DGROUP, with no alignment or filler bytes:

| DS offset | Symbol | Original value | Native owner/consumer |
| --- | --- | --- | --- |
| `1998` | `exalice_laser_slot` | `0000h` | 645-byte fixed-laser fan and its slot increment/mask/reset |
| `199A` | `exalice_sweep_x` | `0C00h` (192 pixels in Q12.4) | 334-byte spiral/gather attack and its player-X capture |

The exact existing C++ declarations are `int exalice_laser_slot` in
`laser_patterns.hpp` and `subpixel_t exalice_sweep_x` in
`final_patterns.hpp`. Both types occupy one genuine 16-bit word. The laser
fan reads the word at DS:1998, increments it for successive fixed lasers,
masks its slot count, and resets it at the final timer frame. The spiral
pattern reads DS:199A into its bullet/gather X centers, and writes the
player's X coordinate back when the pattern ends. Those references occur in
the already accepted exact functions; neither symbol is inferred from zero
bytes alone. The original nonzero seed is the horizontal center of the
384-pixel playfield (`192 * 16` subpixels), retained as the named existing
`EXF_FAN_CENTER_X_PX` game rule.

`attack_state_data.cpp` supplies exactly these two natural C++ initializer
statements. Its native Turbo C++ 4.02 object contains a **complete 4-byte
`_DATA` contribution** matching `00 00 00 0C`, with the original empty
ordered relocation stream. Two independent TCC/TLINK producers verify the
complete extent, original MAP placement and valid OMF. The compiled negative
changes the initial X by one pixel and fails the raw byte comparison.

Receipt:
`.analysis/unit-replays/gpt-web-main-exalice-laser-sweep-data-a/receipt.json`.
This adds **four game-authored C++ semantic DATA bytes** but no instruction
bytes. Both previously accepted large Boss attack code owners retain their
original evidence and are not rebuilt; their real DS bindings provide the
state provenance. No neighboring EX-Alice pattern table, unknown byte or
whole-executable ownership is included.

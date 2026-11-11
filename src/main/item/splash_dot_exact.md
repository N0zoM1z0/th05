# Item splash dot: exact original-register renderer

The complete near `item_splash_dot_render` helper at MAIN `[E152,E16E)`
receives signed screen X in AX, VRAM Y in DX, and its writable graphics plane
in ES. It computes the 80-byte PC-98 row displacement as Y×64 + Y×16,
adds signed X/8, then places the selected pixel bit into ES memory. The
source preserves the original 8-bit mask and the caller's segment instead of
adding a new page switch, clipping check or sprite allocation.

This source reconstructs the dedicated original-register assembly in pinned
ReC98 `th04/main/item/splash_dot_render.asm`. The 28-byte native procedure
has no stack frame, no relocation sites, no switch tables and no padding.
Ordinary C++ arithmetic previously compiled to 42 bytes, so its negative
result is not reclassified as exact C++. The 131-byte accepted splash loop
already calls this helper but remains a separate source owner.

The focused receipt at
`.analysis/asm-replays/gpt-web-main-item-splash-dot-b/receipt.json` passes
two fresh TASM32/TLINK producers, complete 28-byte equality, correct original
CS/DGROUP placement, empty ordered relocations and a rejected mutation of the
pixel-bit mask. The instruction/origin review is
`.analysis/gpt-web-item-splash-dot-native-review.json`. All 28 bytes are
credited as reviewed original-register ASM, with no padding or DATA credit.

# Stage5 midboss renderer candidate

This natural C++ owner comes from ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05/main/midboss/m5.cpp`. It reuses the canonical complete22-byte midboss,
Motion and geometry definitions unchanged. Missing convenience operations are
expanded as ordinary signed field arithmetic; there is no assembly or surrogate
geometry class.

Two original101-byte functions have the same diagnostic shape. Identity comes
from the actual original stage setup assignments, not masked matching:

- Stage5 at `14880` writes near callback `2F7F` to DS:C4B8, selecting
  `AE1:2F7F = DD8F`.
- Extra stage at `14A0D` writes `2F1A`, selecting `DD2A`.

Therefore this owner covers only `[DD8F,DDF4)`,101 complete instruction bytes,
with two original ordered loader fixups and no tables/padding. `[DD2A,DD8F)`
is the unaccepted Extra-stage twin; its matching shape transfers no credit.
The function's final RET is at DDF3. No source exactness is claimed yet.

The real midboss is at DS:5AA4: sprite+16, phase+17, damage+20. The64-pixel sprite
clipping threshold is zero because the real rolling margin is32. Screen-left
uses signed arithmetic shift by4; VRAM-top calls the genuine near Pascal
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 at DF28 with signed y minus256 subpixels. Normal
and white-flash sprites use the actual far Pascal master.lib entries
0000:2FE0/0000:2E1A; flashing clears the damage byte. Phase254 calls the real
near midboss_defeat_render at132D3.

Suggested alias `th05/mb5rend.cpp`, segment `M5_RENDER_TEXT`, group `main_01`,
GAME5/BINARY M, ordinary pinned large-model flags and BP enabled. The binder
contains only true external addresses and no stack/body/data values. A meaningful
negative changes the flash reset assignment from0 to1, making the white flash
persist. Private boundary metadata, binders and suggested entries are under
`.analysis/bombanim-midboss5-*`.

`main-midboss5-render-a` now passes two independent fresh producers, complete
raw-byte comparison, original ordered fixups, deterministic OMF and the
reviewed compiled gameplay mutation. Source state and foreign API bodies
remain uncredited.

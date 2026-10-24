# Growing and shrinking circles

Natural C++ from pinned ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th04/main/circle.cpp`, specialized to TH05's real eight-circle pool. The
maintained TH04 circle source corroborates the semantics. Its acceptance does
not transfer. Each full ten-byte state retains byte flag/age, two signed pixel
coordinates and signed radius/delta. Subpixel centers use signed division by
16 and are translated by the real playfield origin (32,16).

The complete original MAIN contribution is `[E28A,E38B)`, 257 instruction bytes:
growing `[E28A,E2D6)` (76), shrinking `[E2D6,E322)` (76), update `[E322,E358)`
(54), render `[E358,E38B)` (51). Both Pascal far add functions clean four bytes;
the two update/render functions return near in original group `0AE1`.
All branches lead to observed instruction starts; no table or padding exists.
The one original ordered segment fixup is at unit-relative 242 on the far
`GRCG_CIRCLE` call (`0000:10AE`). The near color-register helper is original
load `C204`. External original DS `209D` globals are the circle pool at `9EB4`
and byte color at `41DA`; neither storage nor foreign bodies are reproduced
by the context scaffold or credited here.

`main-circles-b` validates two independently compiled producers, all raw bytes
and the original ordered fixup. Its compiled negative changes the true lifetime
constant from 16 to 15, changing shrinking-radius initialization and removal
age; the oracle rejects the changed output. The initial unbuilt scaffold lacked
explicit CS assumptions for foreign labels; correcting those declarations
preceded the successful cold replay and did not alter semantic source.

Updates preserve the original deferred removal and rendering on the final live
frame. All scaffold holes stay outside complete compiler contributions. No
whole-program linkage, BSS, asset or packed-file equality is claimed.

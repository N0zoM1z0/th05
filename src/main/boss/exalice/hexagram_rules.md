# EX-Alice hexagram raster leaf and original evolving backdrop state

The separate **204-byte** near-Pascal
`exalice_grcg_hexagram_put(radius,angle)` draws an original full circle
followed by *two* equilateral triangles. The complete `hexagram_rules.hpp`
source names the actual two-triangle count, one-full-turn angular
coordinate system (256 units), one-third-turn vertex spacing and
one-sixth-turn separation of the paired triangles. All vertices remain
the real four-byte `SPPoint`s obtained by the canonical foreign vector
provider, converted to pixel coordinates before calling the actual
`grcg_line()` and `grcg_circle()` APIs. There are no stored triangle
vertices, sprite art, fake line calls, or hand-written target opcodes.

The independently accepted **220-byte**
`exalice_hexagrams_update_and_render()` in the full background TU uses
the same semantic geometry contract. Its one-byte state still moves
through uninitialized, clockwise and counterclockwise values, and
shifts its original line sets without introducing another buffer.
Radius starts at one pixel and grows by **five pixels** per update;
when it reaches **320 pixels** the radius resets and the rotation
changes sign. The source retains the original one-unit angle update,
outer and inner lineset indices 18/9, actual GRCG colors 8 and 9,
and the special white-versus-alternating-color distinction for Boss
phases 9 through 12. The separate EX-Alice backdrop renderer and all
other Boss backdrops keep their real rendering and phase APIs.

Changing `src/main/boss/background.cpp` also touches 16 other already
accepted complete background CODE contributors. All **18 affected
scopes** (the 204-byte hexagram leaf plus 17 background routines)
were independently recompiled twice with the pinned Borland toolchain,
including the entire original 220-byte hexagram animator, the 173-byte
Shinki background router, and the real EX-Alice background callback.
They match every original raw byte, public/OMF/MAP extent and literal
ordered MZ relocation site. The compiled geometric mutation changing
the relative triangle rotation from `256/6` to `256/5` is rejected.
Focused receipt:
`.analysis/unit-replays/gpt-web-exalice-hexagram-backdrop-a/receipt.json`.

This changes semantic source contracts only and does **not** double
credit any previously accepted CODE or initialize additional DATA.
The original 204-byte standalone function still owns its separate
compiler contribution; the background TU's old alternative copy is
not counted again. No whole MAIN cold replay was run.

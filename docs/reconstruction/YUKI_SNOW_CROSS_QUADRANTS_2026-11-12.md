# Yuki's complete late solo attacks: exact four-quadrant snow cross

The four late solo-Yuki attacks share one accepted original-order native
compiler contribution, **670 bytes**. The second attack's snow-cross volley
fires exactly four independent B4 balls and advances their real angle by
one 64/256-circle quarter after **each** spawn. Its fifth angle adjustment
adds the separate `yuki_solo_snow_step` oscillation only **after** all four
shots, so it must not be fused with those four quarter turns.

The maintained natural `yuki_patterns_later.inl` now names the common
`YUKI_SNOW_CROSS_QUARTER()` operation, preserving actual spawning calls,
angle changes, their order, the sound gate and the original timed Boss
reposition branch. The other three fan/vector/speedup callbacks are still
compiled from the same original source order.

Two genuine Borland/TLINK producers recompiled the **complete 670-byte**
source owner, matching all original bytes, native relocation order and
actual compiler boundaries; the existing compiled semantic negative was
rejected. The focused receipt is
`.analysis/unit-replays/gpt-web-yuki-snow-cross-four-quadrants-20261112-a/receipt.json`.
The code was already accepted before this readability refactor; no authored
CODE or instruction byte is double-counted and no cold replay was run.

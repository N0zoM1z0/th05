# MAIN difficulty-label gaiji table

The five difficulty labels at MAIN `[21D44,21D6C)` are now a complete,
40-byte, natural C initialized-DATA owner (`main-hud-rank-labels-data`). The
one-byte glyph selectors spell **EASY, NORMAL, HARD, LUNATIC, EXTRA** in
original rank order, with the source-defined empty glyph `02h`, row
terminator `00h`, and an eight-byte stride. The already accepted
`overlay_data.h` gives each bold alphabet glyph its semantic name; this
initializer does not contain pixel data or copied sprite assets.

Both adjacent bytes at `21D42..21D44` remain unassigned, as does the
following rank-related selector region. This packet has no padding, CODE,
BSS, or original relocation sites. Its standalone outside-only binder
preserves the true MAIN DATA origin and contributes nothing inside the
40-byte scope.

The scoped native replay is
`.analysis/unit-replays/gpt-web-main-rank-labels-a/receipt.json`. Two
independent real C compiles, their original-boundary DATA/MAP checks,
complete byte equality, and ordered fixup checks pass. Changing the
HARD terminal D to E is an actually compiled, rejected negative. The
separately accepted shot-velocity and HUD decimal tables were not rebuilt.

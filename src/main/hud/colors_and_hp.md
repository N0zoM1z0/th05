# MAIN HUD color selectors and HP caption bank

The complete original HUD resource band `[21D9E,21DD6)` is reconstructed as
56 naturally initialized C bytes. It follows the ten small-gaiji strings
at `[21D6C,21D9E)`. The leading zero at `21D9E` is explicitly present as
`byte_22720 db 0` in the original source context, but its purpose is unknown;
that one byte is checked and excluded from authored source credit.

The remaining **55 semantic bytes** represent nine dream-bar colors, ten
power-bar colors, eight blank HP glyph selectors plus NUL, five HP colors,
and two distinct eleven-byte editable CP932 captions of fullwidth spaces
and the multiplication sign. The canonical source references are
`th05/main/hud/dream[data].asm`, `th02/main/hud/power[data].asm`, and
`th04/main/hud/hp[data].asm`, followed by two separate Japanese caption
arrays in the TH05 original source listing. The color components are
named PC-98 TRAM selectors, not a bitmap palette or copied graphical asset.

The source groups the fields under a packed-by-construction, byte-only C
struct with explicit field-offset and total-size assertions. This ensures
the two identical but *distinct mutable* captions are not pooled by the
compiler; a prior diagnostic using `const char` coalesced them and emitted
only 44 bytes. A separate-object attempt emitted 55 bytes, but natural
Borland DATA word alignment shifted its contribution by one; including
the real preceding `db 0` restores the original even DATA extent boundary
without an outside-origin fake pad. Neither failed variant was accepted.

Focused replay: `.analysis/unit-replays/gpt-web-main-hud-colors-c/receipt.json`.
Two independent native C producers match the whole 56-byte interval and
original empty ordered fixups; a compiled mutation of a dream-bar color
is rejected. The 55 semantic bytes count as authored DATA, with one
checked uncredited original zero. No adjacent owner was replayed or
reclassified.

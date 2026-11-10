# Exact player-centered spark-circle Boss-adjacent helper

The complete original far-void MAIN function at `[176B8,176CE)` is now
independently accepted as `main-player-sparks-circle-exact`. The descriptive
maintained name `player_sparks_circle()` is not claimed to be the historical
public spelling; ReC98 `th05_main.asm` preserved this body as `sub_158CC`.

The original two player-position words at DS36D2/36D4 are passed to the
existing near-Pascal `sparks_add_circle` provider at `16EE8`, with an original
radius of **12 pixels = 192 subpixels** and a count of **24 sparks**. The
actual machine-code call uses one 32-bit immediate `00C00018` (high word
radius, low word count); reversing these two semantic arguments produces
`001800C0` instead, even though the whole function stays 22 bytes.
The maintained pure C++ source correctly spells the natural parameter types,
relies on Borland's original calling convention and preserves the simple
BP frame, far return and foreign callee. It does not supply any spark table,
player storage, externally called helper implementation or asm code bytes.

Two fresh independent real Turbo C++/TLINK builds reproduce **22/22 original
raw bytes**, the original empty relocation stream and complete MAP/OMF/public
boundaries. The compiled semantic negative changes the actual count 24→25
and is rejected. The original `main_03`/CS `1527` and DGROUP/DS `209D` remain
source-free externally bound. Receipt:
`.analysis/unit-replays/gpt-web-main-player-sparks-circle-22-20261111/receipt.json`.

This adds 22 complete C++ instruction bytes only; the adjacent 290-byte
Boss-explosion function family and the 204-byte `sparks_add_circle` provider
are not part of this owner and are never double-counted.

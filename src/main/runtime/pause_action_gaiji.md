# MAIN three-action pause menu gaiji selectors

MAIN decoded `[20A62,20A6B)` contains exactly nine meaningful bytes:
three separately terminated two-glyph strings for interruption
(`gsCHUUDAN`), resumption (`gsSAIKAI`), and exit (`gsSHUURYOU`). Their
original selectors occupy font slots F0–F5 in the game's gaiji font,
with one real zero terminator per two-glyph phrase. The source names
these roles in a semantic C enum and constructs a 3×3 unsigned-byte
initializer rather than embedding sprite pixels or copied font bitmap
bytes. The original source is
`_reference/ReC98/th04/gaiji/pause[data].asm`, included by the TH05
MAIN data segment; the independently accepted C++ pause/session code
calls `gaiji_putsa()` with each respective string.

The immediately following `[20A6B,20A6C)` zero is the original even-DATA
alignment after the odd nine-byte record. It is deliberately *not*
absorbed into this source's semantic DATA extent. The preceding two
unreviewed zeros and following pointer context remain unowned. The
isolated symbol-only binder uses the authentic MAIN01/MAIN03/shared code
frames and original DS `209D:0092`. It contributes no glyph or padding
bytes from the target binary.

The scoped native replay
`.analysis/unit-replays/gpt-web-main-pause-gaiji-a/receipt.json`
proves two independent Borland C producers, complete nine-byte OMF/MAP
DATA contribution, raw equality, and the original empty ordered MZ
fixup stream. Changing the second glyph of `gsSAIKAI` to the interruption
glyph is a compiled semantic negative and is rejected. No unrelated
accepted unit or full MAIN cold replay was requested. As with other
semantic string-group owners, the source's array grouping does not on
its own prove original source type or full executable symbol linkage.

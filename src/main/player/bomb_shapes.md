# Mima circles and Yuuka hearts

Three complete independent MAIN callbacks pass raw bytes and original ordered
MZ fixups from maintained natural C++:

| Owner | Complete load extent | Instruction bytes | Ordered fixups |
| --- | --- | ---: | --- |
| Marisa lasers | `[FE2C,FF7B)` | 335 | `[299,285,253,221,136,117,94]` |
| Mima circles | `[10058,1010D)` | 181 | `[152,133]` |
| Yuuka hearts | `[1027B,102F9)` | 126 | `[94,43]` |

None has padding, compiler tables or initialized DATA. Receipts are
`.analysis/unit-replays/main-mima-circles-b/receipt.json` and
`.analysis/unit-replays/main-yuuka-heart-d/receipt.json`, with the Marisa receipt
at `.analysis/unit-replays/main-marisa-bomb-lasers-b/receipt.json`. Each uses two fresh
positive producers and its own compiled mutation: circle distance 256 to 257,
initial heart distance 16 to 17, or Marisa initial radius 24 to 25. All mutations
are rejected.

The full canonical 480-byte bomb union and twelve-byte player motion are reused
without ABI changes. Mima keeps eight ten-byte records, modulo-four spawning,
byte random angles, the original otherwise overwritten player-position copy,
and the minus-999 inactive sentinel. Distance falls by sixteen per update;
position uses the real pixel-space polar API and radius uses signed division.
Yuuka draws sixteen clipped hearts around the real pixel center `(192,160)`,
wraps the byte angle, and advances both angle and distance by two per frame.
Neither polar call applies subpixel scaling to these original pixel coordinates.
The generic two-word polar result uses the actual `SPPoint` interface through
a layout-identical view of the complete display-space point.

The sprite plane mode is the genuine `PLANE_PUT | GC_BRGI` value: pinned
ReC98's `ReC98.inc` defines `PLANE_PUT = 0FF00h or GC_RMW`, with `GC_RMW = C0h`
and `GC_BRGI = 0`. Its signed-word push is preserved. The Mima random entry is
bound to the native original `main_01:C700-AE10`, independently of calibration
placement. The symbol-only binders supply no function bodies or owned bytes.

Pinned ReC98 `th05_main.asm` lines 1980–2071 and 2193–2240 corroborate semantics;
complete native original decodes establish the actual bounds and calls. They
are candidate references, not inherited acceptance. Whole-program linkage and
packed executable equality remain open.

Marisa keeps eight full ten-byte beam records, the initial copy and subsequent
player-coordinate reload across the real far Spark callback, and the original
modulo-four spawn schedule. Its three colored rectangles and filled circle use
true master.lib interfaces; AH is only the real GRCG color API input. The final
port write uses the ordinary `outportb` hardware API. All 335 instruction bytes
and all seven original relocation sites pass without normalization.

Current canonical bodies and source-sensitive refresh evidence are documented
in [bomb_family.md](bomb_family.md). Earlier individual controls remain
historical; the eight-owner refresh uses one shared Reimu-star control.

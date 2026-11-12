# TH05 OP first-launch sound setup: original tiled windows and cursor clock

The whole **1,439-byte twelve-function** OP setup controller uses natural
C++ to build three BGM selections, three effect-sound selections and
animated MSWIN.BFT border windows. Its new
`window_choreography.hpp` defines only compile-time screen/layout
semantics; the original `SetupWindow` remains a real four-byte object,
and the genuinely unused `SetupPalette8` remains the original 48-byte
palette object. No extra screen image or compiler state was introduced.

The original BFT windows use **16-pixel tiles** with an **8-pixel**
vertical border and descend by *half a tile* (**8 pixels**) every
frame. The dropdown renders the upper border, interior tiles and the
following bottom border before moving the bottom to its next position;
rollup reverses the movement in the same actual frame order. The
singleline helper draws two complete border rows without allocating
another offscreen buffer. The original off-center choice column begins
at pixel **48**, with its first row at Y **136**; the caption top is
Y **88**. The six option-rendering arms retain the original
0/1/2 row offsets and their source-level Shift-JIS text lengths.

The setup first blacks the palette, loads the real `mswin.bft` and
`ms.pi` resources, draws on the original offscreen page **1**, copies
into page **0**, and fades in by step one. The BGM choice determines
which sound device the actual 128-byte Resident stores. After the
first animated rollup the original source still waits one *extra*
frame before the SE choice (an original timing quirk), then fades out,
frees the BFT sprites and returns. The menu's eight scanline redraw,
input-change check and wraparound branch behaviors are unaltered.

The modified `setup.cpp` source produces the entire original CODE
context and its independently accepted **1,075-byte CP932
initialized-DATA** contribution. Both units were selectively rebuilt
by two independent pinned Turbo C++/TLINK producers. Original raw
bytes, ordered segment fixups, OMF/MAP boundaries and all compiler
switch/data metadata are preserved. The meaningful compiled negative
slows the natural dropdown from half-tile steps to quarter-tile steps
(`MSWIN_H/2` to `MSWIN_H/4`) and is rejected. Focused final receipt:
`.analysis/unit-replays/gpt-web-op-setup-window-choreography-b/receipt.json`.

An earlier script stopped *before editing* at a replacement-order
conflict, so its saved baseline-only producer is not represented as
new source evidence. The source-current receipt above contains the
actual complete edits and compiled negative. Already accepted code
and strings are not double-credited. No full OP or game cold replay
was executed.

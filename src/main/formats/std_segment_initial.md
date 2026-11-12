# Original TH05 STD segment handle: exact initialized DATA

The real MAIN DGROUP word at DS `209D:0F52` (load-module `[21922,21924)`)
is `std_seg`, a mutable 16-bit segment-only pointer initially equal to zero.
This is independently named and initialized by pinned ReC98
`th04/formats/std[data].asm` (`_std_seg dw 0`), not just inferred from a
repeated pair of zero bytes.

The actual accepted TH05 native consumers identify its address and type:
`std_load()` stores the segment returned by `hmem_allocbyte()`, `std_free()`
checks/releases and resets it, tile fill and scrolling load that segment into
ES/FS, and the enemy VM uses it to read its stage script. None consumes a
four-byte far pointer or a DOS file handle instead.

The single complete C++ scalar initializer in `std_segment_initial.cpp`
produces exactly two `_DATA` bytes through the real Borland compiler at the
original DS offset. Focused evidence:
`.analysis/unit-replays/gpt-web-main-std-segment-init-20261112-a/receipt.json`.
Two independent compiler/TLINK producers matched the complete word, original
empty ordered MZ relocation stream and MAP/OMF scope. The compiled negative
changes the initial segment from zero to one and is rejected. This adds
**two exact source-authored C++ DATA bytes**; the surrounding independently
accepted stage filename and bullet callback tables remain separate.

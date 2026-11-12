# MAINE All Cast background pointer and quarter index

The complete original MAINE DATA interval `[10870,10930)` now has a
**192-byte** natural C++ initializer owner. The first 128 bytes are the
real four-by-eight `BG_FN` far-pointer table; each of the four character
programs selects seven consecutive `EXEDnn.pi` resources and terminates
with a fully null eighth slot. The next 64 bytes are the original signed
16-bit `BG_QUARTER[4][8]` controls, which select the quarter-screen layout
for each background. Both arrays have their original mutable pointer and
word representations. The separately accepted all-cast controller in
`allcast.cpp` uses the exact `BG_FN` and `BG_QUARTER` symbol names.

All 28 non-null pointers are source-level references to entries in the
separately accepted, **280-byte** `allcast_background_filenames[4][7][10]`
bank. No numeric pointer offsets or segment words are embedded in source;
the native binder provides only the foreign array's true linker public at
DATA `1011:08EE`. In this isolated replay, the source-derived pointers
resolve against the original MAINE frame and genuine post-contribution
outside-DATA context. The four end-of-row null slots and all 32 quarter
values are genuine semantics, not compiler filler or artificially inserted
relocations. The preceding masked-image DATA and the next accepted All
Cast text pointer bank stay outside the complete scope.

The original eight-slot row order and quarter values are directly recorded
in `th05_maine.asm` under `_BG_FN` and `_BG_QUARTER`. Their source grouping
matches the 4×8 indexing in `allcast.cpp`, preserving each stage's displayed
image and current quarter. The full native replay at
`.analysis/unit-replays/gpt-web-maine-allcast-bg-index-a/receipt.json`
passed two independent Borland C++ producers, complete 192-byte OMF/MAP
DATA ownership, all original raw bytes and every original ordered segment
fixup. The compiled mutation of the first program's quarter selector from
three to two is rejected. The accepted filename producer remains unchanged
and requires no cold replay.

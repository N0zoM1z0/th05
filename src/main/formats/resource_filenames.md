# Writable MAIN format filename bank

MAIN `[22290,222AB)` now has a complete 27-byte natural C initializer
representing three original resource filenames: mutable `txt1.bb` for the
BB text loader, mutable `st00.map` for the MAP loader, and `MIKO.CFG` for
the configuration resource. The BB loader changes the numeric character
at index 3 to load its next text bank, while the MAP loader changes its
fourth filename character to reflect the current stage. The original
assembly references are `th05/formats/bb_txt_load[data].asm` and
`th05_main.asm`'s DATA/resource section; the maintained MAP loader notes
the DS binding of `st00.map` independently.

The single byte between `st00.map` and `MIKO.CFG` is the original
`evendata` zero at `[222A1,222A2)` and is checked without authored credit.
The preceding two unknown bytes `[2228E,22290)` and following unreviewed
byte `[222AB,222AC)` are not claimed. This is a source-level C grouping of
three separate mutable strings, not a claim that the original game used
the struct type. The byte-only struct has checked field offsets 0, 8, 17,
and 18, with a 27-byte complete contribution and no CODE/BSS/fixups.

The targeted native replay at
`.analysis/unit-replays/gpt-web-main-format-filenames-a/receipt.json`
passes two independent original-size Borland C producers and the complete
raw-byte/MAP/OMF/ordered-fixup checks. Its compiled `st00.map`→`st01.map`
negative is rejected. No original bytes, load-module filename array or
binary assembler instruction is copied into the C initializer.

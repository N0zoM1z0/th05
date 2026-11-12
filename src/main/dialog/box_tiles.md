# MAIN dialog-box coverage tile masks

The full original MAIN interval `[228A0,228B8)` holds the **24-byte**
three-stage dialog-box fade/wipe tile pattern. The source-level C
initializer computes all twelve 16-bit monochrome row patterns from
three coverage ratios (one, two and three active pixel positions out of
four) and four cyclic horizontal phases. A four-bit occupancy pattern is
repeated across the full sixteen-pixel word; the native byte representation
is little-endian. No font bitmap or sprite image is copied into the source.

The independently accepted `dialog_box_put()` at original MAIN
`[13A3E,13A96)` accesses this exact `BOX_TILES` symbol at DS `1ED0`.
It indexes one of three eight-byte tile records, cycles each record's
four word masks vertically for 48 rows, and writes each word twenty
times to VRAM via the hardware REP STOSW loop. The new semantic-data owner
therefore provides a real named input to existing reconstructed CODE;
the renderer's ABI and maintained source remain unchanged.

`box_tiles.c` intentionally exposes a `const unsigned char[24]`, matching
the renderer's near byte-bank declaration, while its arithmetic generates
the actual word values rather than transcribing target payloads. The
binder defines only foreign CODE frames and DATA prefix, with no inside
hole, instruction, initializer or relocation. This is a single complete
compiler DATA contribution with no padding.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-dialog-tile-masks-a/receipt.json`.
Two independent real Borland C producers match all 24 original bytes,
complete OMF/MAP DATA boundaries and empty original relocation order.
A real compiled change of the first row's coverage from one to two
is rejected. No unrelated accepted unit was replayed.

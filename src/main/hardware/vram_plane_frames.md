# MAIN PC-98 video-plane far pointer bank

The original MAIN decoded `[21208,21218)` now has a complete natural C
initialized-DATA owner of four independent near-storage far pointers.
The original game uses physical planar video segments A800, B000, B800
and E000, each with offset zero; source explicitly identifies the blue,
red, green and extended planes. They are hardware addresses, not a
copied image, sprite or other asset. The independently accepted OP and
MAINE counterparts reuse the same semantic segment definitions but
remain separate physical DATA contributions in their respective binaries.

The outside-only MAIN binder preserves MAIN01/MAIN03 and shared CODE
frames, with the real DGROUP prefix at DS 209D:0838. No pointer values
or candidate bytes are provided outside the C source. The next two
unreviewed zeros `[21218,2121A)` and the subsequent embedded sprite
asset are deliberately excluded. The source initializes four real
large-model 4-byte far pointers and asserts their physical sizes.

The targeted receipt
`.analysis/unit-replays/gpt-web-main-vram-plane-frames-a/receipt.json`
records two independent Borland C producers, full 16-byte raw equality,
original OMF/MAP initialized-DATA boundaries, and the original empty
ordered fixup stream. A compiled mutation of the red plane's physical
segment from B000 to B010 was rejected. No all-MAIN or unrelated-unit
replay was needed.

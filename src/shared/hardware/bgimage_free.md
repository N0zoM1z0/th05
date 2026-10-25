# Background-plane release candidate

This uncompiled natural source preserves the full eight-byte segmented-pointer
object and the maintained TH04 release algorithm: if B is owned, free B, R, G
and E, then clear B. It copies none of the surrounding snapshot/blit assembly
or image data. Actual decoded OP has one complete 50-byte function at
`D726..D758`, with twelve instructions and no NOPs or compiler tables.

Native review found a strict blocker before any new compilation: original OP
fixups are `[14, 23, 32, 41]`, while the unchanged cached genuine calibration
producer emits `[41, 32, 23, 14]`. Its complete raw body is equal, but original
relocation ordering is not. Neither the raw match nor natural source permits
acceptance. No sorting, normalization, reordering or new compiler probe is
proposed without new authentic producer evidence.

The source and symbol-only OP binder are retained as semantic candidates only;
no unit is registered and no authored credit is claimed. The independent
accepted startup, menu and music owners are unchanged. Private
`.analysis/op-remaining-native-review.json` pins the original decoded view,
calibration hash, exact ordered streams and acceptance-overlap check.

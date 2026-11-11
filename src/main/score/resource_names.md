# MAIN score filename and continue-page glyph names, 20 initialized bytes

Original MAIN `[2192E,21942)` consists of the exact eleven-byte
`GENSOU.SCR\0` score filename, immediately followed by the eight CP932
halfwidth screen glyph bytes for the original `_gCONTINUE` label and one
zero terminator. Both labels are independently present in the retained
original game assembly. The glyph bytes are maintained as a genuine CP932
text literal, not a copied hex byte array or a translated game string.

The natural C model `MainScoreResourceNames` retains two distinct arrays:
`const char[11]` and `const unsigned char[9]`. Compile-time struct size and
offset assertions pin the original 20-byte contiguous storage. The binder
reserves only the original MAIN symbolic CODE/DGROUP frame up to DGROUP:F5E;
no foreign code, stage resources, padding, or initialized byte copies are
supplied. The preceding ST00.STD string and its separator zero remain
separate unknown bytes.

Two independent pinned Borland C/TLINK producers exactly matched all 20
original initialized bytes and the empty ordered MZ relocation list. The
compiled `GENSOU.SCR` to `GENSOU.SCX` negative was rejected. Focused evidence:
`.analysis/unit-replays/gpt-web-main-score-file-continue-20261111/receipt.json`.
The aggregate is a semantic source model of original distinct game resources,
not an assertion about the historical struct declaration.

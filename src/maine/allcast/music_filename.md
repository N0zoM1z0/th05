# MAINE All Cast music-program filename

The decoded MAINE interval `[115F9,115FE)` is the original five-byte,
NUL-terminated `EXED` BGM basename for the ending's All Cast animation.
The original MAIN-to-MAINE assembly list declares public `_EXED` at this
point, and the independently accepted complete three-function
`allcast.cpp` calls the actual `snd_load(EXED, SND_LOAD_SONG)` before
starting the credit-screen timing sequence. The source's `char near
EXED[5] = "EXED"` exports a real mutable C public, not an opaque
copied binary resource. It is a name, not the song data itself.

The C translation unit produces the entire five-byte initialized DATA
contribution at the genuine MAINE DGROUP `10110:14E9`. Its symbol-only
binder preserves the original group_01/SHARED code frames and the
outside DATA prefix; there are no initialized bytes, instructions or
linker fixups inserted inside this contribution. The preceding 2,787
bytes of All Cast credit text and following independently accepted
alphabet bank remain distinct source owners.

The native focused receipt
`.analysis/unit-replays/gpt-web-maine-allcast-music-name-a/receipt.json`
proves two independent Borland C producers, complete five-byte raw,
OMF/LEDATA and MAP equality, the empty original ordered MZ fixups and
rejection of the compiled `EXED`→`EXEE` mutation. No other unit or
whole MAINE cold replay was requested.

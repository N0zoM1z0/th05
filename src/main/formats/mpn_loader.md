# `mpn_load_inner()`: .MPN tile image loader (ASM)

`mpn_loader.asm` is the 92-byte far Pascal function at MAIN `[41B2,420E)`.
It calls `mpn_free()`, opens the file with DOS, reads the 6-byte header and
the 48-byte palette into `Palettes`, takes the last image index from the
header word at offset 4, allocates `(index + 1) * 128` bytes, reads all
images into that segment, closes the file and calls `palette_show()`.

ZUN landmine: no file or allocation errors are handled.

The function preserves SI, DI and DS and returns with `RETF 4`. The first
call to `mpn_free()` is `PUSH CS` and a near call because both are in `_TEXT`;
the NOPs at offsets 56 and 82 come from the same far-call relaxation and
carry no source credit. The image segment and the last image index are the
words at DS `3068` and `306A`.

The direct DOS calls, the temporary DS switch and the register-held file
handle suggest hand-written assembly; the historical source is not known.
The replay's negative control changes the palette read from 48 to 47 bytes.

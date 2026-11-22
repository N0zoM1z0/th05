# ZUN resident: notes

- **Config init.** A 20-byte local frame, ending with a near return at
  `04A8`. The resident block is 128 bytes: six signed-char options, a 10-byte
  disk configuration and a 2-byte resident segment. ZUN's defects are kept: a
  missing file leaves the checksum local uninitialised, recreating an invalid
  file keeps that file's checksum, read/write results are ignored, and a
  failed resident-segment write returns without closing the file.
- **Entry (`-S`).** Tiny-model near cdecl
  `int main(int argc, const unsigned char **argv)` with a 12-byte frame,
  saving SI/DI. The build uses Turbo C++ 4.02 and CP932 source input.
- **C0T startup.** The pinned tiny-model `C0T.OBJ` relinks exactly in the
  `-S` context. Its two uninitialised CODE bytes (read through `CS:[0363]`
  during startup) are compared and filed as a zero-credit reviewed gap.

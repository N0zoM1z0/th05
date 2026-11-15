# File format loaders (MAIN)

Loaders and release functions for the .STD, .MAP, .MPN, .BB and .CFG files,
plus their writable filename buffers. ReC98 (`th04/formats/`, `th05/formats/`,
`th05_main.asm`) documents the same functions; the TH04 versions use
master.lib file functions, while TH05 calls DOS directly and never checks a
DOS or allocation result.

The `.asm` sources in this directory (BB loader, BB text blitter, CDG loader
family and bank release, MPN loader and renderer) are documented in their own
notes, which the ASM family configuration links to.

## Code generation findings

- **Frameless release functions.** `std_free()`, `map_free()` and
  `bb_playchar_free()` need `-k-`. Without it, `map_free()` grows from 23 to
  27 bytes through a `PUSH BP; MOV BP,SP` / `POP BP` frame. Each function in
  the original is followed by one NOP padding byte.
- **`map_load()` must use the live AX.** Assigning DS from `map_seg` after
  `hmem_allocbyte()` reloads the variable from memory and adds two bytes; the
  original moves the allocator's AX result straight into DS.
- **`bb_playchar_load()`** needs the explicit `static_cast<char>` to produce a
  single byte-sized `ADD` to memory. The mixed signed/unsigned expression
  without it is three bytes longer.
- **`mpn_free()`** calls `hmem_free()` in the same `_TEXT` segment, so TLINK
  relaxes the far call and leaves a NOP at offset 11.
- **`std_load()`** goes through `tcc -S` and TASM32, because Turbo C++'s
  built-in assembler cannot parse all of the 386 `MOVZX` forms. Writing the
  script loop as `while(_DL != 0)` adds an `OR DL,DL` (186 instead of 184
  bytes), so the loop ends in inline `DEC DL; JNE`. The `std_run()` callback
  is stored through `SEG MAIN_03` / `OFFSET MAIN_03:@std_run$qv`, which gives
  the original far-pointer relocation; earlier attempts ran into a
  cross-group 16-bit fixup overflow.
- **`mpn_load()`** (`mpn_upload.cpp`): nested `for` loops compile to 94 bytes
  with a stack frame and redundant entry checks; `do`/`while` loops on the
  pseudo-registers give the original 69. A directly compiled object matches
  every byte but writes the fixups in the order `[61,32,12]`; only the
  `tcc -S` + TASM32 pipeline reproduces the original `[12,32,61]`.
- **`cfg_load_resident_ptr()`** is followed by a NOP padding byte, emitted with
  `#pragma codestring "\x90"`.
- **Filename data** (`resource_filenames.c`, `bb_cheeto_filename.c`,
  `bb_playchar.cpp`) is compiled as plain initialized data. The zero byte
  between `st00.map` and `MIKO.CFG` is the even-alignment padding of the
  original data segment.

## `bb_load()` in C++

`bb_load.asm` is the credited implementation of `bb_load()`. `bb_load.cpp`
is an alternative C++ version that also reproduces all 55 bytes, but it is not
part of any replayed unit. The difficulty is that the original pushes SI on
entry, keeps the caller's DS in SI, and pops SI *before* loading the return
value into AX. Turbo C++ saves and restores SI itself as soon as any C or
inline-assembly code touches SI, and its epilogue always loads AX first.

`__emit__()` hides the four SI instructions from the compiler, which then
neither adds its own save/restore nor reorders the epilogue (see the
`__emit__` notes in `_reference/ReC98/codegen.hpp`). Approaches that failed:

- a `register` local for the saved DS, also inside a nested block: 51/55
  bytes, with `MOV AX,[bb_load_seg]` before `POP SI`;
- inline `push si; mov si, ds` ... `mov ds, si; pop si`, with or without
  `#pragma aux ... modify [si]`: 57 bytes, duplicate SI save/restore;
- saving DS through ES (57 bytes) or a BP stack anchor (58 bytes, fixup moves
  from +7 to +8);
- keeping DS only on the stack: 51 bytes, allocator fixup at +6;
- a hand-written `POP SI; MOV AX,...; RET 4` epilogue: the inline assembler
  cannot name the C++ variable, and using its address makes the compiler save
  DI as well (61 bytes).

One early 49-byte `push ds` variant was invalid: after `LDS DX` loads the
filename segment, it read `bb_load_seg` before restoring DS.

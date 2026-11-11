# TH05 OP joystick sound-board detection: complete 42-byte ASM

The real OP `JS_START` occupies decoded `[2BAC,2BD6)`. This game-specific
sound-board joystick startup scans the PSG status port `0188h` up to 256 times,
leaves AX zero on failure, and otherwise reads register 7, preserves its low
six bits, enables joystick input in its upper bits, and writes the mixer back.
It records the board-presence result in the original word `js_bexist` at
DGROUP:0544, then returns far. The original code has one word-alignment NOP
immediately after the RETF; the last byte belongs to the complete 42-byte
assembler scope but carries zero authored credit.

`src/op/joystick/js_start.asm` is a maintained, semantic handwritten-ASM
reconstruction of the **TH05-specific port** of the Master joystick handler.
The original Master 0.23 joystick driver includes a separate SAJ-98 detection
path that this game-specific version does not contain. The recovered function
is therefore not falsely classified as an unchanged upstream Master PROC.
The external `SOUND_I`/`SOUND_O` near routines are resolved by symbol-only
original CODE addresses (20EA and 20D4), without copying their instructions.
The original DATA/BSS segment extents are reserved without LEDATA, preserving
the native OP DGROUP base `0EFE0h` and producing a structurally valid MZ.

A strict original native review fixes all decoded instruction boundaries,
complete target bytes, absence of MZ relocation sites and the sole alignment
NOP. The scoped two-producer TASM 5.0/TLINK replay must match all 42 bytes
while rejecting a compiled change of the sound-board poll count from 256 to
255. This is **41 instruction bytes plus 1 checked alignment NOP**, not C++
compiler output or a claim about the exact original author's source file.

## Accepted focused native replay

Both independent pinned TASM/TLINK producers emitted **42/42 exact bytes**
and the same empty ordered original MZ relocation list. The complete source
was found at the real `_TEXT` entry `2BAC` with the source-only linker frame
matching DGROUP `0EFE0`. A separate real assembly changed the 256-iteration
board poll count to 255 and was rejected by the original-byte comparison.
The local evidence is at
`.analysis/asm-replays/gpt-web-op-joystick-start-a/receipt.json`;
no other OP function, BSS initializer, or sound-board helper is accepted by
this focused owner.

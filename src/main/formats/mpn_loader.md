# MPN image bank loader: complete 92-byte game-specific ASM candidate

MAIN `[41B2,420E)` is one complete far-Pascal `MPN_LOAD_INNER` routine in
original `_TEXT`, CS `0000`, DS `209D`. It contains no local tables or owned
initialized DATA/BSS. Its two original linker call-relaxation NOP bytes, at
relative offsets 56 and 82, are checked in the exact comparison but receive
no source-instruction credit. The separate `MPN_FREE` function starts at
`420E` and remains independently owned; the loader's symbolic end label
represents only that real neighboring far callee, not its body.

The recovered source is a semantic DOS file reader, not a target-instruction
byte array. It releases the previous MPN bank, opens a far filename with
DOS `3D00h`, reads a six-byte header and 48-byte palette into the actual
`Palettes` data object, captures the header's inclusive image index, then
allocates `(last_index + 1) * 128` bytes through `HMEM_ALLOCBYTE`. The 128-byte
image consists of four 16×16 planes, two bytes per row. The loader reads all
image bytes into the returned segment, closes the DOS handle and calls the
real `PALETTE_SHOW` provider. Its original behavior has no file I/O or
allocation-failure checks, so the source does not invent them.

The far ABI preserves SI/DI and DS, consumes four stack bytes on `RETF 4`,
and uses the real `SS:BX+4` far filename operand after the adjacent MPN free
call. The first call is a same-CS near call preceded by `PUSH CS`, preserving
the far return frame to `MPN_FREE`. Both external Master helpers remain real
far providers at `_TEXT` 281A and 2158. Two real segment-valued DATA words
live at DS offsets 3068 and 306A. Neither fake data nor foreign function
instructions are emitted by the zero-payload binder. The global `Palettes`
object is located at DS264A; the index is its word at offset four.

## Source-language inference and native verification

This routine's explicit `INT 21h`, temporary DS swap, register-based DOS
handle, far-to-near call relaxation and manually preserved live state support
a game-specific handwritten-ASM inference. The pinned ReC98
`th05_main.asm` is a semantic architecture reference; the literal historical
original source and assembler version are not proven. Master 0.23 upstream
source ownership has not been assigned to this MPN loader. This result is
therefore distinct from both the accepted MPN renderer's 92-byte owner and
the independently accepted C++ `mpn_load()` wrapper.

The native boundary proof is retained in the private
`.analysis/gpt-web-mpn-loader-native-review.json`, and the first real
source/TASM/TLINK comparison in
`.analysis/gpt-web-mpn-loader-native-b/`. The original 92 bytes and empty
ordered MZ fixups match exactly. The maintained source retains semantic
constants, labels and genuine ABI calls; it does not incorporate raw bytes,
NOP padding directives, forged code/data, or compiler-generated C++ credit.

The accepted `main-mpn-loader` ASM family has two independent cold producers
**only for this owner**, saved under
`.analysis/asm-replays/gpt-web-main-mpn-loader-b/receipt.json`, and an assembled
negative changing palette read length 48 → 47 bytes. Both positive producers
match every original byte and the empty ordered fixup stream; the mutation
retains the complete 92-byte boundary/fixups but fails raw comparison. The two observed NOPs are linker-produced call padding, excluded
as zero-credit *runtime-placeholder* bytes under the current ASM ownership
kind vocabulary; the source itself contains no artificial placeholders.

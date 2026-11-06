# Scrolling tile strip copy

The complete native MAIN scope is BC6E..BD24: 182 instruction bytes with no
table, padding or MZ fixup. `tiles_copy_scroll_strip` and the scratch labels
are descriptive maintained names; their historical spellings are unknown.
ReC98 b6ba5b0a th05_main.asm's sub_BC6A and the corresponding th04_main.asm
routine corroborate the algorithm, but are disassembly references rather
than recovered historical source or transferable acceptance.

The entry takes no arguments and reads scroll_line at DS3516 and a byte height
at DS34F6. It copies 24 tile columns into the newly exposed VRAM strip at
scroll_line*80+4. The first fragment starts scroll_line modulo 16 scanlines
into a tile; a possible second fragment uses the next row of the 25x32-WORD
tile ring at DS511A..575A. Crossing the 32000-byte VRAM bottom also wraps the
cache index by its full 1600-byte extent. The three scratch WORDs at DS34F7,
34F9 and 34FB retain the first source skip, destination and first height.
All shared state and tile pixels remain foreign. Zero or excessive heights
retain their original unchecked behavior.

The source-language decision rests on the complete custom hardware loop:
BP is borrowed for EGC latch data without a BP frame, AX retains a cache
cursor, DH/DL pack spill height and column count, and BL consumes the spill
while CX counts scanlines. That interdependent register protocol supports
handwritten ASM independently of compiler attempts and neighboring routines.
The maintained column macro expresses both fragments and the wrap operation;
geometry gives the strides. There are no opcode emissions or pixel payloads.
It preserves BP/SI/DI/DS and IF/DF, leaves ES=A800, and clobbers AX/BX/CX/DX
and arithmetic flags. The manual copy is independent of DF. EGC mode must
already be enabled by the real caller; this procedure owns no setup helper.
Historical source/assembler identity and exhaustive vendor ancestry remain
unknown. Adjacent compiler-generated code is explicitly excluded.

Two fresh independently built producers pass valid ordinary OMF and the
complete owned CODE/LEDATA contribution, native frames/publics, every raw byte
and the original ordered fixups. Normalized OMF, MAP and whole MZ outputs are
deterministic. Only dependency metadata is normalized. The normal compiled
visible-column negative is rejected with unchanged extent and fixup order.
No new DATA/BSS, C/C++ function, foreign provider or whole EXE is accepted.
Unchanged accepted inputs and tool execution proofs are reused after identity
checks; no whole replay, extra negative or CPU model was run.

Receipt: `.analysis/asm-replays/main-tile-scroll-strip-a/receipt.json`, SHA-256
`76876285a24c0d0f0f876928df26a16362b7aec5083a43d4b3adb322946de2d1`.
Native proof: `.analysis/tile-strip-native-review.json`, SHA-256
`973176b76679755127c0e4069390db4e4405d460d0c46bb1f582d6a9fc6b53e4`.

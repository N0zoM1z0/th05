# Dirty half-tile rendering

The complete MAIN procedure is BDAE..BE1A, 108 instruction bytes, no table or
padding, with the original ordered MZ fixup at relative 103. BE1A starts the
independent compiler-generated PlayfieldMotion::update_seg1; those 32 bytes
are excluded. ReC98 b6ba5b0a th04/main/tile/redraw.asm supplies the candidate
algorithm, not transferred acceptance or proof of historical source identity.

The kernel scans 50 rows of 16x8 half-tile flags from bottom to top, testing
24 visible columns of each 32-byte row. A nonzero flag is cleared before
copying eight VRAM scanlines through the EGC latch. DH parity selects the top
or bottom half of the same 16x16 tile; the cache cursor changes rows only after
both halves. Each cache element is a WORD VRAM offset, not a pixel payload.
The 50x32-byte flag array at DS4ADA..511A and 25x32-WORD tile ring at
DS511A..575A remain foreign and receive no DATA/BSS credit.

The CX scanline / DH half-row / DL column protocol, parity-dependent cache
cursor, and paired ES:A800 hardware latch reads/writes support independent
handwritten-ASM inference for the complete kernel. No failed C++ trial is used
as evidence. The maintained macro expresses the dirty-half copy and geometry;
there are no emitted opcode bytes, artificial gaps or copied image assets.
SI/DI/BP/DS and IF/DF are preserved. ES remains A800; AX/BX/CX/DX and arithmetic
flags are scratch. Manual word copies do not depend on DF. The actual near
no-argument Pascal interface is retained.

The near EGC setup at BC2E and Master far EGC_OFF at 0000:085E remain foreign.
Their source language is not inferred from the caller. Master 0.23 EGC.ASM
corroborates the shutdown protocol; historical assembler identity and exhaustive
vendor ancestry remain unknown. Bindings supply native frames and foreign
labels only, including the full flag/cache extent and the real provider
distances. No stack or initialized provider payload is supplied.

Two fresh independently built producers pass valid ordinary OMF and the
complete owned CODE/LEDATA contribution, native frames/publics, every raw byte
and the original ordered fixups. Normalized OMF, MAP and whole MZ outputs are
deterministic. Only dependency metadata is normalized. The normal compiled
visible-column negative is rejected with unchanged extent and fixup order.
No new DATA/BSS, C/C++ function, foreign provider or whole EXE is accepted.
Unchanged accepted inputs and tool execution proofs are reused after identity
checks; no whole replay, extra negative or CPU model was run.

Receipt: `.analysis/asm-replays/main-tile-redraw-b/receipt.json`, SHA-256
`af8dcb3429751b3ea6d1398116679f7b4b5799eb2180c08bcbc55a81ba4d525b`.
Native proof: `.analysis/tile-redraw-native-review.json`, SHA-256
`b0a3aa000d47d16759870a52725337c9950ec0a20d50389cd35f99756731a6a9`.

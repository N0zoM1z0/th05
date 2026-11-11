# OP/MAINE original Master-derived no-Y-clip blitter: 392 CODE bytes

The two original `GRAPH_PACK_PUT_8_NOCLIP` complete procedures are now
source-linked exactly, at OP `35B0..3674` (196 bytes) and MAINE `3778..383C`
(196 bytes). This routine renders horizontal runs of packed 8-pixel patterns
onto four PC-98 VRAM planes without the original vertical clipping. A complete
semantic derivation—not just similarity of the disassembly—is established
against the pinned original Master 0.23 author source `GRPPPUT8.ASM`.

The original complete `GRAPH_PACK_PUT_8` ASM block has 109 normalized
instruction/source lines. Remove **exactly three contiguous original Y-clip
guards** (`SUB AX,ClipYT`, `CMP AX,ClipYH`, `JA short CLIPOUT`), rename the
procedure from `GRAPH_PACK_PUT_8` to `GRAPH_PACK_PUT_8_NOCLIP` and the
`CLIPOUT` branch target to `GRPPP8NC_CLIPOUT`, and the remaining **106 lines
match exactly** the complete native TASM source body. Register use, all
other instructions, macro options, Y coordinate arithmetic, 4-plane drawing
and the `RET 10` convention remain unchanged. The original author archive
is separate from the native ReC98 `GAME=5` build and retains its own hash.

Both real native TASM OMFs (`op.obj`, `mainem.obj`) provide full ordinary
CODE LEDATA for the exact 196-byte functions. Their nine ordered offset16
FIXUPP actions each resolve into the genuine original `_TEXT` and DGROUP
layout. Full original decoded and retained-calibration raw bytes match;
the original ordered MZ relocation streams are empty for both. Each complete
scope is uniquely located in its respective original payload. No emitted
machine bytes, copied target fragment, patched linker output or DATA/BSS
content are supplied by the review.

This is **Master/ZUN-derived third-party CODE**, not accepted new game-authored
C++ or original unmodified Master. Both extents receive vendor-source credit
with zero authored credit. The surrounding original Master display and archive
functions retain their separate evidence and the two-byte PFEND runtime slots
remain unknown.

Proof: [`context_graph_pack_noclip.json`](../../config/context_graph_pack_noclip.json).
Separate explicit decision:
[`reviewed_context_graph_pack_noclip.json`](../../config/reviewed_context_graph_pack_noclip.json).
Native verification: `python3 scripts/review_context_graph_pack_noclip.py --check`;
public CI runs `--structural-check` only. No full cold replay was run.

# Exact OP Music Room saved B-plane restoration

The complete near `nopoly_B_put()` at decoded OP `[BFF6,C014)` restores
32,000 bytes of the saved B plane to PC-98 VRAM segment `A800`. The original
near return and DI/SI/DS/BP preservation are retained. Its C++ source uses
the true two-byte saved segment handle at DS `4EB8`, selects it through DS,
sets ES to `A800`, and moves 16,000 words in one `REP MOVSW`. No raster
image or segment-memory contents are supplied by the source.

The natural TH05 Music Room donor, pinned ReC98 `th02/op/m_music.cpp`, uses
Borland's `__memcpy__` intrinsic; its first compiler diagnostic gave the
correct 30-byte size but selected `33 FF` and `33 F6` for zeroing DI and SI
instead of the original `31 FF` and `31 F6`. Keeping the explicit semantic
`XOR DI,DI` and `XOR SI,SI` in the C++ register interface produces the
correct native form with **direct TCC `-c`**, whereas TCC `-S` / TASM32
still chooses the other encoding. The original algorithm and all 30 bytes
are preserved without emitting raw opcode bytes or changing the linker output.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-nopoly-plane-put-exact-a/receipt.json`.
Two independent direct Borland C++/TLINK producers reproduce the complete
30 bytes, the original empty relocation list, and native OP `op_01` CODE/
DGROUP placement. Decreasing the copied plane size by one word is compiled
and rejected. This closes the former hole between the separately accepted
Music Room prefix and suffix contributions without changing their sources.

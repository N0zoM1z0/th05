# Exact MAIN tile-ring setter

`tile_ring_set_vo(int x,int y,unsigned int image_vo)` owns the complete
79-byte far-Pascal function at MAIN `[BEA4,BEF3)`. It has a Borland BP frame,
`RETF 6`, no native alignment or tables inside the function, and no MZ
relocations. The separately owned point-popup renderer immediately before it
and the subsequent backdrop renderer are not part of this function.

The maintained source follows `ReC98/th04/main/tile/set.cpp`, which identifies
the TH05 code as an identical implementation. It converts the 16-bit signed
subpixel X coordinate to pixels, saves `scroll_active` from DS `351A` in a
one-byte local, forces scroll conversion, then calls the real near-Pascal
`scroll_subpixel_y_to_vram_seg1` at MAIN `DF28`. The signed `/16` row and
column indices update the complete 25×32 word-valued tile-ring at DS `511A`.
It restores the previous scroll flag and does not add coordinate guards or
state changes. Both real signed divisions and the temporary scroll override
are preserved; a precomputed offset or unsigned cast would change behavior.

The source has one natural C++ function and a symbol-only binding scaffold;
no initialized tile data, fake wrapper logic or byte template is emitted.
Focused receipt:
`.analysis/unit-replays/gpt-web-main-tile-ring-set-a/receipt.json`.
Two fresh Turbo C++/TASM/TLINK producers match 79/79 original bytes and the
empty ordered fixup stream. The negative that replaces the temporary
scroll-active value `1` with `0` compiles and is rejected. The original
CS `AE1`, DGROUP `209D`, and near helper/public MAP placements are retained.

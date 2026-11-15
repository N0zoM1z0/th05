# Bullet and gather tile invalidation (assembly)

`gather_invalidate.asm` is `bullets_and_gather_invalidate()`, MAIN
`E40E..E4B6` (168 bytes). It marks the tiles under all bullets and gather
circles for redrawing. Callers use near cdecl `void()`; the routine preserves
SI/DI and changes the shared dirty-tile rectangle at DS `3502`. It is the
TH05 branch of ReC98's `th04/main/bullets_gather_inv.asm`.

1. Unless a zap or bullet clear is active, it invalidates all 180 pellets
   (8x8) from `bullets` at DS `5F2A`.
2. It then invalidates the 16x16 bullets whose spawn state is above
   `BSF_GRAZED`. If the pellet loop was skipped, the count becomes 400, so
   this loop covers pellets as well.
3. Finally it walks all sixteen 38-byte `gather_t` records at DS `9BFA`,
   using the radius at offset 14 as both width and height around the previous
   center at offset 6.

Each rectangle goes to the near Pascal tile invalidator at MAIN `BAD2`.

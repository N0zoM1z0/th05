# Exact OP single-plane CDG renderer

The OP near/fastcall-independent far-Pascal
`cdg_put_nocolors_8(left, top, slot)` has a complete 74-byte C++ source
match at decoded `[E114,E15E)`. It selects a real 16-byte CDG slot at
DGROUP `3A96`, combines the signed horizontal position with the sprite's
bottom-left VRAM offset, computes its DWORD width and 80-byte row stride,
and selects the correct `A800` VRAM segment from the vertical coordinate.
The original source segment comes from the slot's alpha-plane handle.
It copies one row at a time using 386 `REP MOVSD`, stepping backwards until
the original signed DI condition terminates. The function preserves DS,
SI, DI and BP and ends with `RETF 6`.

The maintained source follows pinned ReC98
`th05/formats/cdg_p_nc.cpp`/`th04/formats/cdg_impl.hpp` with real Borland
register bindings. One conventional C++ signed shift compiled to an
unnecessary AX temporary and emitted 78 bytes. Expressing the original
`SAR DI,3` register operation directly preserves the native result and gives
exactly 74 bytes. Source contains no CDG sprite assets, opcode templates,
module data or foreign helper bodies. The independent preceding byte at
`E113` is not part of this function and is not credited.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-cdg-nocolors-exact-a/receipt.json`.
Two independent TCC `-S`/TASM32/TLINK producers match all 74 original
bytes, complete native MAP/OMF ownership and the empty original relocation
stream. The compiled source negative changes the signed horizontal shift
from three to two, and the strict oracle rejects it. There was no full
cold replay or transfer of credit from accepted CDG graphics providers.

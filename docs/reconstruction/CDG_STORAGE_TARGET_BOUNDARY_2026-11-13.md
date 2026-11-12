# CDG slot BSS: source identity does not imply target-byte ownership

The retained original-game `th03/formats/cdg[bss].asm` declares 64 CDG slots
(`cdg_t CDG_SLOT_COUNT dup(<?>)`, with `GAME >= 4`). The type is 16 bytes,
so the real TASM `_BSS` object has a 1,024-byte uninitialized array with
correct `_cdg_slots` PUBDEF locations in MAIN, OP and MAINE. This alone is
not enough to adopt an MZ file-backed interval.

A focused original-target comparison exposed three distinct blockers:

- MAIN's `_cdg_slots` linker coordinate is beyond the end of the decoded
  original file-backed program image. There are no 1,024 original bytes at
  that coordinate to accept as DATA or source-backed observed storage.
- OP's corresponding original file-backed region contains many nonzero
  values, even though the linked `_BSS` source has no initialized LEDATA.
- MAINE contains fewer than 1,024 file-backed bytes from the corresponding
  coordinate to the image end, and those observed bytes are also nonzero.

The earlier `reviewed-uninitialized-game-storage` method is deliberately
not extended to these CDG arrays. Any future attribution needs an actual
original layout explanation for the difference between TASM's `_BSS` model
and the decoded original file payload, not a zero-padded surrogate or an
invented compiler DATA initializer. No source files or accepted units were
changed during this diagnostic.

# MAINE cutscene interpreter

`cutscene.cpp` follows ReC98's `th03/cutscene/cutscene.cpp` with
`GAME == 5`. Most of ReC98's ZUN bug/quirk/landmine comments for the TH05
branches have been carried over into the source.

## Segment layout and relocation order

All eleven functions sit in one `CUTSCENE_TEXT` segment in the original.
`cutscene_joined.cpp` builds that layout, and only that layout reproduces
`script_op()`'s 42 relocations in their original order: Borland writes code in
1024-byte LEDATA records, and the relocation order follows those record
boundaries. With `script_op()` in a different place or segment, its bytes
still match but its fixups come out in a different order. Sorting or patching
the fixups is not an acceptable fix.

The direct build of `cutscene.cpp` (no `TH05_CUTSCENE_JOINED`) predates the
joined one: it puts everything after `egc_start_copy()` into
`CUTSCENE_AFTER_TEXT`, and the nine functions other than `egc_start_copy()`
and `script_op()` are checked in that configuration.

## egc_start_copy()

The original loads the EGC address register value with `MOV AX, 0`. Writing
`_AX = 0` gives `XOR AX, AX`, one byte shorter, so the joined build and
`egc_setup_exact.cpp` use a one-instruction `asm` statement for it. The split
build keeps the XOR version and its linker scaffold reserves the missing byte.

## Data defined elsewhere

- `colmap_count` is defined in `box_mask_patterns.c`, in front of
  `BOX_MASKS`.
- `CUTSCENE_KANJI` (`kanji_buffer.c`) is a 3-byte `"  "` buffer. `cutscene.hpp`
  declares it as an array of `ShiftJISKanji` so that `cutscene_animate()` can
  write each character into it.
- The 60-byte `unused` array and the `padding` byte are unreferenced BSS that
  ReC98 also declares; their real type is unknown.

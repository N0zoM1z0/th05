; The true 50-by-32 byte dirty flags; no image data is emitted.
DIRTY_MAP_COLUMNS equ 50
DIRTY_MAP_ROWS    equ 32
DIRTY_MAP_BYTES   equ (DIRTY_MAP_COLUMNS * DIRTY_MAP_ROWS)
DIRTY_MAP_DWORDS  equ (DIRTY_MAP_BYTES / 4)

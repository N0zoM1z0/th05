; Native PC-98 GRCG and pellet silhouette geometry only, no raster payload.
GRCG_TILE_PORT equ 07Eh
GRCG_MODE_PORT equ 07Ch
GRCG_RMW equ 0C0h
SCREEN_HEIGHT equ 400
GATHER_POINT_H equ 8
PIXEL_SHIFT_MASK equ 7
RASTER_SHIFT_BYTES equ 4
VRAM_ROW_BYTES equ (640 / 8)
VRAM_PLANE_BYTES equ (640 * 400 / 8)
WORD_BYTES equ 2
BYTE_BYTES equ 1

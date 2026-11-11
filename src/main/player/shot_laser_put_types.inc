; Source-level screen geometry and byte mask roles, no generated pixel bytes.
VRAM_SEGMENT equ 0A800h
VRAM_ROW_BYTES equ (640 / 8)
VRAM_PLANE_BYTES equ (640 * 400 / 8)
SCREEN_HEIGHT equ 400
PIXELS_PER_BYTE_SHIFT equ 3
PIXEL_SHIFT_MASK equ 7
SUBPIXELS_PER_PIXEL_SHIFT equ 4
VRAM_Y_SHIFT1 equ 6
VRAM_Y_SHIFT2 equ 2
WORD_BYTES equ 2
BYTE_BYTES equ 1

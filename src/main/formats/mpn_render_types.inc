; MPN image geometry: four consecutive 16x16 monochrome planes.
MPN_TILE_W equ 16
MPN_TILE_H equ 16
MPN_PLANES equ 4
MPN_ROW_BYTES equ (MPN_TILE_W / 8)
MPN_IMAGE_BYTES equ (MPN_ROW_BYTES * MPN_TILE_H * MPN_PLANES)
MPN_IMAGE_SHIFT equ 7
.errnz MPN_IMAGE_BYTES - (1 shl MPN_IMAGE_SHIFT)
VRAM_ROW_BYTES equ (640 / 8)
SEG_PLANE_B equ 0A800h
SEG_PLANE_R equ 0B000h
SEG_PLANE_G equ 0B800h
SEG_PLANE_E equ 0E000h
; The original far return occupies four bytes before the Pascal arguments.
MPN_ARG_IMAGE equ 4
MPN_ARG_TOP equ 6
MPN_ARG_LEFT equ 8

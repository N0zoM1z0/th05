; Physical PC-98 verdict-screen geometry and GRCG settings.
VERDICT_ROWS        equ 352
VERDICT_COL_BYTES   equ (320 / 8)
VERDICT_WORDS       equ (VERDICT_COL_BYTES / 2)
VRAM_ROW_STRIDE     equ (640 / 8)
ROW_SKIP            equ (VRAM_ROW_STRIDE - VERDICT_COL_BYTES)
PLANE_E_SEGMENT     equ 0E000h
PLANE_B_SEGMENT     equ 0A800h
GRCG_TDW_MODE       equ 080h
GRCG_RMW_MODE       equ 0C0h
GRCG_TILE_COLOR     equ 1
GRCG_MASK_COLOR     equ 13
GRCG_CONTROL_PORT   equ 07Ch

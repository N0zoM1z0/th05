; Full CDG record and PC-98 planar geometry; segment handles are 16-bit words.
ROW_SIZE equ (640 / 8)
SEG_PLANE_B equ 0A800h
SEG_PLANE_R equ 0B000h
SEG_PLANE_G equ 0B800h
SEG_PLANE_E equ 0E000h
SEG_PLANE_DIST_BRG equ (SEG_PLANE_R - SEG_PLANE_B)
SEG_PLANE_DIST_E equ (SEG_PLANE_E - SEG_PLANE_G)
CDG_SLOT_COUNT equ 64
cdg_t struc
 plane_size dw ?
 pixel_w dw ?
 pixel_h dw ?
 offset_at_bottom_left dw ?
 vram_dword_w dw ?
 image_count db ?
 plane_layout db ?
 seg_alpha dw ?
 seg_colors dw ?
cdg_t ends

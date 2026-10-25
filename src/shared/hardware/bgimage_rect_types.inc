; Full four-plane cache record: each member is a 16-bit segment handle.
bgimage_planes_t struc
 B dw ?
 R dw ?
 G dw ?
 E dw ?
bgimage_planes_t ends
ROW_SIZE equ (640 / 8)
SEG_PLANE_B equ 0A800h
SEG_PLANE_R equ 0B000h
SEG_PLANE_G equ 0B800h
SEG_PLANE_E equ 0E000h

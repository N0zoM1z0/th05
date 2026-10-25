; Full PI72 and palette48 ABI, eight complete slots, no image/header payload.
RES_X equ 640
RES_Y equ 400
ROW_BYTES equ (RES_X/8)
PLANE_BYTES equ (ROW_BYTES*RES_Y)
SEG_PLANE_B equ 0A800h
PI_SLOT_COUNT equ 8
PI_MASK_COUNT equ 4
PI_MASK_H equ 4
rgb8_t struc
 r db ?
 g db ?
 b db ?
rgb8_t ends
palette8_t struc
 colors rgb8_t 16 dup (<?>)
palette8_t ends
far_pointer_t struc
 pointer_offset dw ?
 pointer_segment dw ?
far_pointer_t ends
pi_header_t struc
 comment far_pointer_t <?>
 commentlen dw ?
 mode db ?
 aspect_n db ?
 aspect_m db ?
 plane db ?
 machine db 4 dup (?)
 maexlen dw ?
 maex far_pointer_t <?>
 xsize dw ?
 ysize dw ?
 palette palette8_t <?>
pi_header_t ends

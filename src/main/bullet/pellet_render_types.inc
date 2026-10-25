; Full 4-byte queue union, transformed in place by the top pass.
pellet_render_t struc
 union
  struc
   PRT_left dw ?
   PRT_top dw ?
  ends
  struc
   PRB_vram_offset dw ?
   PRB_sprite_offset dw ?
  ends
 ends
pellet_render_t ends
PELLET_H equ 8
RES_Y equ 400
ROW_SIZE equ (640 / 8)
PLANE_SIZE equ (ROW_SIZE * RES_Y)

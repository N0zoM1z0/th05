; Full canonical 16-bit geometry, Laser and scratch overlays. No resource data.
SUBPIXEL_BITS equ 4
PLAYFIELD_LEFT equ 32
PLAYFIELD_TOP equ 16
point_t struc
 x dw ?
 y dw ?
point_t ends
motion_t struc
 cur point_t <?>
 prev point_t <?>
 velocity point_t <?>
motion_t ends
laser_width_t union
 shrink db ?
 nonshrink db ?
laser_width_t ends
laser_coords_t struc
 LC_origin point_t <?>
 LC_start dw ?
 LC_end dw ?
 LC_angle db ?
 LC_width laser_width_t <?>
laser_coords_t ends
laser_active_age_t union
 grow dw ?
 moveout dw ?
laser_active_age_t ends
laser_t struc
 flag db ?
 color db ?
 coords laser_coords_t <?>
 shootout_speed dw ?
 age dw ?
 active_at_age laser_active_age_t <?>
 shrink_at_age dw ?
 grow_to_width db ?
 unused db 3 dup (?)
laser_t ends
; Full flag domain retained; the rendering family receives the selected Laser.
LF_FREE equ 0
LF_SHOOTOUT equ 1
LF_FIXED_WAIT_TO_GROW equ 2
LF_FIXED_GROW equ 3
LF_FIXED_ACTIVE equ 4
LF_FIXED_SHRINK equ 5
LF_FIXED_SHRINK_AND_WAIT_TO_GROW equ 6
LF_SHOOTOUT_DECAY equ 7
ray_construction_t struc
 RC_start_ccw point_t <?>
 RC_unused_1 point_t <?>
 RC_unused_2 point_t <?>
 RC_end_ccw point_t <?>
 RC_unused_3 point_t <?>
 RC_origin_ccw point_t <?>
 RC_delta point_t <?>
 RC_origin point_t <?>
ray_construction_t ends
ray_corners_t struc
 start_ccw point_t <?>
 start_cw point_t <?>
 end_cw point_t <?>
 end_ccw point_t <?>
ray_corners_t ends
ray_scratch_t union
 construction ray_construction_t <?>
 corners ray_corners_t <?>
 clipped point_t 8 dup (<?>)
ray_scratch_t ends
hit_scratch_t struc
 test_center point_t <?>
 origin point_t <?>
hit_scratch_t ends
RAY_BYTES equ size ray_scratch_t
RAY_ORIGIN equ (ray_construction_t.RC_origin - RAY_BYTES)
RAY_DELTA equ (ray_construction_t.RC_delta - RAY_BYTES)
RAY_ORIGIN_CCW equ (ray_construction_t.RC_origin_ccw - RAY_BYTES)
RAY_START_CCW equ (ray_construction_t.RC_start_ccw - RAY_BYTES)
RAY_END_CCW equ (ray_construction_t.RC_end_ccw - RAY_BYTES)

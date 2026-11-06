; Complete 18-byte TH05 shot, with both previous/current coordinates retained.
SHOT_RECORD struc
 SH_flag db ?
 SH_age db ?
 SH_cur_x dw ?
 SH_cur_y dw ?
 SH_prev_x dw ?
 SH_prev_y dw ?
 SH_velocity_x dw ?
 SH_velocity_y dw ?
 SH_patnum db ?
 SH_type db ?
 SH_damage db ?
 SH_angle db ?
SHOT_RECORD ends
SHOT_FREE equ 0
SHOT_ALIVE equ 1
SHOT_POOL_COUNT equ 64
SHOT_POINT_BYTES equ 4
SHOT_PRIMARY_SPEED equ (12 * 16)
SHOT_DEFAULT_VELOCITY equ ((-SHOT_PRIMARY_SPEED) shl 16)
SHOT_ARG_ANGLE equ 2
SHOT_ARG_VELOCITY equ 4
SHOT_ARGUMENT_BYTES equ 4
SHOT_ANGLE_FROM_VELOCITY equ (SHOT_RECORD.SH_angle - SHOT_RECORD.SH_velocity_x)
SHOT_POWER_BOUND_COUNT equ 9
SHOT_FUNCTION_WORD_BYTES equ 2
IF (size SHOT_RECORD) ne 18
 .ERR
ENDIF

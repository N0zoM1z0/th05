; Symbol-only original MAINE context. Every hole is outside the producer CODE.
.386
.model large
GROUP01_BASE equ 0A540h
UNIT_START equ 0D853h
UNIT_SIZE equ 01E3h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0E800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRC_SETCLIP
org 00DCCh
GRC_SETCLIP label far
public IATAN2
org 01A8Ch
IATAN2 label far
public IHYPOT
org 01AF8h
IHYPOT label far
public IRAND
org 01DF8h
IRAND label far
org GROUP01_BASE
_TEXT ends

SCORE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_TEXT
public @SPACE_WINDOW_SET$QIIII
org (0D31Fh - GROUP01_BASE)
@SPACE_WINDOW_SET$QIIII label near
org (0D387h - GROUP01_BASE)
SCORE_TEXT ends

; Both the accepted lifecycle prefix and the unaccepted updater are foreign.
STAFF_LIFE_TEXT segment byte public 'CODE' use16
org (UNIT_START - 0D387h)
STAFF_LIFE_TEXT ends

STAFF_TRAIL_TEXT segment byte public 'CODE' use16
STAFF_TRAIL_TEXT ends

STAFF_TRAIL_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
STAFF_TRAIL_TAIL ends
group_01 group SCORE_TEXT, STAFF_LIFE_TEXT, STAFF_TRAIL_TEXT, STAFF_TRAIL_TAIL

SHARED segment para public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 04A0h
VECTOR2_AT label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends

_DATA segment word public 'DATA' use16
public _staff_back_page
org 0173Ah
_staff_back_page label byte
public _staff_spark_cursor
org 0173Ch
_staff_spark_cursor label word
public _staff_orb_opening_frame
org 0173Eh
_staff_orb_opening_frame label word
public _staff_camera_accel_phase
org 01740h
_staff_camera_accel_phase label byte
public _space_window_w
org 050CEh
_space_window_w label word
public _space_window_h
org 050D0h
_space_window_h label word
public _staff_spawn_point
org 050D2h
_staff_spawn_point label dword
public _space_window_center
org 050D6h
_space_window_center label dword
public _space_camera_velocity
org 050DAh
_space_camera_velocity label dword
public _staff_particle_decay
org 050DEh
_staff_particle_decay label word
public _staff_frame
org 050E2h
_staff_frame label word
public _particles
org 050E4h
_particles label byte
public _orb_trails_center
org 055F8h
_orb_trails_center label dword
public _stars_center
org 05618h
_stars_center label dword
org 0C4D8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

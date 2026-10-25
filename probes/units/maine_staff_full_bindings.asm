; Full17-function natural staff TU, with failed updater/render retained.
; Only real foreign symbols and outside extents; no near stubs, inside holes or .stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BOXFILL
org 0BCEh
GRCG_BOXFILL label far
public GRCG_BYTEBOXFILL_X
org 0C9Eh
GRCG_BYTEBOXFILL_X label far
public GRCG_CIRCLEFILL
org 0D36h
GRCG_CIRCLEFILL label far
public GRC_SETCLIP
org 0DCCh
GRC_SETCLIP label far
public GRCG_SETCOLOR
org 0F28h
GRCG_SETCOLOR label far
public GAIJI_PUTSA
org 0125Eh
GAIJI_PUTSA label far
public IATAN2
org 01A8Ch
IATAN2 label far
public IHYPOT
org 01AF8h
IHYPOT label far
public PALETTE_SHOW
org 01B8Ah
PALETTE_SHOW label far
public IRAND
org 01DF8h
IRAND label far
public TEXT_CLEAR
org 02298h
TEXT_CLEAR label far
public TEXT_PUTSA
org 022AAh
TEXT_PUTSA label far
public SUPER_PUT_RECT
org 02974h
SUPER_PUT_RECT label far
public SUPER_PUT_TINY_SMALL
org 02DB6h
SUPER_PUT_TINY_SMALL label far
org 0A540h
_TEXT ends
STAFF_FULL_TEXT segment byte public 'CODE' use16
org (0D31Fh - 0A540h)
STAFF_FULL_TEXT ends
STAFF_FULL_TAIL segment byte public 'CODE' use16
org (0E800h - 0E3A4h)
STAFF_FULL_TAIL ends
group_01 group STAFF_FULL_TEXT, STAFF_FULL_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8
org 0274h
CDG_PUT_NOALPHA_8 label far
public VECTOR2_AT
org 04A0h
VECTOR2_AT label far
public @snd_bgm_measure$qv
org 0A42h
@snd_bgm_measure$qv label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
org 01910h
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
public _staff_rain_cursor
org 01742h
_staff_rain_cursor label word
public _staff_rain_frame
org 01744h
_staff_rain_frame label word
public _staff_text_clear_requested
org 01746h
_staff_text_clear_requested label byte
public _staff_image_phase_a
org 01748h
_staff_image_phase_a label word
public _staff_image_phase_b
org 0174Ah
_staff_image_phase_b label word
public _staff_image_cover_a
org 0174Ch
_staff_image_cover_a label byte
public _staff_image_cover_b
org 0174Fh
_staff_image_cover_b label byte
public _Palettes
org 01D9Ah
_Palettes label byte
public _cdg_slots
org 029FEh
_cdg_slots label byte
public _staff_image_wipe_extent_a
org 050C4h
_staff_image_wipe_extent_a label word
public _staff_image_wipe_frame_a
org 050C6h
_staff_image_wipe_frame_a label word
public _staff_image_wipe_extent_b
org 050C8h
_staff_image_wipe_extent_b label word
public _staff_image_wipe_frame_b
org 050CAh
_staff_image_wipe_frame_b label word
public _staff_orb_sprite_frame
org 050CCh
_staff_orb_sprite_frame label byte
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
public _staff_bgm_measure
org 050E0h
_staff_bgm_measure label word
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

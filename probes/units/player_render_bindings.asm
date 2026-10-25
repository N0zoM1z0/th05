; Actual foreign graphics endpoints around the complete player renderer.
; No instructions, image values, stack, entry or inside-owner gaps.
.386
ifdef BINDINGS_AFTER
PLAYER_RENDER_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_RENDER_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - 0cea0h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
PLAYER_RENDER_TEXT ends
main_01 group PLAYER_RENDER_TEXT
PLAYER_RENDER_SHARED_GAP segment byte public 'CODE' use16
org (14ab0h - 0df28h)
PLAYER_RENDER_SHARED_GAP ends
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
PLAYER_RENDER_DATA_GAP segment byte public 'CODE' use16
org (209d0h - 15270h)
PLAYER_RENDER_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _player_pos, _player_option_pos_cur, _player_invincibility_time
public _shot_level, _miss_time, _miss_explosion_angle, _miss_explosion_radius
public _drawpoint, _stage_frame_mod4
org 036d2h
_player_pos label byte
org 036e6h
_player_option_pos_cur label byte
org 036eeh
_player_invincibility_time label byte
org 036f1h
_shot_level label byte
org 036f4h
_miss_time label byte
org 036f7h
_miss_explosion_angle label byte
org 036f8h
_miss_explosion_radius label word
org 036feh
_drawpoint label byte
org 05767h
_stage_frame_mod4 label byte
org 05768h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
else
_TEXT segment word public 'CODE' use16
public SUPER_ROLL_PUT_1PLANE, SUPER_ROLL_PUT
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 02fe0h
SUPER_ROLL_PUT label far
org 0ae10h
_TEXT ends
PLAYER_RENDER_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW, @grcg_setmode_rmw$qv
org (0c07ch - 0ae10h)
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
org (0c1f8h - 0ae10h)
@grcg_setmode_rmw$qv label near
org (0cd56h - 0ae10h)
PLAYER_RENDER_TEXT ends
main_01 group PLAYER_RENDER_TEXT
endif
end

; True foreign code/data context for the complete174-byte stage runtime init.
; No instructions, initialized data, source-ownedbytes or stack allocation.
.386
.model large
UNIT_START equ 0b55ah
UNIT_END equ 0b608h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
STAGE_RUNTIME_TEXT segment byte public 'CODE' use16
org (UNIT_START - 0ae10h)
STAGE_RUNTIME_TEXT ends
STAGE_RUNTIME_TAIL segment byte public 'CODE' use16
assume cs:STAGE_RUNTIME_TAIL
public @TILES_RENDER_ALL$QV
org (0bbech - UNIT_END)
@TILES_RENDER_ALL$QV label near
public @tiles_invalidate_reset$qv
org (0bd24h - UNIT_END)
@tiles_invalidate_reset$qv label near
public @randring_fill$qv
org (0c6e8h - UNIT_END)
@randring_fill$qv label near
public @hud_put$qv
org (0d323h - UNIT_END)
@hud_put$qv label far
public HUD_SCORE_PUT
org (0d4c0h - UNIT_END)
HUD_SCORE_PUT label near
public _sparks_init
org (0e134h - UNIT_END)
_sparks_init label near
public POINTNUMS_INIT
org (0e16eh - UNIT_END)
POINTNUMS_INIT label near
public SHOT_LEVEL_UPDATE
org (0e3e2h - UNIT_END)
SHOT_LEVEL_UPDATE label far
public @bomb_reset$qv
org (0fa50h - UNIT_END)
@bomb_reset$qv label near
public _stage_state_init
org (012ac4h - UNIT_END)
_stage_state_init label near
public @std_update_frames_then_animate_d$qv
org (0139fch - UNIT_END)
@std_update_frames_then_animate_d$qv label near
org (14ab0h - UNIT_END)
STAGE_RUNTIME_TAIL ends
main_01 group STAGE_RUNTIME_TEXT, STAGE_RUNTIME_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
STAGE_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:STAGE_RUNTIME_MAIN03_CONTEXT
public @items_init$qv
org 0799eh
@items_init$qv label far
org (209d0h - 15270h)
STAGE_RUNTIME_MAIN03_CONTEXT ends
main_03 group STAGE_RUNTIME_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _scroll_row_advance_current
org 034f6h
_scroll_row_advance_current label byte
public _scroll_line_on_page
org 034feh
_scroll_line_on_page label word
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _scroll_row_advance_previous
org 03510h
_scroll_row_advance_previous label byte
public _tile_ring_scroll_row_prev
org 03512h
_tile_ring_scroll_row_prev label word
public _scroll_subpixel_line
org 03514h
_scroll_subpixel_line label byte
public _scroll_line
org 03516h
_scroll_line label word
public _scroll_active
org 0351ah
_scroll_active label byte
public _playfield_shake_x
org 0351ch
_playfield_shake_x label word
public _playfield_shake_y
org 0351eh
_playfield_shake_y label word
public _player_pos
org 036d2h
_player_pos label byte
public _player_invincibility_time
org 036eeh
_player_invincibility_time label byte
public _player_miss_animation_frame
org 036efh
_player_miss_animation_frame label byte
public _shot_time
org 036f2h
_shot_time label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
public _miss_time
org 036f4h
_miss_time label byte
public _stage_point_items_collected
org 036f5h
_stage_point_items_collected label byte
public _stage_frame
org 05764h
_stage_frame label word
public _bombing_disabled
org 0c4bah
_bombing_disabled label byte
public _std_update
org 0c656h
_std_update label word
org 0c658h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

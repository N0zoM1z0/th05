; Symbol-only context for the complete natural bullet update producer.
; No implementation or target payload bytes; all holes are outside C++ code.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 01f3ah
public IATAN2
IATAN2 label far
org 0ae10h
_TEXT ends
BULLET_UPDATE_MAIN01 segment byte public 'CODE' use16
assume cs:BULLET_UPDATE_MAIN01
org 021a2h
public SELECT_FOR_RANK
SELECT_FOR_RANK label far
org 0242eh
public @hud_graze_put$qv
@hud_graze_put$qv label far
org 07459h
public @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
@OVERLAY_POPUP_UPDATE_AND_RENDER$QV label near
org 09ca0h
BULLET_UPDATE_MAIN01 ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
main_01 group BULLET_UPDATE_MAIN01, HUD_OVRL_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
org 003b0h
public VECTOR2_AT
VECTOR2_AT label far
SHARED ends
BULLET_UPDATE_FRAME_GAP segment byte public 'CODE' use16
assume cs:BULLET_UPDATE_FRAME_GAP
org 00410h
BULLET_UPDATE_FRAME_GAP ends
BULLET_U_TEXT segment word public 'CODE' use16
assume cs:BULLET_U_TEXT
org 0000ch
public @PlayfieldMotion@update_seg3$qv
@PlayfieldMotion@update_seg3$qv label near
org 0006ah
public VECTOR2_NEAR
VECTOR2_NEAR label near
org 017c0h
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG3
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG3 label near
org 01bd2h
public @POINTNUMS_ADD_WHITE$QIIUI
@POINTNUMS_ADD_WHITE$QIIUI label near
org 01c16h
public @SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II
@SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II label far
org 01ce2h
public @BULLET_PATNUM_FOR_ANGLE$QUIUC
@BULLET_PATNUM_FOR_ANGLE$QUIUC label near
org 06bdeh
BULLET_U_TEXT ends
BULLET_UPDATE_TAIL segment byte public 'CODE' use16
assume cs:BULLET_UPDATE_TAIL
org 0078ah
public @ITEMS_ADD$QII11ITEM_TYPE_T
@ITEMS_ADD$QII11ITEM_TYPE_T label near
BULLET_UPDATE_TAIL ends
main_03 group BULLET_U_TEXT, BULLET_UPDATE_TAIL
BULLET_UPDATE_DS_GAP segment byte public 'CODE' use16
assume cs:BULLET_UPDATE_DS_GAP
org 03da5h
BULLET_UPDATE_DS_GAP ends
_DATA segment word public 'DATA' use16
org 01a5ch
public _bullet_zap_drop_point_items
_bullet_zap_drop_point_items label byte
org 036d2h
public _player_pos
_player_pos label byte
org 036eeh
public _player_invincibility_time
_player_invincibility_time label byte
org 036f3h
public _player_is_hit
_player_is_hit label byte
org 036feh
public _drawpoint
_drawpoint label byte
org 03712h
public _score_delta
_score_delta label byte
org 03f94h
public _bullet_special
_bullet_special label byte
org 03f96h
public _bullet_zap
_bullet_zap label byte
org 03f97h
public _bullet_clear_time
_bullet_clear_time label byte
org 03f98h
public _stage_graze
_stage_graze label byte
org 03f9ah
public _graze_score
_graze_score label byte
org 03f9ch
public _pellets_render_count
_pellets_render_count label byte
org 04abdh
public _overlay_popup_id_new
_overlay_popup_id_new label byte
org 04ac0h
public _overlay2
_overlay2 label byte
org 04ac4h
public _overlay_popup_bonus
_overlay_popup_bonus label byte
org 05766h
public _stage_frame_mod2
_stage_frame_mod2 label byte
org 0576ah
public _slowdown_factor
_slowdown_factor label byte
org 0576fh
public _rank
_rank label byte
org 05776h
public _turbo_mode
_turbo_mode label byte
org 0577ch
public _slowdown_caused_by_bullets
_slowdown_caused_by_bullets label byte
org 05f2ah
public _bullets
_bullets label byte
org 0912ah
public _pellets_render
_pellets_render label byte
org 0c340h
public _pellet_clouds_render
_pellet_clouds_render label byte
org 0c4a8h
public _pellet_clouds_render_count
_pellet_clouds_render_count label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

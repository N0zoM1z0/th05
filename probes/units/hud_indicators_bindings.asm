; Complete four natural indicators [D1A2h,D28Bh), actual external UI objects.
; No foreign instructions, UI values, stack or inside-owner holes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_INDICATORS_TEXT segment byte public 'CODE' use16
assume cs:HUD_INDICATORS_TEXT
org 02392h
HUD_INDICATORS_TEXT ends
HUD_INDICATOR_AFTER_TEXT segment byte public 'CODE' use16
assume cs:HUD_INDICATOR_AFTER_TEXT
public HUD_BAR_PUT, @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
org 001e9h
HUD_BAR_PUT label near
org 04fdeh
@OVERLAY_POPUP_UPDATE_AND_RENDER$QV label near
org 07825h
HUD_INDICATOR_AFTER_TEXT ends
main_01 group HUD_INDICATORS_TEXT, HUD_INDICATOR_AFTER_TEXT
HUD_INDICATOR_SHARED_GAP segment byte public 'CODE' use16
org 007c0h
HUD_INDICATOR_SHARED_GAP ends
HUD_INDICATOR_MAIN03_TEXT segment byte public 'CODE' use16
assume cs:HUD_INDICATOR_MAIN03_TEXT
public @HUD_5_DIGIT_PUT$QUIUIUIUI
org 0063ah
@HUD_5_DIGIT_PUT$QUIUIUIUI label far
org 0b760h
HUD_INDICATOR_MAIN03_TEXT ends
main_03 group HUD_INDICATOR_MAIN03_TEXT
_DATA segment word public 'DATA' use16
public _dream_prev, _HUD_DREAM_COLORS, _HUD_POWER_COLORS
public _extend_point_items_collected, _power, _shot_level
public _stage_point_items_collected, _dream, _bullet_clear_time, _stage_graze
public _overlay_popup_id_new, _overlay2
org 013ceh
_dream_prev label byte
org 013cfh
_HUD_DREAM_COLORS label byte
org 013d8h
_HUD_POWER_COLORS label byte
org 01e7eh
_extend_point_items_collected label word
org 036f0h
_power label byte
org 036f1h
_shot_level label byte
org 036f5h
_stage_point_items_collected label byte
org 036f6h
_dream label byte
org 03f97h
_bullet_clear_time label byte
org 03f98h
_stage_graze label word
org 04abdh
_overlay_popup_id_new label byte
org 04ac0h
_overlay2 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Genuine outside-only full HUD context. All861 preceding code bytes come
; from real frozen C++ bodies, never ORG, padding, helper stubs or copied data.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTCA
org 01d7ah
GAIJI_PUTCA label far
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
public TEXT_PUTSA
org 02598h
TEXT_PUTSA label far
org 0ae10h
_TEXT ends
HUD_COMBINED_PREFIX segment byte public 'CODE' use16
org (0cfc6h - 0ae10h)
HUD_COMBINED_PREFIX ends
HUD_COMBINED_TEXT segment byte public 'CODE' use16
HUD_COMBINED_TEXT ends
HUD_COMBINED_AFTER_TEXT segment byte public 'CODE' use16
assume cs:HUD_COMBINED_AFTER_TEXT
public HUD_BAR_PUT
HUD_BAR_PUT label near
public HUD_SCORE_PUT
org (0d4c0h - 0d474h)
HUD_SCORE_PUT label near
public @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
org (012269h - 0d474h)
@OVERLAY_POPUP_UPDATE_AND_RENDER$QV label near
org (014ab0h - 0d474h)
HUD_COMBINED_AFTER_TEXT ends
main_01 group HUD_COMBINED_PREFIX, HUD_COMBINED_TEXT, HUD_COMBINED_AFTER_TEXT
HUD_COMBINED_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
HUD_COMBINED_SHARED_SPACE ends
HUD_COMBINED_MAIN03 segment byte public 'CODE' use16
assume cs:HUD_COMBINED_MAIN03
public @HUD_5_DIGIT_PUT$QUIUIUIUI
org 063ah
@HUD_5_DIGIT_PUT$QUIUIUIUI label far
org 0b760h
HUD_COMBINED_MAIN03 ends
main_03 group HUD_COMBINED_MAIN03
_DATA segment word public 'DATA' use16
public _hiscore_popup_shown
org 01373h
_hiscore_popup_shown label byte
public _glEASY
org 01374h
_glEASY label byte
public _gsSCORE
org 0139ch
_gsSCORE label byte
public _gsHISCORE
org 013a1h
_gsHISCORE label byte
public _gsREIGEKI
org 013a6h
_gsREIGEKI label byte
public _gsREIMU
org 013abh
_gsREIMU label byte
public _gsREIRYOKU
org 013b0h
_gsREIRYOKU label byte
public _gsBOMB
org 013b5h
_gsBOMB label byte
public _gsPLAYER
org 013bah
_gsPLAYER label byte
public _gsPOWER
org 013bfh
_gsPOWER label byte
public _gsENEMY
org 013c4h
_gsENEMY label byte
public _gsRUIKEI
org 013c9h
_gsRUIKEI label byte
public _dream_prev
org 013ceh
_dream_prev label byte
public _HUD_DREAM_COLORS
org 013cfh
_HUD_DREAM_COLORS label byte
public _HUD_POWER_COLORS
org 013d8h
_HUD_POWER_COLORS label byte
public _gHUD_HP_BLANK
org 013e2h
_gHUD_HP_BLANK label byte
public _HUD_HP_COLORS
org 013ebh
_HUD_HP_COLORS label byte
public _hud_lives_extra
org 013f0h
_hud_lives_extra label byte
public _hud_bombs_extra
org 013fbh
_hud_bombs_extra label byte
public _extend_point_items_collected
org 01e7eh
_extend_point_items_collected label word
public _power
org 036f0h
_power label byte
public _shot_level
org 036f1h
_shot_level label byte
public _stage_point_items_collected
org 036f5h
_stage_point_items_collected label byte
public _dream
org 036f6h
_dream label byte
public _score
org 03702h
_score label byte
public _score_delta
org 03712h
_score_delta label dword
public _score_delta_frame
org 03716h
_score_delta_frame label dword
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _stage_graze
org 03f98h
_stage_graze label word
public _resident
org 041fch
_resident label dword
public _overlay_popup_id_new
org 04abdh
_overlay_popup_id_new label byte
public _overlay2
org 04ac0h
_overlay2 label word
public _lives
org 04ad4h
_lives label byte
public _bombs
org 04ad5h
_bombs label byte
public _rank
org 0576fh
_rank label byte
public _playchar
org 05773h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

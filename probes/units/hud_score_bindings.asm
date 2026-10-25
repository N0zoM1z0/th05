; Real external frames/addresses only; no state, divisor or instruction bytes.
.386
.model large
main_01 group MAIN_01_TEXT, FOREIGN_HUD_SCORE_TAIL
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org (0d4c0h - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_HUD_SCORE_TAIL segment byte public 'CODE' use16
assume cs:main_01
public @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
org (012269h - 0d5c1h)
@OVERLAY_POPUP_UPDATE_AND_RENDER$QV label near
org (014ab0h - 0d5c1h)
FOREIGN_HUD_SCORE_TAIL ends
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_HUD_SCORE_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_HUD_SCORE_MAIN03 ends
main_03 group FOREIGN_HUD_SCORE_MAIN03
_DATA segment word public 'DATA' use16
public _score, _hiscore, _hiscore_popup_shown, _score_delta, _score_delta_frame
public _hud_gaiji_row, _FIVE_DIGIT_POWERS_OF_10, _overlay_popup_id_new, _overlay2
org 01373h
_hiscore_popup_shown label byte
org 01422h
_FIVE_DIGIT_POWERS_OF_10 label word
org 0142ch
_hud_gaiji_row label byte
org 03702h
_score label byte
org 0370ah
_hiscore label byte
org 03712h
_score_delta label dword
org 03716h
_score_delta_frame label dword
org 04abdh
_overlay_popup_id_new label byte
org 04ac0h
_overlay2 label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

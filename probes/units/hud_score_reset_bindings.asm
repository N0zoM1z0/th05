; Outside-only original frame/symbol context. No owned instructions or values.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
SCORE_RESET_PREFIX segment byte public 'CODE' use16
org (0cfc6h - 0ae10h)
SCORE_RESET_PREFIX ends
SCORE_RESET_TEXT segment byte public 'CODE' use16
SCORE_RESET_TEXT ends
SCORE_RESET_AFTER_TEXT segment byte public 'CODE' use16
assume cs:SCORE_RESET_AFTER_TEXT
org (014ab0h - 0d035h)
SCORE_RESET_AFTER_TEXT ends
main_01 group SCORE_RESET_PREFIX, SCORE_RESET_TEXT, SCORE_RESET_AFTER_TEXT
SCORE_RESET_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SCORE_RESET_SHARED_SPACE ends
SCORE_RESET_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
SCORE_RESET_MAIN03_SPACE ends
main_03 group SCORE_RESET_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _hiscore_popup_shown
org 01373h
_hiscore_popup_shown label byte
public _score
org 03702h
_score label byte
public _score_delta
org 03712h
_score_delta label dword
public _score_delta_frame
org 03716h
_score_delta_frame label dword
public _resident
org 041fch
_resident label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

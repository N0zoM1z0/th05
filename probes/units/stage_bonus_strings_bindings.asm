; Outside context for complete readable stage-bonus text DATA.
; The source defines all719 bytes; glyph arrays preceding it remain foreign.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BONUS_UI_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
BONUS_UI_MAIN01_SPACE ends
main_01 group BONUS_UI_MAIN01_SPACE
BONUS_UI_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
BONUS_UI_SHARED_SPACE ends
BONUS_UI_TEXT segment byte public 'CODE' use16
org 0b760h
BONUS_UI_TEXT ends
main_03 group BONUS_UI_TEXT
_DATA segment word public 'DATA' use16
org 01aa1h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

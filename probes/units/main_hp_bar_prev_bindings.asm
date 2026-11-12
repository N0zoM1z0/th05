; Real MAIN CODE group frames and only the previous DATA prefix.
; The candidate state and surrounding alignment are NOT injected here.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_HP_PREV_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
HUD_HP_PREV_DATA_TEXT ends
main_01 group HUD_HP_PREV_DATA_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
HUD_HP_PREV_DATA_TEXT_MAIN03 segment byte public 'CODE' use16
org 0b760h
HUD_HP_PREV_DATA_TEXT_MAIN03 ends
main_03 group HUD_HP_PREV_DATA_TEXT_MAIN03
_DATA segment word public 'DATA' use16
org 1a5eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

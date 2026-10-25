; Actual frames and foreign addresses only; no initialized bytes or assets.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org 01512h
MAIN_01_TEXT ends
FOREIGN_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c41eh)
FOREIGN_TAIL ends
main_01 group MAIN_01_TEXT, FOREIGN_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_MAIN03 ends
main_03 group FOREIGN_MAIN03
_DATA segment word public 'DATA' use16
public _sPELLET
org 00e4ah
_sPELLET label byte
public _sPELLET_BOTTOM
org 00ecah
_sPELLET_BOTTOM label byte
public _pellets_render_count
org 03f9ch
_pellets_render_count label word
public _pellets_render
org 0912ah
_pellets_render label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Original MAIN01 position/CS and DGROUP storage, no owned source bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
POINTNUM_UPDATE_PREFIX segment byte public 'CODE' use16
org (0e1a6h - 0ae10h)
POINTNUM_UPDATE_PREFIX ends
POINTNUM_UPDATE_TEXT segment byte public 'CODE' use16
POINTNUM_UPDATE_TEXT ends
POINTNUM_UPDATE_FOREIGN_TAIL segment para public 'CODE' use16
org (014ab0h - 0e220h)
POINTNUM_UPDATE_FOREIGN_TAIL ends
main_01 group POINTNUM_UPDATE_PREFIX, POINTNUM_UPDATE_TEXT, POINTNUM_UPDATE_FOREIGN_TAIL
POINTNUM_UPDATE_SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
POINTNUM_UPDATE_SHARED ends
POINTNUM_UPDATE_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
POINTNUM_UPDATE_MAIN03 ends
main_03 group POINTNUM_UPDATE_MAIN03
_DATA segment word public 'DATA' use16
public _pointnums_alive, _pointnum_first_yellow_alive, _pointnums
org 03fa6h
_pointnums_alive label word
org 041d8h
_pointnum_first_yellow_alive label word
org 09f04h
_pointnums label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

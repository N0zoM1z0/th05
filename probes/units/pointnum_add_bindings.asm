; Symbol-only original group and foreign state/provider placement.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FOREIGN_POINTNUM_ADD_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_POINTNUM_ADD_MAIN01 ends
main_01 group FOREIGN_POINTNUM_ADD_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
MAIN_03_TEXT segment word public 'CODE' use16
assume cs:main_03
public POINTNUM_DIGITS_SET
org (015870h - 015270h)
POINTNUM_DIGITS_SET label near
org (016e28h - 015270h)
MAIN_03_TEXT ends
FOREIGN_POINTNUM_ADD_TAIL segment byte public 'CODE' use16
org (0209d0h - 016e86h)
FOREIGN_POINTNUM_ADD_TAIL ends
main_03 group MAIN_03_TEXT, FOREIGN_POINTNUM_ADD_TAIL
_DATA segment word public 'DATA' use16
public _pointnum_white_p, _pointnum_yellow_p, _pointnums
org 03fa4h
_pointnum_white_p label byte
org 03fa5h
_pointnum_yellow_p label byte
org 09f04h
_pointnums label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

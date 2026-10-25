; Real frames and the complete foreign bitmap bank's address, without values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org (0be3ah - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_POINTNUM_PUT_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bea4h)
FOREIGN_POINTNUM_PUT_TAIL ends
main_01 group MAIN_01_TEXT, FOREIGN_POINTNUM_PUT_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_POINTNUM_PUT_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_POINTNUM_PUT_MAIN03 ends
main_03 group FOREIGN_POINTNUM_PUT_MAIN03
_DATA segment word public 'DATA' use16
public _sPOINTNUMS
org 0084ah
_sPOINTNUMS label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

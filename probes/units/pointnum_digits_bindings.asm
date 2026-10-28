; Whole foreign table and real group context; no converter bytes supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
POINTNUM_DIGITS_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
POINTNUM_DIGITS_MAIN01 ends
main_01 group POINTNUM_DIGITS_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
POINTNUM_DIGITS_PREFIX segment byte public 'CODE' use16
org (015870h - 015270h)
POINTNUM_DIGITS_PREFIX ends
POINTNUM_DIGITS_TEXT segment word public 'CODE' use16
POINTNUM_DIGITS_TEXT ends
POINTNUM_DIGITS_TAIL segment byte public 'CODE' use16
org (0209d0h - 0158aah)
POINTNUM_DIGITS_TAIL ends
main_03 group POINTNUM_DIGITS_PREFIX, POINTNUM_DIGITS_TEXT, POINTNUM_DIGITS_TAIL
_DATA segment word public 'DATA' use16
public _FIVE_DIGIT_POWERS_OF_10
org 01422h
_FIVE_DIGIT_POWERS_OF_10 label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Source-free MAIN03/DGROUP frames and existing accepted decimal table address.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
POINTNUM_DIGITS_PRE_FRAME segment para public 'CODE' use16
org (015270h - 0AE10h)
POINTNUM_DIGITS_PRE_FRAME ends
POINTNUM_DIGITS_PREFIX segment byte public 'CODE' use16
org (015870h - 015270h)
POINTNUM_DIGITS_PREFIX ends
POINTNUM_DIGITS_REGISTER_TEXT segment byte public 'CODE' use16
POINTNUM_DIGITS_REGISTER_TEXT ends
POINTNUM_DIGITS_TAIL segment byte public 'CODE' use16
org (0209D0h - 0158AAh)
POINTNUM_DIGITS_TAIL ends
main_03 group POINTNUM_DIGITS_PREFIX, POINTNUM_DIGITS_REGISTER_TEXT, POINTNUM_DIGITS_TAIL
_DATA segment word public 'DATA' use16
public _FIVE_DIGIT_POWERS_OF_10
org 01422h
_FIVE_DIGIT_POWERS_OF_10 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

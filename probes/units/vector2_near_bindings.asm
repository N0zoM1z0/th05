; Native frames and overlapping foreign sine/cosine tables, without payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FOREIGN_VECTOR_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_VECTOR_MAIN01 ends
main_01 group FOREIGN_VECTOR_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
VECTOR2_NEAR_TEXT segment word public 'CODE' use16
org (0152dah - 015270h)
VECTOR2_NEAR_TEXT ends
FOREIGN_VECTOR_MAIN03_TAIL segment byte public 'CODE' use16
org (0209d0h - 015311h)
FOREIGN_VECTOR_MAIN03_TAIL ends
main_03 group VECTOR2_NEAR_TEXT, FOREIGN_VECTOR_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8
org 0041ch
_SinTable8 label word
org 0049ch
_CosTable8 label word
org 0069ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Native foreign frames, full handle table and no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TINY16_TEXT segment word public 'CODE' use16
org (0c07ch - 0ae10h)
TINY16_TEXT ends
FOREIGN_TINY16_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c180h)
FOREIGN_TINY16_TAIL ends
main_01 group TINY16_TEXT, FOREIGN_TINY16_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_TINY16_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_TINY16_MAIN03 ends
main_03 group FOREIGN_TINY16_MAIN03
_DATA segment word public 'DATA' use16
public _super_patdata
org 0268ch
_super_patdata label word
org (0268ch + (512 * 2))
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

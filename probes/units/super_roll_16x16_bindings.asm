; Actual foreign frames and handle-table address only; no initialized bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPRITE16_TEXT segment word public 'CODE' use16
org (0c21eh - 0ae10h)
SPRITE16_TEXT ends
FOREIGN_SPRITE16_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c322h)
FOREIGN_SPRITE16_TAIL ends
main_01 group SPRITE16_TEXT, FOREIGN_SPRITE16_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_SPRITE16_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_SPRITE16_MAIN03 ends
main_03 group FOREIGN_SPRITE16_MAIN03
_DATA segment word public 'DATA' use16
public _super_patdata
org 0268ch
_super_patdata label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

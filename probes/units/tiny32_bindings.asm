; Native foreign frames, full handle table and no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TINY32_TEXT segment word public 'CODE' use16
public srpt32x32_vram_topleft
org (0bf60h - 0ae10h)
srpt32x32_vram_topleft label word
org (0bf62h - 0ae10h)
TINY32_TEXT ends
FOREIGN_TINY32_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c07ch)
FOREIGN_TINY32_TAIL ends
main_01 group TINY32_TEXT, FOREIGN_TINY32_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_TINY32_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_TINY32_MAIN03 ends
main_03 group FOREIGN_TINY32_MAIN03
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

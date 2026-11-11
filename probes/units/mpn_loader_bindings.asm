; No implementation bytes. The original loader lives in _TEXT at 41B2.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE, PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
org 0281ah
HMEM_ALLOCBYTE label far
org 041b2h
_TEXT ends
FOREIGN_MPN_PREFIX segment byte public 'CODE' use16
org (0ae10h - 0420eh)
FOREIGN_MPN_PREFIX ends
FOREIGN_MPN_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_MPN_MAIN01 ends
main_01 group FOREIGN_MPN_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_MPN_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_MPN_MAIN03 ends
main_03 group FOREIGN_MPN_MAIN03
_DATA segment word public 'DATA' use16
public Palettes, mpn_images_seg, mpn_last_image
org 0264ah
Palettes label byte
org 03068h
mpn_images_seg label word
org 0306ah
mpn_last_image label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

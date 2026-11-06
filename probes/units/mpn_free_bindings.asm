; Real same-segment allocator and foreign image handle. No initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 0291eh
HMEM_FREE label far
org 0420eh
_TEXT ends
MPN_FREE_TAIL segment byte public 'CODE' use16
org (0ae10h - 04225h)
MPN_FREE_TAIL ends
MPN_FREE_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
MPN_FREE_MAIN01 ends
main_01 group MPN_FREE_MAIN01
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _mpn_images_seg
org 03068h
_mpn_images_seg label word
org 0306ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
BITREVERSE_PRE_SHARED segment byte public 'CODE' use16
org (14AB0h - 0AE10h)
BITREVERSE_PRE_SHARED ends
SHARED segment byte public 'CODE' use16
org (14B58h - 14AB0h)
SHARED ends
BITREVERSE_TAIL segment byte public 'CODE' use16
org (209D0h - 14B76h)
BITREVERSE_TAIL ends
_DATA segment word public 'DATA' use16
public _hflip_lut
org 02E8Eh
_hflip_lut label byte
org 05F00h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

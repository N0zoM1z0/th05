.386
.model large
_TEXT segment word public 'CODE' use16
org 0E800h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0E802h - 0E800h)
SHARED ends
BITREVERSE_TAIL segment byte public 'CODE' use16
org (10110h - 0E820h)
BITREVERSE_TAIL ends
_DATA segment word public 'DATA' use16
public _hflip_lut
org 025DEh
_hflip_lut label byte
org 04F0Eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0D304h - 0D300h)
SHARED ends
BITREVERSE_TAIL segment byte public 'CODE' use16
org (0EFE0h - 0D322h)
BITREVERSE_TAIL ends
_DATA segment word public 'DATA' use16
public _hflip_lut
org 03662h
_hflip_lut label byte
org 03E96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

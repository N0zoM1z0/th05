.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 02322h
HMEM_ALLOCBYTE label far
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0D688h - 0D300h)
SHARED ends
BGIMAGE_TAIL segment byte public 'CODE' use16
org (0EFE0h - 0D725h)
BGIMAGE_TAIL ends
_DATA segment word public 'DATA' use16
public _bgimage
org 009E4h
_bgimage label byte
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

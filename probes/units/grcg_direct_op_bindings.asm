.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0DB21h - 0D300h)
SHARED ends
GRCG_DIRECT_OP_TAIL segment byte public 'CODE' use16
org (0EFE0h - 0DB3Bh)
GRCG_DIRECT_OP_TAIL ends
_DATA segment word public 'DATA' use16
; Reserve the established foreign OP initialized-DATA address range to make
; the isolated MZ stack allocation valid. No image or DATA values supplied.
org 03E96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

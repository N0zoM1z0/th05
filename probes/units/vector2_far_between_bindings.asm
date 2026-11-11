.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01f3ah
IATAN2 label far
org 0ae10h
_TEXT ends
VECTOR_PREFIX_GAP segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
VECTOR_PREFIX_GAP ends
SHARED segment byte public 'CODE' use16
org 4eh
SHARED ends
VECTOR_TAIL segment para public 'CODE' use16
org (0209d0h - 14b60h)
VECTOR_TAIL ends
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8
org 041ch
_SinTable8 label word
org 049ch
_CosTable8 label word
org 04a0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

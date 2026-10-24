; Symbol-only foreign address context. No instructions or table values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0f000h
_TEXT ends
VECTOR_FRAME_GAP segment byte public 'CODE' use16
org 05ab0h
VECTOR_FRAME_GAP ends
SHARED segment para public 'CODE' use16
org 0394h
SHARED ends
VECTOR_DS_GAP segment byte public 'CODE' use16
org 0bb2ch
VECTOR_DS_GAP ends
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8
org 041ch
_SinTable8 label word
org 049ch
_CosTable8 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

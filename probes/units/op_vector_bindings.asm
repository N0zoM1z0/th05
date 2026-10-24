; Symbol-only foreign address context. No instructions or table values.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org 0534h
SHARED ends
VECTOR_DS_GAP segment byte public 'CODE' use16
org 0174ch
VECTOR_DS_GAP ends
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8
org 0590h
_SinTable8 label word
org 0610h
_CosTable8 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real TINY 16-bit CRT and ZUN.COM runtime context, foreign-symbol only.
; C0T _TEXT ends at 0367h, original CODE ends 1642h; user DATA begins
; after C0T 006Eh DATA at 16BEh, with 0140h owned C++ initializer.
.286
_TEXT segment byte public 'CODE' use16
_TEXT ends
FOREIGN_TEXT_TAIL segment byte public 'CODE' use16
public _main
org (004A9h - 00367h)
_main label near
public __abort
org (009D6h - 00367h)
__abort label near
public ___ErrorMessage
org (00A13h - 00367h)
___ErrorMessage label near
public _exit
org (00A87h - 00367h)
_exit label near
public __exit
org (00A9Ah - 00367h)
__exit label near
org (01642h - 00367h)
FOREIGN_TEXT_TAIL ends
_DATA segment word public 'DATA' use16
; The original 320 C++ bytes already occupy 16BE..17FE before this segment.
public __nfile
org (019E0h - 017FEh)
__nfile label word
public __heaplen
org (01A0Ah - 017FEh)
__heaplen label word
public __stklen
org (01A68h - 017FEh)
__stklen label word
org (01AA4h - 017FEh)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _TEXT, FOREIGN_TEXT_TAIL, _DATA, _BSS
end

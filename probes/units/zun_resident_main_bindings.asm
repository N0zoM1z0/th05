; Real tiny-model COM offsets, linked after the pinned, unmodified C0T.OBJ.
; C0T supplies the real entry/prefix and the first6Eh DATA bytes.
; No instructions, resident bytes, options, filename or stack are supplied.
.286
_TEXT segment byte public 'CODE' use16
_TEXT ends
FOREIGN_TEXT_TAIL segment byte public 'CODE' use16
public GRAPH_CLEAR
GRAPH_CLEAR label near
public RESDATA_EXIST
org (005dah - 005b6h)
RESDATA_EXIST label near
public RESDATA_CREATE
org (00622h - 005b6h)
RESDATA_CREATE label near
public FILE_READ
org (00698h - 005b6h)
FILE_READ label near
public FILE_CLOSE
org (007b8h - 005b6h)
FILE_CLOSE label near
public FILE_ROPEN
org (007c6h - 005b6h)
FILE_ROPEN label near
public FILE_WRITE
org (007fch - 005b6h)
FILE_WRITE label near
public FILE_CREATE
org (008a2h - 005b6h)
FILE_CREATE label near
public FILE_SEEK
org (008deh - 005b6h)
FILE_SEEK label near
public FILE_APPEND
org (00920h - 005b6h)
FILE_APPEND label near
public DOS_FREE
org (00970h - 005b6h)
DOS_FREE label near
public DOS_PUTS2
org (00996h - 005b6h)
DOS_PUTS2 label near
public __abort
org (009d6h - 005b6h)
__abort label near
public ___ErrorMessage
org (00a13h - 005b6h)
___ErrorMessage label near
public _exit
org (00a87h - 005b6h)
_exit label near
public __exit
org (00a9ah - 005b6h)
__exit label near
public N_SCOPY@
org (00b66h - 005b6h)
N_SCOPY@ label near
; The real CRT CODE ends at1642; paragraph alignment precedes DATA1650.
org (01642h - 005b6h)
FOREIGN_TEXT_TAIL ends
_DATA segment word public 'DATA' use16
public __nfile
org (019E0h - 017FEh)
__nfile label word
public __heaplen
org (01A0Ah - 017FEh)
__heaplen label word
public __stklen
org (01A68h - 017FEh)
__stklen label word
org (01A94h - 017FEh)
_DATA ends
_CVTSEG segment word public 'DATA' use16
_CVTSEG ends
_SCNSEG segment word public 'DATA' use16
_SCNSEG ends
_INIT_ segment word public 'INITDATA' use16
org 012h
_INIT_ ends
_BSS segment word public 'BSS' use16
org 054h
_BSS ends
DGROUP group _TEXT, FOREIGN_TEXT_TAIL, _DATA, _BSS
end

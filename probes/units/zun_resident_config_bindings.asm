; Real tiny-model COM offsets, linked after the pinned, unmodified C0T.OBJ.
; C0T supplies the real entry/prefix and the first6Eh DATA bytes.
; No instructions, resident bytes, options, filename or stack are supplied.
.286
_TEXT segment byte public 'CODE' use16
_TEXT ends
FOREIGN_TEXT_TAIL segment byte public 'CODE' use16
public _main
_main label near
public FILE_READ
org (00698h - 004a9h)
FILE_READ label near
public FILE_CLOSE
org (007b8h - 004a9h)
FILE_CLOSE label near
public FILE_ROPEN
org (007c6h - 004a9h)
FILE_ROPEN label near
public FILE_WRITE
org (007fch - 004a9h)
FILE_WRITE label near
public FILE_CREATE
org (008a2h - 004a9h)
FILE_CREATE label near
public FILE_SEEK
org (008deh - 004a9h)
FILE_SEEK label near
public FILE_APPEND
org (00920h - 004a9h)
FILE_APPEND label near
public __abort
org (009d6h - 004a9h)
__abort label near
public ___ErrorMessage
org (00a13h - 004a9h)
___ErrorMessage label near
public _exit
org (00a87h - 004a9h)
_exit label near
public __exit
org (00a9ah - 004a9h)
__exit label near
public N_SCOPY@
org (00b66h - 004a9h)
N_SCOPY@ label near
; The real CRT CODE ends at1642; paragraph alignment precedes DATA1650.
org (01642h - 004a9h)
FOREIGN_TEXT_TAIL ends
_DATA segment word public 'DATA' use16
public _debug
_debug label byte
public _OPTS_DEFAULT
org 00001h
_OPTS_DEFAULT label byte
public _ZUN_CFG_FILENAME
org 00007h
_ZUN_CFG_FILENAME label byte
public __nfile
org (019e0h - 016beh)
__nfile label word
public __heaplen
org (01a0ah - 016beh)
__heaplen label word
public __stklen
org (01a68h - 016beh)
__stklen label word
org (01aa4h - 016beh)
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _TEXT, FOREIGN_TEXT_TAIL, _DATA, _BSS
end

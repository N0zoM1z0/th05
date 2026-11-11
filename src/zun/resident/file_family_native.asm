; Exact Master library buffered file read/flush/close/open contribution in
; the ZUN.COM -S resident. Source of original logic: pinned ReC98 Master lib.
.8086
.model tiny
locals
include master_file_tiny.inc
_call macro nearproc
    call near ptr nearproc
endm
.code
org 0100h
resident_file_prefix label byte
org 0698h

include master_read.inc
include master_close.inc
include master_ropen.inc
include master_write.inc
include master_create.inc
include master_seek.inc
include master_append.inc

; Foreign provider near entry: no instruction body supplied in this unit.
org 0980h
DOS_AXDX label near
org 09BEh
DOS_ROPEN label near

; Foreign CODE ends before true DOS DGROUP. The holes are *outside* the
; source-owned four complete functions and never earn code credit.
org 016BEh
.data
org (01872h - 016BEh)
file_BufferSize label word
org (01874h - 016BEh)
file_Handle label word
org (01AAAh - 016BEh)
file_Buffer label dword
org (01AAEh - 016BEh)
file_BufferPos label dword
org (01AB2h - 016BEh)
file_BufPtr label word
org (01AB4h - 016BEh)
file_InReadBuf label word
org (01AB6h - 016BEh)
file_Eof label word
org (01AB8h - 016BEh)
file_ErrorStat label word

end resident_file_prefix

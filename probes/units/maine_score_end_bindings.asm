; TH05 MAINE score file lifecycle original-address symbol-only context.
; No helper bodies, score/filename values, source-owned state or .stack.
.386
.model large
GROUP01_BASE equ 0a540h
UNIT_START equ 0b590h
UNIT_SIZE equ 01a0h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0e800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_APPEND
org 0886h
FILE_APPEND label far
public FILE_CLOSE
org 0946h
FILE_CLOSE label far
public FILE_CREATE
org 0956h
FILE_CREATE label far
public FILE_EXIST
org 0996h
FILE_EXIST label far
public FILE_READ
org 09b2h
FILE_READ label far
public FILE_ROPEN
org 0a66h
FILE_ROPEN label far
public FILE_SEEK
org 0aa2h
FILE_SEEK label far
public FILE_WRITE
org 0af2h
FILE_WRITE label far
org GROUP01_BASE
_TEXT ends

SCORE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_TEXT
public @SCOREDAT_DECODE$QV
org 0f96h
@SCOREDAT_DECODE$QV label near
public @SCOREDAT_ENCODE$QV
org 0fech
@SCOREDAT_ENCODE$QV label near
org (UNIT_START - GROUP01_BASE)
SCORE_TEXT ends

MAINE_SCORE_CODE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
MAINE_SCORE_CODE_TAIL ends
GROUP_01 group SCORE_TEXT, MAINE_SCORE_CODE_TAIL

MAINE_SCORE_FOREIGN_SHARED_SPACE segment para public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
MAINE_SCORE_FOREIGN_SHARED_SPACE ends

_DATA segment word public 'DATA' use16
public _SCOREDAT_FN
org 01524h
_SCOREDAT_FN label byte
public _SCOREDAT_FN_0
org 0152fh
_SCOREDAT_FN_0 label byte
public _SCOREDAT_FN_1
org 0153ah
_SCOREDAT_FN_1 label byte
public _SCOREDAT_FN_2
org 01545h
_SCOREDAT_FN_2 label byte
public _hi
org 04f1ah
_hi label byte
public _rank
org 05077h
_rank label byte
public _playchar
org 05078h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

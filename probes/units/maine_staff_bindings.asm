; Symbol-only original TH05 MAINE staff context. No .stack or game bodies.
.386
.model large

GROUP01_BASE equ 0A540h
UNIT_START equ 0D31Fh
IFNDEF STAFF_CODE_SIZE
STAFF_CODE_SIZE equ 068h
ENDIF
UNIT_END equ (UNIT_START + STAFF_CODE_SIZE)
DGROUP_BASE equ 10110h
OWNED_BSS_START equ 050E4h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRC_SETCLIP
org 0DCCh
GRC_SETCLIP label far
org GROUP01_BASE
_TEXT ends

SCORE_TEXT segment word public 'CODE' use16
assume cs:SCORE_TEXT
org (UNIT_START - GROUP01_BASE)
SCORE_TEXT ends
group_01 group SCORE_TEXT

STAFF_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
STAFF_DGROUP_GAP ends

; Foreign state only. The full compiler-owned BSS follows this DATA hole.
_DATA segment word public 'DATA' use16
public _space_window_w
org 050CEh
_space_window_w label word
public _space_window_h
org 050D0h
_space_window_h label word
public _space_window_center
org 050D6h
_space_window_center label dword
org OWNED_BSS_START
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

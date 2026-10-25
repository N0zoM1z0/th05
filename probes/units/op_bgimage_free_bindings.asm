; Complete decoded OP free50 atD726..D758; all origin holes outside its body.
; No foreign instructions, image data, initialized values or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 02426h
HMEM_FREE label far
org 0d300h
_TEXT ends
SHARED segment byte public 'CODE' use16
assume cs:SHARED
org 00426h
SHARED ends
OP_BGIMAGE_DGROUP_GAP segment byte public 'CODE' use16
org 01888h
OP_BGIMAGE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _bgimage
org 009e4h
_bgimage label byte
; Preserve the real foreign music DATA end for OP's minimum allocation.
; This reserves addresses only and supplies no DATA bytes or authored credit.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

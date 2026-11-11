; Strict symbol-only OP origin frame: no foreign function instructions,
; initialized DATA, imported code copies, or stack bytes are supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SOUND_O, SOUND_I
org 020d4h
SOUND_O label near
org 020eah
SOUND_I label near
org 02bach
_TEXT ends

; This source follows the real OP _TEXT 2BAC..2BD6 contribution. Reserve the
; remainder of the original foreign CODE address space without any LEDATA.
FOREIGN_OP_CODE segment byte public 'CODE' use16
org (0efe0h - 02bd6h)
FOREIGN_OP_CODE ends

_DATA segment word public 'DATA' use16
public js_bexist
org 0544h
js_bexist label word
; Real OP initialized DATA ends at DGROUP:2DEC. The entire foreign DATA
; section is reserved, with no LEDATA or imported initialized byte values.
org 02dech
_DATA ends
_BSS segment word public 'BSS' use16
; The real OP native BSS has at least 1128h bytes, not an invented stack.
org 01128h
_BSS ends
DGROUP group _DATA, _BSS
end

; Original OP frame and outside DATA prefix. No glyph bytes are injected.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
GLYPH_OVERLAY_OP_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
GLYPH_OVERLAY_OP_TEXT ends
op_01 group GLYPH_OVERLAY_OP_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 009beh
_DATA ends
OP_GLYPH_FOREIGN_DATA_TAIL segment word public 'DATA' use16
; Real OP initialized-DATA suffix exists outside the complete mask scope.
; The linker needs the original downstream extent for the MZ SS:SP floor.
org (02817h - 009deh)
OP_GLYPH_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_GLYPH_FOREIGN_DATA_TAIL, _BSS
end

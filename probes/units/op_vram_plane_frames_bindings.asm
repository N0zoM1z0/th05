; Only true OP code groups and DATA prefix; far pointers come from C source.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
VRAM_PLANES_OP_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
VRAM_PLANES_OP_TEXT ends
op_01 group VRAM_PLANES_OP_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 00aa4h
_DATA ends
; The original downstream OP DATA keeps this isolated MZ builder valid;
; all suffix bytes lie strictly outside the candidate's own 16-byte scope.
VRAM_PLANES_OP_FOREIGN_TAIL segment word public 'DATA' use16
org (02817h - 00ab4h)
VRAM_PLANES_OP_FOREIGN_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, VRAM_PLANES_OP_FOREIGN_TAIL, _BSS
end

; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
MEM_ASSIGN_INIT_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
MEM_ASSIGN_INIT_TEXT ends
op_01 group MEM_ASSIGN_INIT_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 09ech
_DATA ends
; Preserve the actual already accepted Music Room DATA end at DS:2817.
; This foreign suffix follows the compiler's complete DS:0980..09EE owner.
; It reserves no source bytes and supplies no DATA values or artificial stack.
SE_PRIORITY_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 009eeh)
SE_PRIORITY_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, SE_PRIORITY_FOREIGN_DATA_TAIL, _BSS
end

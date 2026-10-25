; Real original code frames and foreign DATA prefix. No resource values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
TEXT_FX_DATA_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
TEXT_FX_DATA_TEXT ends
op_01 group TEXT_FX_DATA_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 09a2h
_DATA ends
TEXT_FX_MASK_STORAGE segment word public 'DATA' use16
org 32
TEXT_FX_MASK_STORAGE ends
TEXT_FX_STATE_DATA segment word public 'DATA' use16
TEXT_FX_STATE_DATA ends
; Independently accepted foreign Music Room DATA end; no artificial stack.
TEXT_FX_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 009e2h)
TEXT_FX_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, TEXT_FX_MASK_STORAGE, TEXT_FX_STATE_DATA, TEXT_FX_FOREIGN_DATA_TAIL, _BSS
end

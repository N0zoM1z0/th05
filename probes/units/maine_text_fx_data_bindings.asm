; Real original code frames and foreign DATA prefix. No resource values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
TEXT_FX_DATA_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
TEXT_FX_DATA_TEXT ends
group_01 group TEXT_FX_DATA_TEXT
SHARED segment para public 'CODE' use16
org (010110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 0680h
_DATA ends
TEXT_FX_MASK_STORAGE segment word public 'DATA' use16
org 32
TEXT_FX_MASK_STORAGE ends
TEXT_FX_STATE_DATA segment word public 'DATA' use16
TEXT_FX_STATE_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, TEXT_FX_MASK_STORAGE, TEXT_FX_STATE_DATA, _BSS
end

; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
SOUND_RESOURCE_DATA_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
SOUND_RESOURCE_DATA_TEXT ends
op_01 group SOUND_RESOURCE_DATA_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 0a52h
_DATA ends
; Preserve the actual already accepted Music Room DATA end at DS:2817.
; This foreign suffix follows the compiler's complete DS:0A52..0A64 owner.
; It reserves no source bytes and supplies no DATA values or artificial stack.
SOUND_RESOURCE_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 00a64h)
SOUND_RESOURCE_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, SOUND_RESOURCE_FOREIGN_DATA_TAIL, _BSS
end

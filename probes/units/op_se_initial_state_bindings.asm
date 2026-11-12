; Original code frames and outside DATA prefix only. No values or bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
SE_PLAYBACK_DATA_TEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
SE_PLAYBACK_DATA_TEXT ends
op_01 group SE_PLAYBACK_DATA_TEXT
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 09e2h
_DATA ends
; Preserve the actual already accepted Music Room DATA end at DS:2817.
; This foreign suffix follows the compiler's complete DS:09E2..09E4 owner.
; It reserves no source bytes and supplies no DATA values or artificial stack.
SE_PRIORITY_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 009e4h)
SE_PRIORITY_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, SE_PRIORITY_FOREIGN_DATA_TAIL, _BSS
end

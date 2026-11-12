; True MAIN CODE frames and the real outside DATA prefix only.
; The entire nine-cell writable HUD row must come from native C.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_DECIMAL_SCRATCH_TEXT segment byte public 'CODE' use16
org 09ca0h
HUD_DECIMAL_SCRATCH_TEXT ends
main_01 group HUD_DECIMAL_SCRATCH_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
HUD_DECIMAL_SCRATCH_MAIN03 segment byte public 'CODE' use16
org 0b760h
HUD_DECIMAL_SCRATCH_MAIN03 ends
main_03 group HUD_DECIMAL_SCRATCH_MAIN03
_DATA segment word public 'DATA' use16
org 0142ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

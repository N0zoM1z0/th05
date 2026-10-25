; Actual frames and foreign addresses only; no initialized bytes or assets.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 004e4h
SHARED ends
FOREIGN_TAIL segment byte public 'CODE' use16
org 013aah
FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _bgimage
org 006c2h
_bgimage label word
; End of independently accepted foreign all-cast DATA context.
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

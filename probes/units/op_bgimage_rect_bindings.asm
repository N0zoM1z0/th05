; Actual frames and foreign addresses only; no initialized bytes or assets.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 0083ch
SHARED ends
FOREIGN_TAIL segment byte public 'CODE' use16
org 01422h
FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _bgimage
org 009e4h
_bgimage label word
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

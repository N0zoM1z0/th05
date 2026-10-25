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
org 00458h
SHARED ends
FOREIGN_TAIL segment byte public 'CODE' use16
org 017f4h
FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _cdg_slots
org 03a96h
_cdg_slots label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

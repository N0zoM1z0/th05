; Actual foreign frames/slot address only; no initialized image or state bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00274h
SHARED ends
FOREIGN_TAIL segment byte public 'CODE' use16
org 01636h
FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _cdg_slots
org 029feh
_cdg_slots label byte
; Real foreign pool or independently accepted foreign DATA extent.
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

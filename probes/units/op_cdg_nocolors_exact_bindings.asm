.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 00E14h
SHARED ends
CDG_NCOL_TAIL segment byte public 'CODE' use16
org 00E82h
CDG_NCOL_TAIL ends
_DATA segment word public 'DATA' use16
public _cdg_slots
org 03A96h
_cdg_slots label byte
org 03E96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

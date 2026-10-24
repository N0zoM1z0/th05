; Symbol-only foreign layout. No instructions or state values.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FIREWAVES_FRAME_GAP segment byte public 'CODE' use16
org 0a460h
FIREWAVES_FRAME_GAP ends
BX_UPDATE_TEXT segment byte public 'CODE' use16
org 045cdh
BX_UPDATE_TEXT ends
main_03 group BX_UPDATE_TEXT
FIREWAVES_DS_GAP segment byte public 'CODE' use16
org 07135h
FIREWAVES_DS_GAP ends
_DATA segment word public 'DATA' use16
public _firewaves
org 04a90h
_firewaves label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

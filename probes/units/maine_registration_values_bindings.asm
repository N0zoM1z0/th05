; Complete native far-provider frames; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_PUT, GRAPH_GAIJI_PUTC
org 02b68h
SUPER_PUT label far
org 038e6h
GRAPH_GAIJI_PUTC label far
org 0a540h
_TEXT ends
REG_VALUES_PREFIX segment byte public 'CODE' use16
org (0b730h - 0a540h)
REG_VALUES_PREFIX ends
REG_VALUES_TEXT segment byte public 'CODE' use16
REG_VALUES_TEXT ends
REG_VALUES_TAIL segment byte public 'CODE' use16
org (0e800h - 0ba84h)
REG_VALUES_TAIL ends
GROUP_01 group REG_VALUES_PREFIX, REG_VALUES_TEXT, REG_VALUES_TAIL
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi, _entered_place, _playchar, _resident, _rank
org 01d6eh
_resident label dword
org 04f1ah
_hi label byte
org 05076h
_entered_place label byte
org 05077h
_rank label byte
org 05078h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

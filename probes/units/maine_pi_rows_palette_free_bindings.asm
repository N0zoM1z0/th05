; Real foreign frames/symbols only; no initialized payload or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_PI_FREE
org 013eeh
GRAPH_PI_FREE label far
public PALETTE_SHOW
org 01b8ah
PALETTE_SHOW label far
public GRAPH_PACK_PUT_8_NOCLIP
org 03778h
GRAPH_PACK_PUT_8_NOCLIP label far
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00828h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
org 01056h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _pi_buffers
org 006feh
_pi_buffers label byte
public Palettes
org 01d9ah
Palettes label byte
public _pi_headers
org 027bah
_pi_headers label byte
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real foreign frames/symbols only; no initialized payload or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_PI_FREE
org 012fch
GRAPH_PI_FREE label far
public PALETTE_SHOW
org 019f0h
PALETTE_SHOW label far
public GRAPH_PACK_PUT_8_NOCLIP
org 035b0h
GRAPH_PACK_PUT_8_NOCLIP label far
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00b80h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
org 010ceh
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _pi_buffers
org 00a84h
_pi_buffers label byte
public Palettes
org 02e1eh
Palettes label byte
public _pi_headers
org 03852h
_pi_headers label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

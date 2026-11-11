.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_PI_LOAD_PACK
org 01446h
GRAPH_PI_LOAD_PACK label far
org 0E800h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 00780h
SHARED ends
PI_LOAD_TAIL segment byte public 'CODE' use16
assume cs:PI_LOAD_TAIL
public PI_FREE
org 000D6h
PI_FREE label near
org 0115Eh
PI_LOAD_TAIL ends
PI_LOAD_G group SHARED, PI_LOAD_TAIL
_DATA segment word public 'DATA' use16
public _pi_buffers,_pi_headers
org 006FEh
_pi_buffers label dword
org 027BAh
_pi_headers label byte
org 02F00h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

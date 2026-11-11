.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 00B0Ah
SHARED ends
PI_PLAIN_TAIL segment byte public 'CODE' use16
assume cs:PI_PLAIN_TAIL
public PI_PUT_8_ROWLOOP
org 00047h
PI_PUT_8_ROWLOOP label near
org 011A7h
PI_PLAIN_TAIL ends
PI_PLAIN_G group SHARED, PI_PLAIN_TAIL
_DATA segment word public 'DATA' use16
public _pi_buffers, _pi_headers
org 00A84h
_pi_buffers label dword
org 03852h
_pi_headers label byte
org 03E96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

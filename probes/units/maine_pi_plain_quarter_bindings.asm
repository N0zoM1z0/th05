.386
.model large
_TEXT segment word public 'CODE' use16
org 0E800h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 007E2h
SHARED ends
PI_PLAIN_TAIL segment byte public 'CODE' use16
assume cs:PI_PLAIN_TAIL
public PI_PUT_8_ROWLOOP
org 00000h
PI_PUT_8_ROWLOOP label near
org 010E8h
PI_PLAIN_TAIL ends
PI_PLAIN_G group SHARED, PI_PLAIN_TAIL
_DATA segment word public 'DATA' use16
public _pi_buffers, _pi_headers
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

.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 00994h
SHARED ends
PI_MASK_TAIL segment byte public 'CODE' use16
assume cs:PI_MASK_TAIL
public PI_PUT_MASKED_8_ROWLOOP
org 00001h
PI_PUT_MASKED_8_ROWLOOP label near
org 012D1h
PI_MASK_TAIL ends
PI_MASK_GROUP group SHARED, PI_MASK_TAIL
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

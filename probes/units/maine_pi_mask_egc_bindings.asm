.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public _EGC_ON
org 00824h
_EGC_ON label far
org 0E800h
_TEXT ends
SHARED segment byte public 'CODE' use16
org 0073Fh
SHARED ends
PI_MASK_EGC_TAIL segment byte public 'CODE' use16
org 01190h
PI_MASK_EGC_TAIL ends
_DATA segment word public 'DATA' use16
public _pi_mask_ptr, _pi_mask_y
org 027B4h
_pi_mask_ptr label word
org 027B6h
_pi_mask_y label word
org 04F0Eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0A390h
_TEXT ends
NP_B_PREFIX segment byte public 'CODE' use16
org (0BFF6h - 0A390h)
NP_B_PREFIX ends
NP_B_TEXT segment byte public 'CODE' use16
NP_B_TEXT ends
NP_B_TAIL segment byte public 'CODE' use16
org (0D300h - 0C014h)
NP_B_TAIL ends
op_01 group NP_B_PREFIX, NP_B_TEXT, NP_B_TAIL
SHARED segment para public 'CODE' use16
org (0EFE0h - 0D300h)
SHARED ends
_DATA segment word public 'DATA' use16
public _nopoly_B
org 04EB8h
_nopoly_B label word
org 05060h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

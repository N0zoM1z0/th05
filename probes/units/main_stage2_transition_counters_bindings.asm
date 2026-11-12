; Real MAIN CODE frames and original DGROUP prefix, no candidate state bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
STAGE2_TRANSITION_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
STAGE2_TRANSITION_DATA_TEXT ends
main_01 group STAGE2_TRANSITION_DATA_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
STAGE2_TRANSITION_MAIN03 segment byte public 'CODE' use16
org 0b760h
STAGE2_TRANSITION_MAIN03 ends
main_03 group STAGE2_TRANSITION_MAIN03
_DATA segment word public 'DATA' use16
org 01994h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

; Outside-only context for38 real semantic resource fields/347 initializedbytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
PAUSE_TEXT segment byte public 'CODE' use16
org 09ca0h
PAUSE_TEXT ends
main_01 group PAUSE_TEXT
PAUSE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
PAUSE_SHARED_SPACE ends
PAUSE_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
PAUSE_MAIN03_SPACE ends
main_03 group PAUSE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 020dh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Original main_01 and main_03 segment frames; only outside DATA prefix.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
END_BINARY_NAMES_TEXT segment byte public 'CODE' use16
org 09ca0h
END_BINARY_NAMES_TEXT ends
main_01 group END_BINARY_NAMES_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
END_NAMES_MAIN03 segment byte public 'CODE' use16
org 0b760h
END_NAMES_MAIN03 ends
main_03 group END_NAMES_MAIN03
_DATA segment word public 'DATA' use16
org 0143eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; MAIN CODE and DATA segment frames, no resource filename bytes included.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_FORMAT_NAMES_TEXT segment byte public 'CODE' use16
org 09ca0h
MAIN_FORMAT_NAMES_TEXT ends
main_01 group MAIN_FORMAT_NAMES_TEXT
FMT_NAMES_OUTSIDE segment byte public 'CODE' use16
org 07c0h
FMT_NAMES_OUTSIDE ends
FMT_NAMES_MAIN03 segment byte public 'CODE' use16
org 0b760h
FMT_NAMES_MAIN03 ends
main_03 group FMT_NAMES_MAIN03
_DATA segment word public 'DATA' use16
org 018c0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

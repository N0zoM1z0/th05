; Original MAIN frames, only prior DATA outside the candidate.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BB_CHEETO_FILENAME_TEXT segment byte public 'CODE' use16
org 09ca0h
BB_CHEETO_FILENAME_TEXT ends
main_01 group BB_CHEETO_FILENAME_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BB_CHEETO_FILENAME_MAIN03 segment byte public 'CODE' use16
org 0b760h
BB_CHEETO_FILENAME_MAIN03 ends
main_03 group BB_CHEETO_FILENAME_MAIN03
_DATA segment word public 'DATA' use16
org 0169bh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

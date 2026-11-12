; Genuine MAIN CODE frames and only the outside original DATA prefix.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
EYECATCH_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
EYECATCH_DATA_TEXT ends
main_01 group EYECATCH_DATA_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
EYECATCH_MAIN03 segment byte public 'CODE' use16
org 0b760h
EYECATCH_MAIN03 ends
main_03 group EYECATCH_MAIN03
_DATA segment word public 'DATA' use16
org 000aah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

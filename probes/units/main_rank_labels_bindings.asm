; Original MAIN external segment frame and preexisting DATA only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
RANK_LABELS_TEXT segment byte public 'CODE' use16
org 09ca0h
RANK_LABELS_TEXT ends
main_01 group RANK_LABELS_TEXT
RANK_LABELS_OUTSIDE segment byte public 'CODE' use16
org 07c0h
RANK_LABELS_OUTSIDE ends
RANK_LABELS_MAIN03 segment byte public 'CODE' use16
org 0b760h
RANK_LABELS_MAIN03 ends
main_03 group RANK_LABELS_MAIN03
_DATA segment word public 'DATA' use16
org 01374h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

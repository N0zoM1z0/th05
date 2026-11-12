; Preserve the original MAIN large-model frames and the preceding DATA bank.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
STAT_LABELS_TEXT segment byte public 'CODE' use16
org 09ca0h
STAT_LABELS_TEXT ends
main_01 group STAT_LABELS_TEXT
STAT_LABELS_OUTSIDE segment byte public 'CODE' use16
org 07c0h
STAT_LABELS_OUTSIDE ends
STAT_LABELS_MAIN03 segment byte public 'CODE' use16
org 0b760h
STAT_LABELS_MAIN03 ends
main_03 group STAT_LABELS_MAIN03
_DATA segment word public 'DATA' use16
org 0139ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

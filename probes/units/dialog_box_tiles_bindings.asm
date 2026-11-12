; Original MAIN code frames and only the DATA prefix outside the candidate.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
DIALOG_TILE_MASKS_TEXT segment byte public 'CODE' use16
org 09ca0h
DIALOG_TILE_MASKS_TEXT ends
main_01 group DIALOG_TILE_MASKS_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
DIALOG_TILE_MASKS_MAIN03 segment byte public 'CODE' use16
org 0b760h
DIALOG_TILE_MASKS_MAIN03 ends
main_03 group DIALOG_TILE_MASKS_MAIN03
_DATA segment word public 'DATA' use16
org 01ed0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

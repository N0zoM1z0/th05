; Native MAIN DATA prefix; the complete table is supplied only by C.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_SECTION_MAIN01_GAP segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
TILE_SECTION_MAIN01_GAP ends
TILE_SECTION_SHARED_GAP segment byte public 'CODE' use16
org (0209d0h - 014ab0h)
TILE_SECTION_SHARED_GAP ends
_DATA segment word public 'DATA' use16
org 00f0ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

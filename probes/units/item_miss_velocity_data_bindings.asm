; Outside-only frames; source owns the complete60-byte typed miss velocity table.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
ITEM_MISS_DATA_CONTEXT segment byte public 'CODE' use16
org 09ca0h
ITEM_MISS_DATA_CONTEXT ends
main_01 group HUD_OVRL_TEXT, ITEM_MISS_DATA_CONTEXT
ITEM_MISS_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
ITEM_MISS_SHARED_SPACE ends
ITEM_MISS_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
ITEM_MISS_MAIN03_SPACE ends
main_03 group ITEM_MISS_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 01e86h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

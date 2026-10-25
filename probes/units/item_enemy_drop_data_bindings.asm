; Outside-only frames; source owns the complete64-byte automatic drop schedule.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
ITEM_DROP_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
ITEM_DROP_DATA_TEXT ends
main_01 group HUD_OVRL_TEXT, ITEM_DROP_DATA_TEXT
ITEM_DROP_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
ITEM_DROP_SHARED_SPACE ends
ITEM_DROP_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
ITEM_DROP_MAIN03_SPACE ends
main_03 group ITEM_DROP_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 01dc2h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

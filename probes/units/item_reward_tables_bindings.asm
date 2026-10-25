; Outside-only segment context for semantic item DATA. No owned values/bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
ITEM_UPDATE_MAIN01 segment byte public 'CODE' use16
ITEM_UPDATE_MAIN01 ends
ITEM_TABLE_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
ITEM_TABLE_MAIN01_SPACE ends
main_01 group HUD_OVRL_TEXT, ITEM_UPDATE_MAIN01, ITEM_TABLE_MAIN01_SPACE
ITEM_TABLE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
ITEM_TABLE_SHARED_SPACE ends
ITEM_REWARD_TABLE_CONTEXT segment byte public 'CODE' use16
ITEM_REWARD_TABLE_CONTEXT ends
ITEM_EXTEND_TEXT segment byte public 'CODE' use16
ITEM_EXTEND_TEXT ends
ITEM_REWARD_TEXT segment byte public 'CODE' use16
ITEM_REWARD_TEXT ends
ITEM_UPDATE_TEXT segment byte public 'CODE' use16
ITEM_UPDATE_TEXT ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
ITEM_SPLASH_TEXT ends
ITEM_TABLE_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
ITEM_TABLE_MAIN03_SPACE ends
main_03 group ITEM_REWARD_TABLE_CONTEXT, ITEM_EXTEND_TEXT, ITEM_REWARD_TEXT, ITEM_UPDATE_TEXT, ITEM_SPLASH_TEXT, ITEM_TABLE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 01e04h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

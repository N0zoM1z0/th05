; Complete initializer: foreign addresses only, no values or instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
ITEM_INIT_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
ITEM_INIT_MAIN01_GAP ends
main_01 group HUD_OVRL_TEXT, ITEM_INIT_MAIN01_GAP
ITEM_INIT_SHARED_GAP segment byte public 'CODE' use16
org 07c0h
ITEM_INIT_SHARED_GAP ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
ITEM_SPLASH_TEXT ends
ITEM_SPLASH_INIT_TEXT segment byte public 'CODE' use16
org (16362h - 15270h)
ITEM_SPLASH_INIT_TEXT ends
main_03 group ITEM_SPLASH_TEXT, ITEM_SPLASH_INIT_TEXT
ITEM_INIT_DATA_GAP segment byte public 'CODE' use16
org (209d0h - 1637ch)
ITEM_INIT_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _item_splashes, _item_splash_last_id
org 0372ch
_item_splashes label byte
org 03786h
_item_splash_last_id label byte
org 03787h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
SHARED segment para public 'CODE' use16
org (015270h - 0AE10h)
SHARED ends
ITEM_SPLASH_INIT_PREFIX segment byte public 'CODE' use16
org (016362h - 015270h)
ITEM_SPLASH_INIT_PREFIX ends
ITEM_SPLASH_INIT_TEXT segment byte public 'CODE' use16
ITEM_SPLASH_INIT_TEXT ends
ITEM_SPLASH_INIT_TAIL segment byte public 'CODE' use16
org (0209D0h - 01637Ch)
ITEM_SPLASH_INIT_TAIL ends
main_03 group ITEM_SPLASH_INIT_PREFIX, ITEM_SPLASH_INIT_TEXT, ITEM_SPLASH_INIT_TAIL
_DATA segment word public 'DATA' use16
public _item_splashes, _item_splash_last_id
org 0372Ch
_item_splashes label byte
org 03786h
_item_splash_last_id label byte
org 0A000h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

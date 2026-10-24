; Original address-only context; no bodies/data values/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
HUD_OVRL_TEXT ends
ITEM_FOREIGN_MAIN01 segment byte public 'CODE' use16
assume cs:ITEM_FOREIGN_MAIN01
org 09ca0h
ITEM_FOREIGN_MAIN01 ends
main_01 group HUD_OVRL_TEXT, ITEM_FOREIGN_MAIN01
ITEM_FOREIGN_SHARED segment para public 'CODE' use16
assume cs:ITEM_FOREIGN_SHARED
org 07c0h
ITEM_FOREIGN_SHARED ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
assume cs:ITEM_SPLASH_TEXT
org 0110ch
ITEM_SPLASH_TEXT ends
ITEM_SPLASH_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ITEM_SPLASH_MAIN03_TAIL
org 0a5d2h
ITEM_SPLASH_MAIN03_TAIL ends
main_03 group ITEM_SPLASH_TEXT, ITEM_SPLASH_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _item_splashes
org 0372ch
_item_splashes label byte
public _item_splash_last_id
org 03786h
_item_splash_last_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

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
ITEM_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:ITEM_INVALIDATE_TEXT
public TILES_INVALIDATE_AROUND
org 0cc2h
TILES_INVALIDATE_AROUND label near
org 0139ch
ITEM_INVALIDATE_TEXT ends
ITEM_INVALIDATE_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:ITEM_INVALIDATE_MAIN01_TAIL
org 088b9h
ITEM_INVALIDATE_MAIN01_TAIL ends
main_01 group HUD_OVRL_TEXT, ITEM_INVALIDATE_TEXT, ITEM_INVALIDATE_MAIN01_TAIL
ITEM_FOREIGN_SHARED segment para public 'CODE' use16
assume cs:ITEM_FOREIGN_SHARED
org 07c0h
ITEM_FOREIGN_SHARED ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
assume cs:ITEM_SPLASH_TEXT
ITEM_SPLASH_TEXT ends
ITEM_INVALIDATE_MAIN03_SPACE segment byte public 'CODE' use16
assume cs:ITEM_INVALIDATE_MAIN03_SPACE
org 0b760h
ITEM_INVALIDATE_MAIN03_SPACE ends
main_03 group ITEM_SPLASH_TEXT, ITEM_INVALIDATE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _tile_invalidate_box
org 03502h
_tile_invalidate_box label byte
public _item_splashes
org 0372ch
_item_splashes label byte
public _items
org 0b084h
_items label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Actual foreign endpoints only; no code bytes, images, stack or entry.
.386
ifdef BINDINGS_AFTER
ITEM_RENDER_TEXT segment byte public 'CODE' use16
assume cs:ITEM_RENDER_TEXT
ITEM_RENDER_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
main_01 group HUD_OVRL_TEXT, ITEM_RENDER_TEXT
else
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
ITEM_RENDER_TEXT segment byte public 'CODE' use16
assume cs:ITEM_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW
org (0c07ch - 0ae10h)
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
public ITEM_SPLASHES_RENDER
org (0dca7h - 0ae10h)
ITEM_SPLASHES_RENDER label near
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - 0ae10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (138e4h - 0ae10h)
ITEM_RENDER_TEXT ends
main_01 group HUD_OVRL_TEXT, ITEM_RENDER_TEXT
ITEM_RENDER_SHARED_GAP segment byte public 'CODE' use16
org (14ab0h - 1392bh)
ITEM_RENDER_SHARED_GAP ends
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
ITEM_SPLASH_TEXT ends
main_03 group ITEM_SPLASH_TEXT
ITEM_RENDER_DATA_GAP segment byte public 'CODE' use16
org (209d0h - 15270h)
ITEM_RENDER_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _drawpoint, _item_splashes, _items
org 036feh
_drawpoint label byte
org 0372ch
_item_splashes label byte
org 0b084h
_items label byte
org 0b3a4h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
endif
end

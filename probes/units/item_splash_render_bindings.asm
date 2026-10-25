; Actual foreign endpoints only; no code bytes, images, stack or entry.
.386
ifdef BINDINGS_AFTER
ITEM_RENDER_TEXT segment byte public 'CODE' use16
assume cs:ITEM_RENDER_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - 0dd2ah)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
public @item_splash_dot_render
org (0e152h - 0dd2ah)
@item_splash_dot_render label near
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
public @grcg_setcolor_direct_raw$qv
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (0dca7h - 0ae10h)
ITEM_RENDER_TEXT ends
main_01 group HUD_OVRL_TEXT, ITEM_RENDER_TEXT
ITEM_RENDER_SHARED_GAP segment byte public 'CODE' use16
org (14ab0h - 0e152h)
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

; Real MAIN01/SHARED/MAIN03 frames and foreign tile/scroll state only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_INV_ORIGINAL_PREFIX segment byte public 'CODE' use16
org (0bad2h - 0ae10h)
TILE_INV_ORIGINAL_PREFIX ends
TILE_INVALIDATE_AROUND_TEXT segment byte public 'CODE' use16
TILE_INVALIDATE_AROUND_TEXT ends
TILE_INV_ORIGINAL_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bb9eh)
TILE_INV_ORIGINAL_TAIL ends
main_01 group TILE_INV_ORIGINAL_PREFIX, TILE_INVALIDATE_AROUND_TEXT, TILE_INV_ORIGINAL_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
TILE_INV_MAIN03_CONTEXT segment byte public 'CODE' use16
org (0209d0h - 015270h)
TILE_INV_MAIN03_CONTEXT ends
main_03 group TILE_INV_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _invalidate_left_x_tile, _scroll_line_on_page
public _tile_invalidate_box, _page_back
public _halftiles_dirty, _halftiles_dirty_end
org 034f4h
_invalidate_left_x_tile label word
org 034feh
_scroll_line_on_page label word
org 03502h
_tile_invalidate_box label byte
org 04ad6h
_page_back label byte
org 04adah
_halftiles_dirty label byte
org 0511ah
_halftiles_dirty_end label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

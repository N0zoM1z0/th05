; Whole tile-ring setter, true CS AE1/DS209D frames and foreign positions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCROLL_RSET_TEXT segment byte public 'CODE' use16
assume cs:SCROLL_RSET_TEXT
org (0bea4h - 0ae10h)
SCROLL_RSET_TEXT ends
SCROLL_RSET_TAIL segment byte public 'CODE' use16
assume cs:SCROLL_RSET_TAIL
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - 0bef3h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (014ab0h - 0bef3h)
SCROLL_RSET_TAIL ends
main_01 group SCROLL_RSET_TEXT, SCROLL_RSET_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _scroll_active, _tile_ring
org 0351ah
_scroll_active label byte
org 0511ah
_tile_ring label word
org 0575ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

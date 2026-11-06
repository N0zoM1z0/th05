; Native frames and foreign labels only; no initialized payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_OFF
org 0085eh
EGC_OFF label far
org 0ae10h
_TEXT ends
TILE_REDRAW_TEXT segment word public 'CODE' use16
assume cs:main_01
public @egc_start_copy_noframe$qv
org (0bc2eh - 0ae10h)
@egc_start_copy_noframe$qv label near
org (0bdaeh - 0ae10h)
TILE_REDRAW_TEXT ends
FOREIGN_TILE_REDRAW_TAIL segment byte public 'CODE' use16
org (014ab0h - 0be1ah)
FOREIGN_TILE_REDRAW_TAIL ends
main_01 group TILE_REDRAW_TEXT, FOREIGN_TILE_REDRAW_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_TILE_REDRAW_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_TILE_REDRAW_MAIN03 ends
main_03 group FOREIGN_TILE_REDRAW_MAIN03
_DATA segment word public 'DATA' use16
public _halftiles_dirty, _tile_ring
org 04adah
_halftiles_dirty label byte
org 0511ah
_tile_ring label word
org 0575ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Native frames and foreign objects only; no initialized payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_FILL_TEXT segment word public 'CODE' use16
org (0bb9eh - 0ae10h)
TILE_FILL_TEXT ends
FOREIGN_TILE_FILL_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bbech)
FOREIGN_TILE_FILL_TAIL ends
main_01 group TILE_FILL_TEXT, FOREIGN_TILE_FILL_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_TILE_FILL_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_TILE_FILL_MAIN03 ends
main_03 group FOREIGN_TILE_FILL_MAIN03
_DATA segment word public 'DATA' use16
public _TILE_SECTION_OFFSETS, _std_seg, _map_seg, _tile_ring, _std_map_section_p
org 00f0ah
_TILE_SECTION_OFFSETS label word
org 00f4ah
org 00f52h
_std_seg label word
org 00f54h
org 04ad8h
_map_seg label word
org 04adah
org 0511ah
_tile_ring label word
org 0575ah
_std_map_section_p label word
org 0575ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

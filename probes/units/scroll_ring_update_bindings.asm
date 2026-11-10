ifdef BINDINGS_AFTER
; Authentic two-phase source-only scroll ring context.
.386
.model large
SCROLL_RING_CONTEXT segment byte public 'CODE' use16
SCROLL_RING_CONTEXT ends
SCROLL_RING_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c506h)
SCROLL_RING_TAIL ends
main_01 group SCROLL_RING_CONTEXT, SCROLL_RING_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
MAIN03_FOREIGN segment byte public 'CODE' use16
org (0209d0h - 015270h)
MAIN03_FOREIGN ends
main_03 group MAIN03_FOREIGN
_DATA segment word public 'DATA' use16
public _std_seg, _TILE_SECTION_OFFSETS, _scroll_tile_row, _scroll_row_advance_current, _scroll_row_advance_previous
public _scroll_active, _scroll_line, _scroll_speed, _map_seg, _tile_ring, _tile_row_in_section
public _std_map_section_p, _std_scroll_speed, _stage_id
org 00f0ah
_TILE_SECTION_OFFSETS label word
org 00f52h
_std_seg label word
org 034f6h
_scroll_row_advance_current label byte
org 03510h
_scroll_row_advance_previous label byte
org 03512h
_scroll_tile_row label word
org 03515h
_scroll_speed label byte
org 03516h
_scroll_line label word
org 0351ah
_scroll_active label byte
org 04ad8h
_map_seg label word
org 0511ah
_tile_ring label word
org 0575ah
_std_map_section_p label word
org 0575ch
_tile_row_in_section label byte
org 0575eh
_std_scroll_speed label word
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end
else
; Authentic two-phase source-only scroll ring context.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_OFF
org 0085eh
EGC_OFF label far
org 0ae10h
_TEXT ends
SCROLL_RING_CONTEXT segment byte public 'CODE' use16
assume cs:SCROLL_RING_CONTEXT
public @egc_start_copy_noframe$qv, _tiles_copy_scroll_strip
org (0bc2eh - 0ae10h)
@egc_start_copy_noframe$qv label near
org (0bc6eh - 0ae10h)
_tiles_copy_scroll_strip label near
org (0c43ah - 0ae10h)
SCROLL_RING_CONTEXT ends
main_01 group SCROLL_RING_CONTEXT
end
endif

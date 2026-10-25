; Real outside CODE/state contexts only; no instruction bodies or owned DATA.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_SCROLLUP
org 01ee2h
GRAPH_SCROLLUP label far
org 0ae10h
_TEXT ends
SCROLL_RING_CONTEXT segment byte public 'CODE' use16
assume cs:SCROLL_RING_CONTEXT
public @scroll_tile_ring_update$qv
org (0c43ah - 0ae10h)
@scroll_tile_ring_update$qv label near
org (0c506h - 0ae10h)
SCROLL_RING_CONTEXT ends
SCROLL_DRIVER_TEXT segment byte public 'CODE' use16
SCROLL_DRIVER_TEXT ends
SCROLL_DRIVER_TAIL segment byte public 'CODE' use16
org (14ab0h - 0c579h)
SCROLL_DRIVER_TAIL ends
main_01 group SCROLL_RING_CONTEXT, SCROLL_DRIVER_TEXT, SCROLL_DRIVER_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _scroll_row_advance_current
org 034f6h
_scroll_row_advance_current label byte
public _scroll_line_on_page
org 034feh
_scroll_line_on_page label word
public _scroll_row_advance_previous
org 03510h
_scroll_row_advance_previous label byte
public _scroll_subpixel_line, _scroll_speed
org 03514h
_scroll_subpixel_line label byte
org 03515h
_scroll_speed label byte
public _scroll_line, _scroll_last_delta, _scroll_active
org 03516h
_scroll_line label word
org 03518h
_scroll_last_delta label word
org 0351ah
_scroll_active label byte
public _page_back
org 04ad6h
_page_back label byte
public _stage_id
org 0576eh
_stage_id label byte
org 0576fh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

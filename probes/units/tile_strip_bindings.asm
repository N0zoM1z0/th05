; Native frames and foreign labels only; no initialized payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
TILE_STRIP_TEXT segment word public 'CODE' use16
org (0bc6eh - 0ae10h)
TILE_STRIP_TEXT ends
FOREIGN_TILE_STRIP_TAIL segment byte public 'CODE' use16
org (014ab0h - 0bd24h)
FOREIGN_TILE_STRIP_TAIL ends
main_01 group TILE_STRIP_TEXT, FOREIGN_TILE_STRIP_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_TILE_STRIP_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_TILE_STRIP_MAIN03 ends
main_03 group FOREIGN_TILE_STRIP_MAIN03
_DATA segment word public 'DATA' use16
public _tile_strip_height, _tile_strip_source_skip
public _tile_strip_destination, _tile_strip_first_rows
public _scroll_line, _tile_ring
org 034f6h
_tile_strip_height label byte
org 034f7h
_tile_strip_source_skip label word
org 034f9h
_tile_strip_destination label word
org 034fbh
_tile_strip_first_rows label word
org 03516h
_scroll_line label word
org 0511ah
_tile_ring label word
org 0575ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

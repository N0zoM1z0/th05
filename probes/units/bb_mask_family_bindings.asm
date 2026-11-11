; Relocation-accurate foreign function contexts and original DS globals.
; Source owns no additional code, data values, graphics assets or CRT.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_SETCOLOR
org 01a88h
GRCG_SETCOLOR label far
org 0ae10h
_TEXT ends
TILE_BB_MASK_PREFIX segment byte public 'CODE' use16
assume cs:TILE_BB_MASK_PREFIX
public tiles_invalidate_around
org (0bad2h - 0ae10h)
tiles_invalidate_around label near
org (0f968h - 0ae10h)
TILE_BB_MASK_PREFIX ends
TILE_BB_MASK_TEXT segment byte public 'CODE' use16
TILE_BB_MASK_TEXT ends
TILE_BB_MASK_TAIL segment byte public 'CODE' use16
assume cs:TILE_BB_MASK_TAIL
public grcg_tile_bb_put_8
org (01045ch - 0fa50h)
grcg_tile_bb_put_8 label near
org (014ab0h - 0fa50h)
TILE_BB_MASK_TAIL ends
main_01 group TILE_BB_MASK_PREFIX, TILE_BB_MASK_TEXT, TILE_BB_MASK_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _scroll_line, _scroll_active
public _tiles_bb_col, _tiles_bb_seg, _bb_boss_seg
org 03502h
_tile_invalidate_box label dword
org 03516h
_scroll_line label word
org 0351ah
_scroll_active label byte
org 04444h
_tiles_bb_col label byte
org 04448h
_tiles_bb_seg label word
org 0c692h
_bb_boss_seg label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

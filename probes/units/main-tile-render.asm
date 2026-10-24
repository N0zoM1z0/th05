; Original-address symbols only for main-tile-render. No bodies, values or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h
UNIT_START equ 0bd4eh
UNIT_SIZE equ 05fh
UNIT_END equ (UNIT_START + UNIT_SIZE)
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
SMALL_MAIN01_CONTEXT segment byte public 'CODE' use16
SMALL_MAIN01_CONTEXT ends
TILE_TEXT segment byte public 'CODE' use16
assume cs:TILE_TEXT
public @TILES_RENDER_ALL$QV
org (0bbech - MAIN01_BASE)
@TILES_RENDER_ALL$QV label near
org (UNIT_START - MAIN01_BASE)
TILE_TEXT ends
SMALL_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:SMALL_MAIN01_TAIL
public @TILES_REDRAW_INVALIDATED$QV
org (0bdaeh - UNIT_END)
@TILES_REDRAW_INVALIDATED$QV label near
public @enemies_invalidate$qv
org (0c180h - UNIT_END)
@enemies_invalidate$qv label near
public @items_invalidate$qv
org (0c1ach - UNIT_END)
@items_invalidate$qv label near
public @player_invalidate$qv
org (0c9bah - UNIT_END)
@player_invalidate$qv label near
public @sparks_invalidate$qv
org (0e10eh - UNIT_END)
@sparks_invalidate$qv label near
public @pointnums_invalidate$qv
org (0e17ah - UNIT_END)
@pointnums_invalidate$qv label near
public @bullets_and_gather_invalidate$qv
org (0e40eh - UNIT_END)
@bullets_and_gather_invalidate$qv label near
public @overlay_titles_invalidate$qv
org (011ee4h - UNIT_END)
@overlay_titles_invalidate$qv label near
public @shots_invalidate$qv
org (01337dh - UNIT_END)
@shots_invalidate$qv label near
org (SHARED_BASE - UNIT_END)
SMALL_MAIN01_TAIL ends
main_01 group SMALL_MAIN01_CONTEXT, TILE_TEXT, SMALL_MAIN01_TAIL
SMALL_SHARED_SPACE segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SMALL_SHARED_SPACE ends
SMALL_MAIN03_SPACE segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
SMALL_MAIN03_SPACE ends
main_03 group SMALL_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _bg_render_not_bombing
org 03506h
_bg_render_not_bombing label word
public _tile_render_all_time
org 0350eh
_tile_render_all_time label byte
public _stage_invalidate
org 04a86h
_stage_invalidate label word
public _midboss_invalidate
org 0c4ach
_midboss_invalidate label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

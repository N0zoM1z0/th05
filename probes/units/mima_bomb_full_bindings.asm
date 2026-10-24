; Original outside-only context for the complete adjacent Mima draw/control.
; No helper body, callback contents, assets, stack or owned filler.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLE
org 010aeh
GRCG_CIRCLE label far
public GRCG_SETCOLOR
org 01a88h
GRCG_SETCOLOR label far
public GRCG_VLINE
org 01ab8h
GRCG_VLINE label far
public GRAPH_SCROLLUP
org 01ee2h
GRAPH_SCROLLUP label far
org 0ae10h
_TEXT ends
MIMA_CIRCLES_TEXT segment byte public 'CODE' use16
MIMA_CIRCLES_TEXT ends
MIMA_BOMB_TEXT segment byte public 'CODE' use16
assume cs:MIMA_BOMB_TEXT
public @grcg_setcolor_direct_raw$qv
org 013f4h
@grcg_setcolor_direct_raw$qv label near
public NULLFUNC_NEAR
org 0192eh
NULLFUNC_NEAR label near
public @bomb_dream_decay$qv
org 04cfah
@bomb_dream_decay$qv label near
public @mima_circles_update_and_render$qv
org 05248h
@mima_circles_update_and_render$qv label near
org 052fdh
MIMA_BOMB_TEXT ends
MIMA_BOMB_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:MIMA_BOMB_FOREIGN_TEXT
public @mima_bomb_backdrop_render$qv
org 02b1h
@mima_bomb_backdrop_render$qv label near
org 04835h
MIMA_BOMB_FOREIGN_TEXT ends
main_01 group MIMA_CIRCLES_TEXT, MIMA_BOMB_TEXT, MIMA_BOMB_FOREIGN_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8
org 01c0h
CDG_PUT_NOALPHA_8 label far
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 0bf20h
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone
org 03dah
_PaletteTone label word
public _items_pull_to_player
org 01e84h
_items_pull_to_player label byte
public _bg_render_bombing
org 03508h
_bg_render_bombing label word
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _scroll_line
org 03516h
_scroll_line label word
public _scroll_active
org 0351ah
_scroll_active label byte
public _bombing
org 04206h
_bombing label byte
public _bomb_frame
org 04207h
_bomb_frame label byte
public _palette_changed
org 0576dh
_palette_changed label byte
public _stage_id
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

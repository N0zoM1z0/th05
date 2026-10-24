; Foreign symbol addresses only, outside the complete161-byte callback.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_SCROLLUP
org 01ee2h
GRAPH_SCROLLUP label far
org 0ae10h
_TEXT ends
YUUKA_BOMB_TEXT segment byte public 'CODE' use16
assume cs:YUUKA_BOMB_TEXT
public BB_PLAYCHAR_PUT, NULLFUNC_NEAR, @yuuka_bomb_draw$qv, @bomb_dream_decay$qv
org (0c73eh - 0ae10h)
NULLFUNC_NEAR label near
org (0faf7h - 0ae10h)
BB_PLAYCHAR_PUT label near
org (0fb0ah - 0ae10h)
@bomb_dream_decay$qv label near
org (102f9h - 0ae10h)
@yuuka_bomb_draw$qv label near
org (10371h - 0ae10h)
YUUKA_BOMB_TEXT ends
YUUKA_BOMB_TAIL segment byte public 'CODE' use16
org (14ab0h - 10432h)
YUUKA_BOMB_TAIL ends
MARISA_BOMB_TEXT segment byte public 'CODE' use16
MARISA_BOMB_TEXT ends
main_01 group MARISA_BOMB_TEXT, YUUKA_BOMB_TEXT, YUUKA_BOMB_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _items_pull_to_player, _bg_render_bombing
public _bg_render_bombing_func, _scroll_line, _scroll_active
public _tiles_bb_col
public _bombing, _bomb_frame, _palette_changed, _stage_id
org 03dah
_PaletteTone label word
org 01e84h
_items_pull_to_player label byte
org 03508h
_bg_render_bombing label word
org 0350ah
_bg_render_bombing_func label word
org 03516h
_scroll_line label word
org 0351ah
_scroll_active label byte
org 04206h
_bombing label byte
org 04207h
_bomb_frame label byte
org 04444h
_tiles_bb_col label byte
org 0576dh
_palette_changed label byte
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

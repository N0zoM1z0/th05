; Real full bomb-family context. Foreign addresses/extents only.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BOXFILL
org 0ea6h
GRCG_BOXFILL label far
public GRCG_CIRCLEFILL
org 0100eh
GRCG_CIRCLEFILL label far
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
public PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
public SUPER_ROLL_PUT_1PLANE
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 0ae10h
_TEXT ends
MIMA_CIRCLES_TEXT segment byte public 'CODE' use16
assume cs:MIMA_CIRCLES_TEXT
MIMA_CIRCLES_TEXT ends
MIMA_BOMB_TEXT segment byte public 'CODE' use16
assume cs:MIMA_BOMB_TEXT
MIMA_BOMB_TEXT ends
MIMA_BOMB_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:MIMA_BOMB_FOREIGN_TEXT
MIMA_BOMB_FOREIGN_TEXT ends
BOMB_RUNTIME_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:BOMB_RUNTIME_FOREIGN_TEXT
BOMB_RUNTIME_FOREIGN_TEXT ends
MARISA_BOMB_TEXT segment byte public 'CODE' use16
assume cs:MARISA_BOMB_TEXT
MARISA_BOMB_TEXT ends
BOMB_FAMILY_TEXT segment byte public 'CODE' use16
assume cs:BOMB_FAMILY_TEXT
public @grcg_setmode_rmw$qv
org 013e8h
@grcg_setmode_rmw$qv label near
public @grcg_setcolor_direct_raw$qv
org 013f4h
@grcg_setcolor_direct_raw$qv label near
public @randring1_next16$qv
org 018f0h
@randring1_next16$qv label near
public @RANDRING1_NEXT16_AND$QUI
org 018feh
@RANDRING1_NEXT16_AND$QUI label near
public @RANDRING1_NEXT16_MOD$QUI
org 01914h
@RANDRING1_NEXT16_MOD$QUI label near
public NULLFUNC_NEAR
org 0192eh
NULLFUNC_NEAR label near
public PLAYPERF_LOWER
org 02184h
PLAYPERF_LOWER label far
public @SELECT_FOR_PLAYCHAR$QIIII
org 0219ch
@SELECT_FOR_PLAYCHAR$QIIII label far
public @hud_bombs_put$qv
org 022d9h
@hud_bombs_put$qv label far
public HUD_DREAM_PUT
org 023bdh
HUD_DREAM_PUT label far
public @CIRCLES_ADD_GROWING$QII
org 0347ah
@CIRCLES_ADD_GROWING$QII label far
public @TILES_BB_PUT_RAW$QI
org 04b58h
@TILES_BB_PUT_RAW$QI label near
org 04c40h
BOMB_FAMILY_TEXT ends
BOMB_FAMILY_TAIL segment byte public 'CODE' use16
assume cs:BOMB_FAMILY_TAIL
public @reimu_bomb_backdrop_render$qv
org 0223h
@reimu_bomb_backdrop_render$qv label near
public @marisa_bomb_backdrop_render$qv
org 0253h
@marisa_bomb_backdrop_render$qv label near
public @mima_bomb_backdrop_render$qv
org 02b1h
@mima_bomb_backdrop_render$qv label near
org 04835h
BOMB_FAMILY_TAIL ends
main_01 group MIMA_CIRCLES_TEXT, MIMA_BOMB_TEXT, MIMA_BOMB_FOREIGN_TEXT, BOMB_RUNTIME_FOREIGN_TEXT, MARISA_BOMB_TEXT, BOMB_FAMILY_TEXT, BOMB_FAMILY_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public VECTOR2
org 08h
VECTOR2 label far
public CDG_PUT_NOALPHA_8
org 01c0h
CDG_PUT_NOALPHA_8 label far
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
MAIN_BOMB_SPARKS segment byte public 'CODE' use16
assume cs:MAIN_BOMB_SPARKS
public @bomb_sparks_add_at_player$qv
org 02448h
@bomb_sparks_add_at_player$qv label far
org 0b760h
MAIN_BOMB_SPARKS ends
main_03 group MAIN_BOMB_SPARKS
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
public _player_pos
org 036d2h
_player_pos label byte
public _player_invincibility_time
org 036eeh
_player_invincibility_time label byte
public _player_respawn_motion_time
org 036efh
_player_respawn_motion_time label byte
public _shot_time
org 036f2h
_shot_time label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
public _miss_time
org 036f4h
_miss_time label byte
public _dream
org 036f6h
_dream label byte
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _circles_color
org 041dah
_circles_color label byte
public _resident
org 041fch
_resident label dword
public _bombing
org 04206h
_bombing label byte
public _bomb_frame
org 04207h
_bomb_frame label byte
public _bb_playchar_seg
org 0420ah
_bb_playchar_seg label word
public _bomb_anim
org 0420eh
_bomb_anim label byte
public _tiles_bb_col
org 04444h
_tiles_bb_col label byte
public _tiles_bb_seg
org 04448h
_tiles_bb_seg label word
public _bombs
org 04ad5h
_bombs label byte
public _stage_frame_mod4
org 05767h
_stage_frame_mod4 label byte
public _stage_frame_mod8
org 05768h
_stage_frame_mod8 label byte
public _palette_changed
org 0576dh
_palette_changed label byte
public _stage_id
org 0576eh
_stage_id label byte
public _boss
org 05abah
_boss label byte
public _bombing_disabled
org 0c4bah
_bombing_disabled label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Actual outside-only providers/globals; no owned call or NOP supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BOMB_RUNTIME_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:BOMB_RUNTIME_FOREIGN_TEXT
public NULLFUNC_NEAR
org (0c73eh - 0ae10h)
NULLFUNC_NEAR label near
public PLAYPERF_LOWER
org (0cf94h - 0ae10h)
PLAYPERF_LOWER label far
public @SELECT_FOR_PLAYCHAR$QIIII
org (0cfach - 0ae10h)
@SELECT_FOR_PLAYCHAR$QIIII label far
public @hud_bombs_put$qv
org (0d0e9h - 0ae10h)
@hud_bombs_put$qv label far
public HUD_DREAM_PUT
org (0d1cdh - 0ae10h)
HUD_DREAM_PUT label far
public @TILES_BB_PUT_RAW$QI
org (0f968h - 0ae10h)
@TILES_BB_PUT_RAW$QI label near
org (0fa50h - 0ae10h)
BOMB_RUNTIME_FOREIGN_TEXT ends
BOMB_RUNTIME_TEXT segment byte public 'CODE' use16
BOMB_RUNTIME_TEXT ends
BOMB_RUNTIME_TAIL segment byte public 'CODE' use16
org (014ab0h - 0fb44h)
BOMB_RUNTIME_TAIL ends
main_01 group BOMB_RUNTIME_FOREIGN_TEXT, BOMB_RUNTIME_TEXT, BOMB_RUNTIME_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
BOMB_RUNTIME_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
BOMB_RUNTIME_MAIN03_SPACE ends
main_03 group BOMB_RUNTIME_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _items_pull_to_player
org 01e84h
_items_pull_to_player label byte
public _bg_render_bombing
org 03508h
_bg_render_bombing label word
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _player_invincibility_time
org 036eeh
_player_invincibility_time label byte
public _player_respawn_motion_time
org 036efh
_player_respawn_motion_time label byte
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
public _tiles_bb_seg
org 04448h
_tiles_bb_seg label word
public _bombs
org 04ad5h
_bombs label byte
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

; Whole real player-update281, no foreign bodies, values, stack or source gaps.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
PLAYER_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_UPDATE_TEXT
public @PlayfieldMotion@update_seg1$qv, @PLAYER_MOVE$QUI
public @player_pos_update_and_clamp$qv, @player_miss_update$qv
org 0100ah
@PlayfieldMotion@update_seg1$qv label near
org 01c3ch
@PLAYER_MOVE$QUI label near
org 01cc2h
@player_pos_update_and_clamp$qv label near
org 01cfah
@player_miss_update$qv label near
org 01e2dh
PLAYER_UPDATE_TEXT ends
PLAYER_UPDATE_AFTER_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_UPDATE_AFTER_TEXT
public PLAYER_BOMB
org 02d0ah
PLAYER_BOMB label near
org 07d5ah
PLAYER_UPDATE_AFTER_TEXT ends
main_01 group PLAYER_UPDATE_TEXT, PLAYER_UPDATE_AFTER_TEXT
PLAYER_UPDATE_DGROUP_GAP segment byte public 'CODE' use16
org 0bf20h
PLAYER_UPDATE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _key_det, _shiftkey, _player_input_prev, _player_pos
public _player_option_pos_cur, _player_option_pos_prev
public _player_invincibility_time, _player_respawn_motion_time
public _shot_time, _player_is_hit, _miss_time, _playchar_shot_func
org 03064h
_key_det label word
org 03066h
_shiftkey label byte
org 036d0h
_player_input_prev label word
org 036d2h
_player_pos label byte
org 036e6h
_player_option_pos_cur label dword
org 036eah
_player_option_pos_prev label dword
org 036eeh
_player_invincibility_time label byte
org 036efh
_player_respawn_motion_time label byte
org 036f2h
_shot_time label byte
org 036f3h
_player_is_hit label byte
org 036f4h
_miss_time label byte
org 0c4bch
_playchar_shot_func label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

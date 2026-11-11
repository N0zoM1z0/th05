; Complete target CODE placement and foreign data/helper PUBDEF addresses only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
PLAYER_REGISTER_PREFIX segment byte public 'CODE' use16
assume cs:PLAYER_REGISTER_PREFIX
public TILES_INVALIDATE_AROUND
org (0BAD2h - 0AE10h)
TILES_INVALIDATE_AROUND label near
org (0C9BAh - 0AE10h)
PLAYER_REGISTER_PREFIX ends
PLAYER_REGISTER_TEXT segment byte public 'CODE' use16
PLAYER_REGISTER_TEXT ends
PLAYER_REGISTER_TAIL segment byte public 'CODE' use16
org (014AB0h - 0CAD2h)
PLAYER_REGISTER_TAIL ends
main_01 group PLAYER_REGISTER_PREFIX, PLAYER_REGISTER_TEXT, PLAYER_REGISTER_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03B0h
VECTOR2_AT label far
org (015270h - 014AB0h)
SHARED ends
PLAYER_REGISTER_MAIN03 segment para public 'CODE' use16
org (0209D0h - 015270h)
PLAYER_REGISTER_MAIN03 ends
main_03 group PLAYER_REGISTER_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _player_pos, _player_option_pos_prev
public _miss_time, _miss_explosion_angle, _miss_explosion_radius, _drawpoint
public _playchar_speed_aligned, _playchar_speed_diagonal
org 03502h
_tile_invalidate_box label dword
org 036D2h
_player_pos label byte
org 036DEh
_playchar_speed_aligned label word
org 036E2h
_playchar_speed_diagonal label word
org 036EAh
_player_option_pos_prev label dword
org 036F4h
_miss_time label byte
org 036F7h
_miss_explosion_angle label byte
org 036F8h
_miss_explosion_radius label word
org 036FEh
_drawpoint label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Address-only player context; no bodies/data values/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
PLAYER_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_INVALIDATE_TEXT
public TILES_INVALIDATE_AROUND
org 0cc2h
TILES_INVALIDATE_AROUND label near
org 01baah
PLAYER_INVALIDATE_TEXT ends
PLAYER_REGION_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:PLAYER_REGION_MAIN01_TAIL
org 08065h
PLAYER_REGION_MAIN01_TAIL ends
main_01 group PLAYER_INVALIDATE_TEXT, PLAYER_REGION_MAIN01_TAIL
PLAYER_REGION_SHARED segment para public 'CODE' use16
assume cs:PLAYER_REGION_SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
PLAYER_REGION_SHARED ends
PLAYER_REGION_MAIN03 segment byte public 'CODE' use16
assume cs:PLAYER_REGION_MAIN03
org 0b760h
PLAYER_REGION_MAIN03 ends
main_03 group PLAYER_REGION_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box
org 03502h
_tile_invalidate_box label byte
public _player_pos
org 036d2h
_player_pos label byte
public _player_option_pos_prev
org 036eah
_player_option_pos_prev label byte
public _miss_time
org 036f4h
_miss_time label byte
public _miss_explosion_angle
org 036f7h
_miss_explosion_angle label byte
public _miss_explosion_radius
org 036f8h
_miss_explosion_radius label byte
public _drawpoint
org 036feh
_drawpoint label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

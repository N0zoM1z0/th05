; Address-only player context; no bodies/data values/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
PLAYER_MOVE_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_MOVE_TEXT
org 01c3ch
PLAYER_MOVE_TEXT ends
PLAYER_REGION_MAIN01_TAIL segment byte public 'CODE' use16
assume cs:PLAYER_REGION_MAIN01_TAIL
org 07fdeh
PLAYER_REGION_MAIN01_TAIL ends
main_01 group PLAYER_MOVE_TEXT, PLAYER_REGION_MAIN01_TAIL
PLAYER_REGION_SHARED segment para public 'CODE' use16
assume cs:PLAYER_REGION_SHARED
org 07c0h
PLAYER_REGION_SHARED ends
PLAYER_REGION_MAIN03 segment byte public 'CODE' use16
assume cs:PLAYER_REGION_MAIN03
org 0b760h
PLAYER_REGION_MAIN03 ends
main_03 group PLAYER_REGION_MAIN03
_DATA segment word public 'DATA' use16
public _player_pos
org 036d2h
_player_pos label byte
public _playchar_speed_aligned
org 036deh
_playchar_speed_aligned label byte
public _playchar_speed_diagonal
org 036e2h
_playchar_speed_diagonal label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

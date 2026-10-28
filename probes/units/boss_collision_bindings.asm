; Complete collision owner; every reserve is outside compiler-owned bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0FFFFh
_TEXT ends
COLLISION_MAIN03_GAP segment byte public 'CODE' use16
org (15270h - 0FFFFh)
COLLISION_MAIN03_GAP ends
BOSS_TEXT segment word public 'CODE' use16
BOSS_TEXT ends
BOSS_COLLISION_TEXT segment byte public 'CODE' use16
org (1FD4Fh - 15270h)
BOSS_COLLISION_TEXT ends
main_03 group BOSS_TEXT, BOSS_COLLISION_TEXT
COLLISION_DGROUP_GAP segment para public 'CODE' use16
org (209D0h - 1FD80h)
COLLISION_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _player_pos
org 036D2h
_player_pos label byte
public _player_is_hit
org 036F3h
_player_is_hit label byte
public _boss
org 05ABAh
_boss label byte
_DATA ends
end

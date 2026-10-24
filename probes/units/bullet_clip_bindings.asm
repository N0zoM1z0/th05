; Symbol-only context. All ORG holes are outside the credited C++ function.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FRAME_PADDING segment word public 'CODE' use16
org 0a460h
FRAME_PADDING ends
BULLET_A_TEXT segment word public 'CODE' use16
assume cs:BULLET_A_TEXT
public @playperf_speedtune
org (171eah - 15270h)
@playperf_speedtune label near
org (173deh - 15270h)
BULLET_A_TEXT ends
main_03 group BULLET_A_TEXT
_DATA segment word public 'DATA' use16
public _player_pos, _player_is_hit, _bullet_clear_time
public _group_fixedspeed, _bullet_template
org 36d2h
_player_pos label byte
org 36f3h
_player_is_hit label byte
org 3f97h
_bullet_clear_time label byte
org 41e0h
_group_fixedspeed label byte
org 577eh
_bullet_template label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

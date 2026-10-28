; Complete273-byte updater, real foreign labels and outside extents only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
assume cs:SHOT_HIT_TEXT
public @shots_hittest$qv
org (13683h - 0ae10h)
@shots_hittest$qv label far
org (14ab0h - 0ae10h)
SHOT_HIT_TEXT ends
main_01 group YUKI_SOLO_RENDER_TEXT, SHOT_HIT_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @PlayfieldMotion@update_seg3$qv
org (1527ch - 15270h)
@PlayfieldMotion@update_seg3$qv label near
public _bullets_add_regular
org (17204h - 15270h)
_bullets_add_regular label near
org (18459h - 15270h)
MAIN_035_TEXT ends
; This natural paragraph boundary lies after both273 and278-byte bodies.
B4_UPDATE_AFTER_TEXT segment para public 'CODE' use16
org (209d0h - 18570h)
B4_UPDATE_AFTER_TEXT ends
main_03 group MAIN_035_TEXT, B4_UPDATE_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _player_pos
org 036d2h
_player_pos label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
public _score_delta
org 03712h
_score_delta label dword
public _bullet_template
org 0577eh
_bullet_template label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _shot_hitbox_center
org 0c4c0h
_shot_hitbox_center label dword
public _shot_hitbox_radius
org 0c4c4h
_shot_hitbox_radius label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

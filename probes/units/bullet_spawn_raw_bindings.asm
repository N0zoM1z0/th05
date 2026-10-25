; Original segment frames and external symbols only. No initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPAWN_MAIN01 segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
SPAWN_MAIN01 ends
main_01 group SPAWN_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
BULLET_A_TEXT segment word public 'CODE' use16
assume cs:BULLET_A_TEXT
public VECTOR2_NEAR
org 0006ah
VECTOR2_NEAR label near
public @BULLET_PATNUM_FOR_ANGLE$QUIUC
org 01ce2h
@BULLET_PATNUM_FOR_ANGLE$QUIUC label near
public @gather_add_bullets$qv
org 01d1bh
@gather_add_bullets$qv label near
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
org 01f5ch
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
public _bullets_add_regular
org 01f94h
_bullets_add_regular label near
public _bullet_velocity_and_angle_set
org 01fe2h
_bullet_velocity_and_angle_set label near
public @bullet_template_clip$qv
org 0216eh
@bullet_template_clip$qv label near
org 021cch
BULLET_A_TEXT ends
SPAWN_FOREIGN_TAIL segment word public 'CODE' use16
assume cs:SPAWN_FOREIGN_TAIL
org 0935ah
SPAWN_FOREIGN_TAIL ends
main_03 group BULLET_A_TEXT, SPAWN_FOREIGN_TAIL
_DATA segment word public 'DATA' use16
public _group_is_special
org 018beh
_group_is_special label byte
public _randring
org 03526h
_randring label byte
public _randring_p
org 03626h
_randring_p label word
public _bullet_template_special_angle
org 03f95h
_bullet_template_special_angle label byte
public _bullet_zap
org 03f96h
_bullet_zap label byte
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _group_fixedspeed
org 041e0h
_group_fixedspeed label byte
public _group_i_spread_angle
org 041e1h
_group_i_spread_angle label byte
public _group_i
org 041e2h
_group_i label byte
public _group_i_absolute_angle
org 041e3h
_group_i_absolute_angle label byte
public _group_i_speed
org 041e4h
_group_i_speed label byte
public _group_i_velocity
org 041e5h
_group_i_velocity label byte
public _playperf
org 05770h
_playperf label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _pellets
org 05f2ah
_pellets label byte
public _bullets16
org 075aah
_bullets16 label byte
public _gather_template
org 09ea6h
_gather_template label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

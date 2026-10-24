; Actual foreign code/data context outside the complete615-byte Mai cohort.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 190f7h
AFTER_BASE equ 1935eh
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
MAI_ADV_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MAI_ADV_MAIN01_SPACE ends
main_01 group YUKI_SOLO_RENDER_TEXT, MAI_ADV_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @RANDRING2_NEXT16_AND$QUI
org (0152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
public @BOSS_FLYSTEP_RANDOM$QI
org (015914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
public _bullets_add_special
org (017218h - MAIN03_BASE)
_bullets_add_special label near
public _bullets_add_special_fixedspeed
org (017244h - MAIN03_BASE)
_bullets_add_special_fixedspeed label near
public B4BALLS_ADD
org (0183f0h - MAIN03_BASE)
B4BALLS_ADD label near
org (UNIT_START - MAIN03_BASE)
MAIN_035_TEXT ends
MAI_ADV_TEXT segment byte public 'CODE' use16
MAI_ADV_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @LASER_FIXED_SPAWN$QI
org (1a6efh - AFTER_BASE)
@LASER_FIXED_SPAWN$QI label near
org (DGROUP_BASE - AFTER_BASE)
LASER_SC_TEXT ends
main_03 group MAIN_035_TEXT, MAI_ADV_TEXT, LASER_SC_TEXT
_DATA segment word public 'DATA' use16
public _bullet_special
org 03f94h
_bullet_special label byte
public _bullet_template_special_angle
org 03f95h
_bullet_template_special_angle label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _laser_template
org 05a8ch
_laser_template label byte
public _boss
org 05abah
_boss label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _boss_statebyte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

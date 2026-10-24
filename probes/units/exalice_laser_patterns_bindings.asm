; Real foreign frames and holes outside the complete645-byte pattern owner.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 19c2dh
AFTER_BASE equ 19eb2h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
X_LASER_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
X_LASER_MAIN01_SPACE ends
main_01 group X_LASER_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_PAT_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_MOD$QUI
public @BOSS_FLYSTEP_RANDOM$QI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17218h - MAIN03_BASE)
_bullets_add_special label near
org (UNIT_START - MAIN03_BASE)
EXALICE_PAT_TEXT ends
EXALICE_LSR_TEXT segment byte public 'CODE' use16
EXALICE_LSR_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @lasers_shootout_add$qv, @LASER_FIXED_SPAWN$QI
org (1a66eh - AFTER_BASE)
@lasers_shootout_add$qv label near
org (1a6efh - AFTER_BASE)
@LASER_FIXED_SPAWN$QI label near
org (DGROUP_BASE - AFTER_BASE)
LASER_SC_TEXT ends
main_03 group EXALICE_PAT_TEXT, EXALICE_LSR_TEXT, LASER_SC_TEXT
_DATA segment word public 'DATA' use16
public _exalice_laser_slot, _bullet_special, _bullet_template
public _lasers, _laser_template, _boss, _boss_statebyte
org 1998h
_exalice_laser_slot label word
org 3f94h
_bullet_special label byte
org 577eh
_bullet_template label byte
org 578ch
_lasers label byte
org 5a8ch
_laser_template label byte
org 5abah
_boss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

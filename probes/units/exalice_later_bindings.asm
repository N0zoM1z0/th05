; Foreign symbols and holes outside the three complete600-byte patterns.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 199d5h
AFTER_BASE equ 19c30h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
X_LATER_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
X_LATER_MAIN01_SPACE ends
main_01 group X_LATER_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_PAT_TEXT
public @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI
public @BOSS_FLYSTEP_RANDOM$QI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special, @FIREWAVES_ADD$QIUC
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
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
org (1983dh - MAIN03_BASE)
@FIREWAVES_ADD$QIUC label near
org (UNIT_START - MAIN03_BASE)
EXALICE_PAT_TEXT ends
EXALICE_LAT_TEXT segment byte public 'CODE' use16
EXALICE_LAT_TEXT ends
X_LATER_MAIN03_TAIL segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
X_LATER_MAIN03_TAIL ends
main_03 group EXALICE_PAT_TEXT, EXALICE_LAT_TEXT, X_LATER_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_special, _exalice_aim_origin, _bullet_template, _boss
public _pellet_bottom_col, _boss_statebyte
org 3f94h
_bullet_special label byte
org 4a8ah
_exalice_aim_origin label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 0c33eh
_pellet_bottom_col label word
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

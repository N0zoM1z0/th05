; Genuine symbol-only context around complete remaining Mai/Yuki patterns.
; No target bytes, helper bodies, state values or inside-contribution gaps.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 17c30h
AFTER_BASE equ 17fe0h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01f3ah
IATAN2 label far
org MAIN01_BASE
_TEXT ends
MAI_YUKI_LATER_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MAI_YUKI_LATER_MAIN01_CONTEXT ends
main_01 group MAI_YUKI_LATER_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17218h - MAIN03_BASE)
_bullets_add_special label near
org (UNIT_START - MAIN03_BASE)
MAIN_035_TEXT ends

; The real empty LASER_SC_TEXT from the canonical header merges here in the
; same main03 group. The outside paragraph follows full original end17FDB.
LASER_SC_TEXT segment para public 'CODE' use16
assume cs:LASER_SC_TEXT
public @LASER_MANUAL_FIXED_SPAWN$QI, @LASER_MANUAL_GROW$QI, @LASER_STOP$QI
public @cheetos_add$qv
org (1a74bh - AFTER_BASE)
@LASER_MANUAL_FIXED_SPAWN$QI label near
org (1a7a5h - AFTER_BASE)
@LASER_MANUAL_GROW$QI label near
org (1a7ceh - AFTER_BASE)
@LASER_STOP$QI label near
org (1a82eh - AFTER_BASE)
@cheetos_add$qv label near
org (DGROUP_BASE - AFTER_BASE)
LASER_SC_TEXT ends
main_03 group MAIN_035_TEXT, LASER_SC_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _bullet_template_tune, _bullet_template
public _lasers, _laser_template, _boss, _boss2, _custom_entities, _boss_statebyte
org 36d2h
_player_pos label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
org 578ch
_lasers label byte
org 5a8ch
_laser_template label byte
org 5abah
_boss label byte
org 5ad2h
_boss2 label byte
org 0b3f4h
_custom_entities label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

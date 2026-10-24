; Symbol-only genuine context for three complete later solo Mai attacks.
; No instructions, initialized state, callback entries or inside-function holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 18f07h
AFTER_BASE equ 19100h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
MAI_YUKI_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MAI_YUKI_MAIN01_CONTEXT ends
main_01 group YUKI_SOLO_RENDER_TEXT, MAI_YUKI_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @BOSS_FLYSTEP_RANDOM$QI
public @RANDRING2_NEXT16_AND$QUI
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public _bullets_add_regular, _bullets_add_regular_fixedspeed
public _bullets_add_special_fixedspeed
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
org (1705dh - MAIN03_BASE)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC, B4BALLS_ADD
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17236h - MAIN03_BASE)
_bullets_add_regular_fixedspeed label near
org (17244h - MAIN03_BASE)
_bullets_add_special_fixedspeed label near
org (183f0h - MAIN03_BASE)
B4BALLS_ADD label near
org (UNIT_START - MAIN03_BASE)
MAIN_035_TEXT ends

; The real outside paragraph follows original complete end190F7 at19100.
; This external context supplies no bytes inside the three complete functions.
MAI_YUKI_INITIAL_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
MAI_YUKI_INITIAL_AFTER_TEXT ends
main_03 group MAIN_035_TEXT, MAI_YUKI_INITIAL_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _bullet_template_tune, _mai_pattern_current, _yuki_pattern_current
public _bullet_template, _boss, _boss2, _gather_template, _boss_statebyte
public _bullet_special, _bullet_template_special_angle, _rank
org 3f94h
_bullet_special label byte
org 3f95h
_bullet_template_special_angle label byte
org 41deh
_bullet_template_tune label word
org 442eh
_mai_pattern_current label word
org 4430h
_yuki_pattern_current label word
org 576fh
_rank label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 5ad2h
_boss2 label byte
org 9ea6h
_gather_template label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

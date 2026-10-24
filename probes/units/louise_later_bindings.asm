; Symbol-only original context for the four complete later Louise patterns.
; No helper instructions, initialized values or inside-contribution holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1dae5h
AFTER_BASE equ 1dd40h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
LOUISE_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
LOUISE_MAIN01_CONTEXT ends
main_01 group LOUISE_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

; Match the real foreign LASER_SC_TEXT declaration so its zero compiler
; contribution merges into the original main03 frame rather than after DS.
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @RANDRING2_NEXT16_AND$QUI, _bullets_add_regular, _bullets_add_special
public @lasers_shootout_add$qv, @LOUISE_CHARGE_UPDATE$QI
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (17218h - MAIN03_BASE)
_bullets_add_special label near
org (1a66eh - MAIN03_BASE)
@lasers_shootout_add$qv label near
org (1d938h - MAIN03_BASE)
@LOUISE_CHARGE_UPDATE$QI label near
org (UNIT_START - MAIN03_BASE)
LASER_SC_TEXT ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
B4_UPDATE_TEXT ends

; The full original603-byte contribution ends exactly at the next paragraph.
; This independent context reserves only foreign code after the source owner.
LOUISE_LATER_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
LOUISE_LATER_AFTER_TEXT ends
main_03 group LASER_SC_TEXT, B4_UPDATE_TEXT, LOUISE_LATER_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _bullet_special, _bullet_template_special_angle, _bullet_template_tune
public _bullet_template, _laser_template, _boss, _boss_statebyte
org 3f94h
_bullet_special label byte
org 3f95h
_bullet_template_special_angle label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
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

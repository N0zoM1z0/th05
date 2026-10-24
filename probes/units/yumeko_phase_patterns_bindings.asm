; Genuine original context for three later complete Yumeko attacks.
; Source owns all bytes in its slot; foreign routines are only public labels.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
YUMEKO_PHASE_MAIN01_CONTEXT segment byte public 'CODE' use16
assume cs:YUMEKO_PHASE_MAIN01_CONTEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
org 09ca0h
YUMEKO_PHASE_MAIN01_CONTEXT ends
main_01 group GENERIC_BOSS_MAIN01_TEXT, YUMEKO_PHASE_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY, VECTOR2_AT
org 0232h
SND_SE_PLAY label far
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI
public @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T, SWORDS_ADD
org 003ah
@RANDRING2_NEXT16_AND$QUI label near
org 0050h
@RANDRING2_NEXT16_MOD$QUI label near
org (1705dh - 15270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (171cch - 15270h)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - 15270h)
_bullets_add_regular label near
org (17218h - 15270h)
_bullets_add_special label near
org (176ddh - 15270h)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (1ed41h - 15270h)
SWORDS_ADD label near
org (1f088h - 15270h)
B5_UPDATE_TEXT ends
YUMEKO_PHASE_MAIN03_TAIL segment byte public 'CODE' use16
org (209d0h - 1f3f0h)
YUMEKO_PHASE_MAIN03_TAIL ends
main_03 group BOSS_TEXT, B5_UPDATE_TEXT, YUMEKO_PHASE_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_clear_time, _bullet_template_tune, _bullet_template
public _boss, _custom_entities, _boss_statebyte
org 3f97h
_bullet_clear_time label byte
org 41deh
_bullet_template_tune label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 0b3f4h
_custom_entities label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

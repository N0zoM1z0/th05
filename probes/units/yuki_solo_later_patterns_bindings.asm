; Actual external-symbol context around four complete later Yuki solo functions.
; No helper bodies, initialized state, table values or .stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
assume cs:YUKI_SOLO_RENDER_TEXT
public B4BALLS_RENDER
org 05acfh
B4BALLS_RENDER label near
org 09ca0h
YUKI_SOLO_RENDER_TEXT ends
main_01 group YUKI_SOLO_RENDER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI
public @BOSS_FLYSTEP_RANDOM$QI, @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, _bullets_add_special, B4BALLS_ADD
org 002ch
@randring2_next16$qv label near
org 003ah
@RANDRING2_NEXT16_AND$QUI label near
org (15914h - 15270h)
@BOSS_FLYSTEP_RANDOM$QI label near
org (1705dh - 15270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (171cch - 15270h)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - 15270h)
_bullets_add_regular label near
org (17218h - 15270h)
_bullets_add_special label near
org (183f0h - 15270h)
B4BALLS_ADD label near
org (18767h - 15270h)
MAIN_035_TEXT ends
YUKI_SOLO_AFTER_TEXT segment byte public 'CODE' use16
org (209d0h - 18a05h)
YUKI_SOLO_AFTER_TEXT ends
main_03 group MAIN_035_TEXT, YUKI_SOLO_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _bullet_special, _bullet_template_tune, _rank
public _bullet_template, _boss, _custom_entities, _boss_statebyte
org 3f94h
_bullet_special label byte
org 41deh
_bullet_template_tune label word
org 576fh
_rank label byte
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

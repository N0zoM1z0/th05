; Genuine foreign-only context for the complete 169-byte cheeto-wall pattern.
; No own-function labels, game bytes, artificial prefix or .stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_0_TEXT segment byte public 'CODE' use16
assume cs:MAIN_0_TEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
org 09ca0h
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group MAIN_0_TEXT, BOSS_BG_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @RANDRING2_NEXT16_AND$QUI
org 03ah
@RANDRING2_NEXT16_AND$QUI label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public _bullets_add_regular
org 01f94h
_bullets_add_regular label near
public @cheetos_add$qv
org 055beh
@cheetos_add$qv label near
org (1b016h - 15270h)
LASER_SC_TEXT ends
B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
B6_PATTERN_A_TEXT ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
B6_UPDATE_TEXT ends
CHEETOWALLS_MAIN03_TAIL segment byte public 'CODE' use16
org (209d0h - 1b0bfh)
CHEETOWALLS_MAIN03_TAIL ends
main_03 group BULLET_A_TEXT, LASER_SC_TEXT, B6_BALLS_TEXT, B6_PATTERN_A_TEXT, B6_UPDATE_TEXT, CHEETOWALLS_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_template
org 0577eh
_bullet_template label byte
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

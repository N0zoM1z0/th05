; True external addresses around one complete natural Yumeko sweep.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUMEKO_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:YUMEKO_UPDATE_MAIN01_TEXT
public SELECT_FOR_RANK
org 021a2h
SELECT_FOR_RANK label far
org 09ca0h
YUMEKO_UPDATE_MAIN01_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
main_01 group YUMEKO_UPDATE_MAIN01_TEXT, GENERIC_BOSS_MAIN01_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @RANDRING2_NEXT16_MOD$QUI, @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public _bullets_add_regular, SWORDS_ADD
org 0050h
@RANDRING2_NEXT16_MOD$QUI label near
org (1705dh - 15270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (171cch - 15270h)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (17204h - 15270h)
_bullets_add_regular label near
org (1ed41h - 15270h)
SWORDS_ADD label near
org (1f59ch - 15270h)
B5_UPDATE_TEXT ends
YUMEKO_SWEEP_AFTER_TEXT segment byte public 'CODE' use16
org (209d0h - 1f6ddh)
YUMEKO_SWEEP_AFTER_TEXT ends
main_03 group BOSS_TEXT, B5_UPDATE_TEXT, YUMEKO_SWEEP_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _bullet_template, _boss, _boss2, _custom_entities, _boss_statebyte
org 577eh
_bullet_template label byte
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

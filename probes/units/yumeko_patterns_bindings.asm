; Genuine MAIN context for the three complete Yumeko algorithm functions.
; Only real external symbols and outside-contribution space; no helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUMEKO_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
YUMEKO_MAIN01_CONTEXT ends
main_01 group YUMEKO_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2, SND_SE_PLAY, VECTOR2_AT
org 0008h
VECTOR2 label far
org 0232h
SND_SE_PLAY label far
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI
public @GATHER_ADD_ONLY_3STACK$QIUIUI, _bullets_add_regular, SWORDS_ADD
org 002ch
@randring2_next16$qv label near
org 003ah
@RANDRING2_NEXT16_AND$QUI label near
org 0050h
@RANDRING2_NEXT16_MOD$QUI label near
org (1705dh - 15270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (17204h - 15270h)
_bullets_add_regular label near
org (1ed41h - 15270h)
SWORDS_ADD label near
org (1eed5h - 15270h)
B5_UPDATE_TEXT ends
YUMEKO_MAIN03_TAIL segment byte public 'CODE' use16
org (209d0h - 1f088h)
YUMEKO_MAIN03_TAIL ends
main_03 group B5_UPDATE_TEXT, YUMEKO_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_template_tune, _bullet_template, _boss
public _custom_entities, _boss_statebyte
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

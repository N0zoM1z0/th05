; Address-only context for the complete original121-byte sword allocator.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUMEKO_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
YUMEKO_UPDATE_MAIN01_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:CIRCLE_TEXT
public @CIRCLES_ADD_SHRINKING$QII
org 034c6h
@CIRCLES_ADD_SHRINKING$QII label far
org 09ca0h
CIRCLE_TEXT ends
main_01 group YUMEKO_UPDATE_MAIN01_TEXT, GENERIC_BOSS_MAIN01_TEXT, CIRCLE_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public VECTOR2_NEAR, @BULLET_PATNUM_FOR_ANGLE$QUIUC, @playperf_speedtune
org 006ah
VECTOR2_NEAR label near
org (16f52h - 15270h)
@BULLET_PATNUM_FOR_ANGLE$QUIUC label near
org (171eah - 15270h)
@playperf_speedtune label near
org (1ed41h - 15270h)
B5_UPDATE_TEXT ends
YUMEKO_SWORDS_ADD_AFTER_TEXT segment byte public 'CODE' use16
org (209d0h - 1edbah)
YUMEKO_SWORDS_ADD_AFTER_TEXT ends
main_03 group BOSS_TEXT, B5_UPDATE_TEXT, YUMEKO_SWORDS_ADD_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _circles_color, _custom_entities
org 41dah
_circles_color label byte
org 0b3f4h
_custom_entities label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

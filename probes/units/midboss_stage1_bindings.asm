; Symbol-only TH05 MAIN stage-one midboss context, no executable bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_TEXT segment byte public 'CODE' use16
MAI_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
M1_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
M1_MAIN01_SPACE ends
main_01 group MAI_TEXT, GENERIC_BOSS_MAIN01_TEXT, M1_MAIN01_SPACE
M1_SHARED segment para public 'CODE' use16
assume cs:M1_SHARED
public SND_SE_PLAY, @POLAR$QIII
org 0232h
SND_SE_PLAY label far
org 0394h
@POLAR$QIII label far
org 07c0h
M1_SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
MIDBOSS1_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSS1_TEXT
public @randring2_next16$qv
org 002ch
@randring2_next16$qv label near
org 0832h
MIDBOSS1_TEXT ends
; Follows the complete 543-byte contribution at original15CC1.
M1_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:M1_MAIN03_TAIL
public @SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II
public _bullets_add_regular, _bullets_add_special
public @HUD_HP_UPDATE_AND_RENDER$QII, @MIDBOSS_SCORE_BONUS$QUI
public @midboss_defeat_update$qv, @ITEMS_ADD$QII11ITEM_TYPE_T
public @MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII
org (01c78h - 00a51h)
@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II label near
org (01f94h - 00a51h)
_bullets_add_regular label near
org (01fa8h - 00a51h)
_bullets_add_special label near
org (07286h - 00a51h)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (072deh - 00a51h)
@MIDBOSS_SCORE_BONUS$QUI label near
org (073b8h - 00a51h)
@midboss_defeat_update$qv label near
org (079bbh - 00a51h)
@ITEMS_ADD$QII11ITEM_TYPE_T label near
org (0a820h - 00a51h)
@MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII label near
org (0b760h - 00a51h)
M1_MAIN03_TAIL ends
main_03 group BOSS_TEXT, MIDBOSS1_TEXT, M1_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8, _homing_target, _bullet_zap
public _bullet_template_tune, _bullet_template, _midboss, _boss
org 041ch
_SinTable8 label byte
org 049ch
_CosTable8 label byte
org 3f8ah
_homing_target label byte
org 3f96h
_bullet_zap label byte
org 41deh
_bullet_template_tune label byte
org 577eh
_bullet_template label byte
org 5aa4h
_midboss label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

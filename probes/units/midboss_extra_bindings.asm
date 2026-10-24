; Symbol-only TH05 MAIN Extra-stage midboss context, no executable bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_TEXT segment byte public 'CODE' use16
MAI_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
MX_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
MX_MAIN01_SPACE ends
main_01 group MAI_TEXT, GENERIC_BOSS_MAIN01_TEXT, MX_MAIN01_SPACE
MX_SHARED segment para public 'CODE' use16
assume cs:MX_SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
MX_SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
MIDBOSSX_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSSX_TEXT
public @MIDBOSSX_DASH_UPDATE$QI, @midbossx_pattern_spread$qv
org (163feh - 15270h)
@MIDBOSSX_DASH_UPDATE$QI label near
org (164b6h - 15270h)
@midbossx_pattern_spread$qv label near
org (165b6h - 15270h)
MIDBOSSX_TEXT ends
; Follows the complete 366-byte contribution at original16724.
MX_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:MX_MAIN03_TAIL
public @SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II
public @HUD_HP_UPDATE_AND_RENDER$QII, @MIDBOSS_SCORE_BONUS$QUI
public @midboss_defeat_update$qv, @ITEMS_ADD$QII11ITEM_TYPE_T
public @MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII
org (01c78h - 014b4h)
@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II label near
org (07286h - 014b4h)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (072deh - 014b4h)
@MIDBOSS_SCORE_BONUS$QUI label near
org (073b8h - 014b4h)
@midboss_defeat_update$qv label near
org (079bbh - 014b4h)
@ITEMS_ADD$QII11ITEM_TYPE_T label near
org (0a820h - 014b4h)
@MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII label near
org (0b760h - 014b4h)
MX_MAIN03_TAIL ends
main_03 group BOSS_TEXT, MIDBOSSX_TEXT, MX_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _midbossx_pattern, _midbossx_patterns, _midbossx_dash_angles
public _homing_target, _bullet_zap, _bullet_clear_time
public _bullet_template, _midboss, _gather_template, _boss_statebyte
org 147ah
_midbossx_pattern label byte
org 147ch
_midbossx_patterns label byte
org 1488h
_midbossx_dash_angles label byte
org 3f8ah
_homing_target label byte
org 3f96h
_bullet_zap label byte
org 3f97h
_bullet_clear_time label byte
org 577eh
_bullet_template label byte
org 5aa4h
_midboss label byte
org 9ea6h
_gather_template label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

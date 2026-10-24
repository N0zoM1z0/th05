; Address-only context for genuine stage-four patterns and update callback.
; The whole798-byte compiler contribution occupies its slot; no inner holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 16044h
AFTER_BASE equ 16370h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MIDBOSS4_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MIDBOSS4_MAIN01_CONTEXT ends
main_01 group MIDBOSS4_MAIN01_CONTEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @PlayfieldMotion@update_seg3$qv
public @RANDRING2_NEXT16_MOD$QUI
public @midboss4_pattern_transition$qv
org (1527ch - MAIN03_BASE)
@PlayfieldMotion@update_seg3$qv label near
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (15f74h - MAIN03_BASE)
@midboss4_pattern_transition$qv label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends

MIDBOSS4_AFTER_TEXT segment para public 'CODE' use16
assume cs:MIDBOSS4_AFTER_TEXT
public @SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II
public _bullets_add_regular, _bullets_add_regular_fixedspeed
public @HUD_HP_UPDATE_AND_RENDER$QII, @MIDBOSS_SCORE_BONUS$QUI
public @midboss_defeat_update$qv, @ITEMS_ADD$QII11ITEM_TYPE_T
public @MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII
org (16ee8h - AFTER_BASE)
@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II label near
org (17204h - AFTER_BASE)
_bullets_add_regular label near
org (17236h - AFTER_BASE)
_bullets_add_regular_fixedspeed label near
org (1c4f6h - AFTER_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (1c54eh - AFTER_BASE)
@MIDBOSS_SCORE_BONUS$QUI label near
org (1c628h - AFTER_BASE)
@midboss_defeat_update$qv label near
org (1cc2bh - AFTER_BASE)
@ITEMS_ADD$QII11ITEM_TYPE_T label near
org (1fa90h - AFTER_BASE)
@MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII label near
org (DGROUP_BASE - AFTER_BASE)
MIDBOSS4_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, MIDBOSS4_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _homing_target, _bullet_zap, _bullet_template_tune, _bullet_template
public _midboss, _gather_template, _boss_statebyte
org 3f8ah
_homing_target label byte
org 3f96h
_bullet_zap label byte
org 41deh
_bullet_template_tune label word
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

; Symbol-only genuine MAIN context for the single complete stage-two callback.
; No instructions, initialized values, inside-function holes or .stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 15debh
AFTER_BASE equ 15f80h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MIDBOSS2_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MIDBOSS2_MAIN01_CONTEXT ends
main_01 group MIDBOSS2_MAIN01_CONTEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_BETWEEN_PLUS, SND_SE_PLAY
org 004eh
VECTOR2_BETWEEN_PLUS label far
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @PlayfieldMotion@update_seg3$qv
public @midboss2_move$qv, @midboss2_pattern$qv, @midboss2_pattern_final$qv
org (1527ch - MAIN03_BASE)
@PlayfieldMotion@update_seg3$qv label near
org (15cc1h - MAIN03_BASE)
@midboss2_move$qv label near
org (15d43h - MAIN03_BASE)
@midboss2_pattern$qv label near
org (15db8h - MAIN03_BASE)
@midboss2_pattern_final$qv label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends

; Only the compiler's complete contribution occupies the source slot. Its
; original end15F74 aligns to the separate real context paragraph15F80.
MIDBOSS2_AFTER_TEXT segment para public 'CODE' use16
assume cs:MIDBOSS2_AFTER_TEXT
public @SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II
public @HUD_HP_UPDATE_AND_RENDER$QII, @MIDBOSS_SCORE_BONUS$QUI
public @midboss_defeat_update$qv, @ITEMS_ADD$QII11ITEM_TYPE_T
public @MIDBOSS_HITTEST_SHOTS_DAMAGE$QIII
org (16ee8h - AFTER_BASE)
@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II label near
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
MIDBOSS2_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, MIDBOSS2_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _midboss2_orbit_center, _homing_target, _bullet_zap, _bullet_clear_time
public _bullet_template, _midboss, _boss_statebyte
org 3726h
_midboss2_orbit_center label byte
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
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

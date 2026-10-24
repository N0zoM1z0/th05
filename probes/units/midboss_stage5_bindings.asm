; Address-only context for the complete natural stage-five callback.
; No helper instructions, initialized values or inside-contribution holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 168f2h
AFTER_BASE equ 16a30h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MIDBOSS5_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
MIDBOSS5_MAIN01_CONTEXT ends
main_01 group MIDBOSS5_MAIN01_CONTEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

MAIN_036_TEXT segment byte public 'CODE' use16
assume cs:MAIN_036_TEXT
public @PlayfieldMotion@update_seg3$qv
public @midboss5_flystep$qv, @midboss5_pattern_update$qv
public @midboss5_pattern_blue_spread$qv
org (1527ch - MAIN03_BASE)
@PlayfieldMotion@update_seg3$qv label near
org (16724h - MAIN03_BASE)
@midboss5_flystep$qv label near
org (16768h - MAIN03_BASE)
@midboss5_pattern_update$qv label near
org (167edh - MAIN03_BASE)
@midboss5_pattern_blue_spread$qv label near
org (UNIT_START - MAIN03_BASE)
MAIN_036_TEXT ends

; The original complete318-byte contribution ends16A30, exactly the next
; independent paragraph. Source size remains the actual compiler size.
MIDBOSS5_AFTER_TEXT segment para public 'CODE' use16
assume cs:MIDBOSS5_AFTER_TEXT
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
MIDBOSS5_AFTER_TEXT ends
main_03 group MAIN_036_TEXT, MIDBOSS5_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _MIDBOSS5_PATTERNS, _midboss5_pattern_func
public _homing_target, _bullet_zap, _bullet_template, _midboss
public _gather_template, _boss_statebyte
org 1490h
_MIDBOSS5_PATTERNS label word
org 3788h
_midboss5_pattern_func label word
org 3f8ah
_homing_target label byte
org 3f96h
_bullet_zap label byte
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

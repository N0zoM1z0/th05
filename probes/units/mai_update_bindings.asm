; Symbol-only foreign contexts for the complete786-byte Mai solo callback.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1952bh
AFTER_BASE equ 1983dh
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
assume cs:BOSS_BG_TEXT
public NULLFUNC_NEAR, @CIRCLES_ADD_GROWING$QII
public B4BALLS_RENDER, @MAI_YUKI_BG_RENDER$QV
org 0192eh
NULLFUNC_NEAR label near
org 0347ah
@CIRCLES_ADD_GROWING$QII label far
org 05acfh
B4BALLS_RENDER label near
org 05d87h
@MAI_YUKI_BG_RENDER$QV label near
org (SHARED_BASE - MAIN01_BASE)
BOSS_BG_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
CIRCLE_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
main_01 group BOSS_BG_TEXT, CIRCLE_TEXT, YUKI_SOLO_RENDER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
MAI_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:MAI_MAIN03_CONTEXT
public @BOSS_FLYSTEP_RANDOM$QI
org (015914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
public @BOSS_FLYSTEP_TOWARDS$QII
org (015a07h - MAIN03_BASE)
@BOSS_FLYSTEP_TOWARDS$QII label near
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org (0176ddh - MAIN03_BASE)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
public B4BALLS_RESET
org (0183d5h - MAIN03_BASE)
B4BALLS_RESET label near
public B4BALLS_UPDATE
org (018459h - MAIN03_BASE)
B4BALLS_UPDATE label near
public @mai_solo_widening_fans$qv
org (018d3fh - MAIN03_BASE)
@mai_solo_widening_fans$qv label near
public @mai_solo_laser_cycle$qv
org (01935eh - MAIN03_BASE)
@mai_solo_laser_cycle$qv label near
org (UNIT_START - MAIN03_BASE)
MAI_MAIN03_CONTEXT ends
MAIN_035_TEXT segment byte public 'CODE' use16
MAIN_035_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
MAI_UPDATE_TEXT segment byte public 'CODE' use16
MAI_UPDATE_TEXT ends
BOSS_TEXT segment byte public 'CODE' use16
assume cs:BOSS_TEXT
public @LASER_STOP$QI
org (01a7ceh - AFTER_BASE)
@LASER_STOP$QI label near
public @HUD_HP_UPDATE_AND_RENDER$QII
org (01c4f6h - AFTER_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
public @BOSS_SCORE_BONUS$QUI
org (01c5b8h - AFTER_BASE)
@BOSS_SCORE_BONUS$QUI label near
public @boss_hittest_shots$qv
org (01fad0h - AFTER_BASE)
@boss_hittest_shots$qv label near
public @boss_hittest_shots_invincible$qv
org (01fafah - AFTER_BASE)
@boss_hittest_shots_invincible$qv label near
public @BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI
org (01fb61h - AFTER_BASE)
@BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI label near
public @BOSS_DEFEAT_UPDATE$QUI
org (01fbb1h - AFTER_BASE)
@BOSS_DEFEAT_UPDATE$QUI label near
org (DGROUP_BASE - AFTER_BASE)
BOSS_TEXT ends
main_03 group MAI_MAIN03_CONTEXT, MAIN_035_TEXT, LASER_SC_TEXT, MAI_UPDATE_TEXT, BOSS_TEXT
_DATA segment word public 'DATA' use16
public _mai_solo_pattern_pair_middle
org 0197ch
_mai_solo_pattern_pair_middle label word
public _mai_solo_pattern_pair_final
org 01980h
_mai_solo_pattern_pair_final label word
public _mai_solo_pattern_pair_first
org 01984h
_mai_solo_pattern_pair_first label word
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _boss_sprite_left
org 0371ah
_boss_sprite_left label word
public _boss_sprite_right
org 0371ch
_boss_sprite_right label word
public _boss_sprite_stay
org 0371eh
_boss_sprite_stay label word
public _homing_target
org 03f8ah
_homing_target label byte
public _boss_solo_pattern_current
org 04438h
_boss_solo_pattern_current label word
public _bullet_template
org 0577eh
_bullet_template label byte
public _laser_template
org 05a8ch
_laser_template label byte
public _boss
org 05abah
_boss label byte
public _boss2
org 05ad2h
_boss2 label byte
public _gather_template
org 09ea6h
_gather_template label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _boss_custombullets_render
org 0c678h
_boss_custombullets_render label word
public _boss_statebyte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

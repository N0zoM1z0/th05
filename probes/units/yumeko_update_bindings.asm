; Real symbol-only context for the final helper plus full Yumeko callback.
; No instructions, target table values, owned data or .stack are supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_CONVERT_TINY
org 035a2h
SUPER_CONVERT_TINY label far
org 0ae10h
_TEXT ends
YUMEKO_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:YUMEKO_UPDATE_MAIN01_TEXT
public NULLFUNC_NEAR, @YUMEKO_BG_RENDER$QV, @shots_hittest$qv, SWORDS_RENDER
org 0192eh
NULLFUNC_NEAR label near
org 05e19h
@YUMEKO_BG_RENDER$QV label near
org 08873h
@shots_hittest$qv label far
org 095d0h
SWORDS_RENDER label near
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
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @BOSS_FLYSTEP_TOWARDS$QII, @GATHER_ADD_ONLY_3STACK$QIUIUI
public _bullets_add_special_fixedspeed, @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
public @HUD_HP_UPDATE_AND_RENDER$QII, @BOSS_SCORE_BONUS$QUI
public SWORDS_UPDATE, @YUMEKO_FLYSTEP_BOUNCE$QII
public @yumeko_pattern_sword_fan$qv, @yumeko_pattern_aimed_swords$qv
public @yumeko_pattern_counterrotating_s$qv
public @yumeko_pattern_laser_swords$qv, @yumeko_pattern_sword_sweep$qv
org (15a07h - 15270h)
@BOSS_FLYSTEP_TOWARDS$QII label near
org (1705dh - 15270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (17244h - 15270h)
_bullets_add_special_fixedspeed label near
org (176ddh - 15270h)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (1c4f6h - 15270h)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (1c5b8h - 15270h)
@BOSS_SCORE_BONUS$QUI label near
org (1edbah - 15270h)
SWORDS_UPDATE label near
org (1eed5h - 15270h)
@YUMEKO_FLYSTEP_BOUNCE$QII label near
org (1ef59h - 15270h)
@yumeko_pattern_sword_fan$qv label near
org (1f088h - 15270h)
@yumeko_pattern_aimed_swords$qv label near
org (1f1eah - 15270h)
@yumeko_pattern_counterrotating_s$qv label near
org (1f3f0h - 15270h)
@yumeko_pattern_laser_swords$qv label near
org (1f59ch - 15270h)
@yumeko_pattern_sword_sweep$qv label near
org (1f6ddh - 15270h)
B5_UPDATE_TEXT ends
; Actual generic Boss helpers follow the full source-owned table at1FA51.
BOSS_TEXT segment byte public 'CODE' use16
assume cs:BOSS_TEXT
public @boss_hittest_shots$qv, @boss_hittest_shots_invincible$qv
public @BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI, @BOSS_DEFEAT_UPDATE$QUI
org (1fad0h - 1fa51h)
@boss_hittest_shots$qv label near
org (1fafah - 1fa51h)
@boss_hittest_shots_invincible$qv label near
org (1fb61h - 1fa51h)
@BOSS_PHASE_NEXT$Q16EXPLOSION_TYPE_TI label near
org (1fbb1h - 1fa51h)
@BOSS_DEFEAT_UPDATE$QUI label near
org (209d0h - 1fa51h)
BOSS_TEXT ends
main_03 group B5_UPDATE_TEXT, BOSS_TEXT
_DATA segment word public 'DATA' use16
public _yumeko_patterns_phase2, _yumeko_patterns_phase5
public _bg_render_bombing_func, _boss_sprite_left, _boss_sprite_right, _boss_sprite_stay
public _homing_target, _bullet_special, _bullet_template_special_angle, _bullet_template_tune
public _bullet_template, _boss, _boss2, _gather_template, _custom_entities
public _shot_hitbox_center, _shot_hitbox_radius, _yumeko_pattern, _boss_custombullets_render
public _boss_statebyte
org 1f9eh
_yumeko_patterns_phase2 label byte
org 1fa6h
_yumeko_patterns_phase5 label byte
org 350ah
_bg_render_bombing_func label word
org 371ah
_boss_sprite_left label word
org 371ch
_boss_sprite_right label word
org 371eh
_boss_sprite_stay label word
org 3f8ah
_homing_target label byte
org 3f94h
_bullet_special label byte
org 3f95h
_bullet_template_special_angle label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 5ad2h
_boss2 label byte
org 9ea6h
_gather_template label byte
org 0b3f4h
_custom_entities label byte
org 0c4c0h
_shot_hitbox_center label byte
org 0c4c4h
_shot_hitbox_radius label byte
org 0c670h
_yumeko_pattern label word
org 0c678h
_boss_custombullets_render label word
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end
